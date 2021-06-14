from config import *
from helpers import *
from scipy.signal import find_peaks
from scipy import stats
import math
import matplotlib.pyplot as plt
import numpy as np
import os


# Real uncut chip thickness
class RUCT:
    ruct = 0
    ratio = 0
    mean_range_1 = 0
    mean_range_2 = 0

    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.join(ROOT, filename)
        self.run_pipeline()

    def run_pipeline(self):
        self.create_folders()
        self.set_cutting_speed()
        self.set_rotation_duration()
        self.set_cutting_duration()
        self.set_uncut_chip_thickness()
        self.import_data()
        self.remove_noisy_part()
        self.set_stats()
        if SAVE_RUCT_1:
            self.plot()

    def set_cutting_speed(self):
        self.cutting_speed = extract_parameters(self.filename)[0]

    def set_rotation_duration(self):
        self.rotation_duration = int(
            (1 / MAX_REVOLUTIONS_PER_SECOND)
            * (100 / self.cutting_speed)
            * SAMPLING_FREQUENCY
        )

    def set_uncut_chip_thickness(self):
        self.uct = extract_parameters(self.filename)[6]

    def set_cutting_duration(self):
        self.cutting_duration = int(0.2 * SAMPLING_FREQUENCY / self.cutting_speed)

    def remove_noisy_part(self):
        """
        After cutting, the chips fly in front of the laser beam,
        so the signal is distorted. To remove the effect of this on the data,
        one rotation of the arm after the start of the cutting process will be set to 0.
        """
        self.data[self.cutting_start : self.cutting_start + self.rotation_duration] = 0

    def import_data(self):
        self.data = np.loadtxt(self.path, delimiter=DELIMITER)
        # Since cutting start can be found the most effectively
        # using the feed force, the script works with Y-axis.
        _, self.cutting_start, _ = prepare(
            "y", self.data[:, CORRESPONDING_CHANNELS["y"]], self.cutting_speed
        )
        self.data = abs(self.data[:, CORRESPONDING_CHANNELS["distance"]])

    def get_ranges_of_interest(self, data, peaks):
        # One sample was found for each region of interest.
        # Now it is necessary to find the entire range corresponding to the cut sample.
        data_workpiece = np.array(
            []
        )  # The values from the found ranges will be stored here.
        after_cutting = np.array([])
        for peak in peaks:
            if peak - self.cutting_duration < 0:
                start, stop = process_scanner(
                    data[0 : peak + self.cutting_duration], self.cutting_speed
                )
            elif peak + self.cutting_duration > len(data):
                start, stop = process_scanner(
                    data[peak - self.cutting_duration :], self.cutting_speed
                )
            else:
                start, stop = process_scanner(
                    data[peak - self.cutting_duration : peak + self.cutting_duration],
                    self.cutting_speed,
                )

            data_ = data[peak - self.cutting_duration : peak + self.cutting_duration]
            data_workpiece = np.concatenate((data_workpiece, data_[start:stop]))

            if SAVE_RUCT_2:
                self.plot_all(peak, data_, start, stop)

            # If the values are before the specimen is cut,
            # then give them an index equal to "0". Otherwise, "1".
            if peak <= self.cutting_start:
                after_cutting = np.concatenate(
                    (after_cutting, [0] * len(data_[start:stop]))
                )
            else:
                after_cutting = np.concatenate(
                    (after_cutting, [1] * len(data_[start:stop]))
                )

        difference_at = np.where(after_cutting == 1)[0][0]
        range_1 = data_workpiece[:difference_at]
        range_2 = data_workpiece[difference_at:]
        return range_1, range_2

    def get_stats(self, range_1, range_2):
        mean_range_1 = np.median(range_1)
        mean_range_2 = np.median(range_2)
        real_uncut_chip_thickness = abs(mean_range_1 - mean_range_2)
        ratio = ((real_uncut_chip_thickness / self.uct) - 1) * 100
        return (
            round(real_uncut_chip_thickness, DECIMALS_UNCUT_CHIP_THICKNESS),
            round(ratio, DECIMALS_RATIO),
            mean_range_1,
            mean_range_2,
        )

    def set_stats(self):
        peaks, _ = find_peaks(self.data, distance=self.rotation_duration)

        if SAVE_RUCT_3:
            self.plot_entire(self.data, peaks)

        # These will be used for plotting purposes.
        self.range_1, self.range_2 = self.get_ranges_of_interest(self.data, peaks)

        # Overriding the variables belonging to the class with the calculated statistics.
        ruct, ratio, mean_range_1, mean_range_2 = self.get_stats(
            self.range_1, self.range_2
        )
        self.ruct = ruct
        self.ratio = ratio
        self.mean_range_1 = mean_range_1
        self.mean_range_2 = mean_range_2

    def get_canvas(self, spines_off=False):
        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.set_xlabel(X_LABEL_RUCT, fontsize=FONTSIZE)
        ax.set_ylabel(Y_LABEL_RUCT, fontsize=FONTSIZE)
        ax.tick_params(axis="both", which="major", labelsize=TICK_FONTSIZE_1)
        ax.tick_params(axis="both", which="minor", labelsize=TICK_FONTSIZE_2)
        if spines_off:
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        return ax

    def create_folders(self):
        if SAVE_RUCT_1:
            try:
                os.mkdir(os.path.join(ROOT, FOLDER_NAME_RUCT))
            except:
                pass

        if SAVE_RUCT_2:
            try:
                os.mkdir(os.path.join(ROOT, FOLDER_NAME_RUCT, self.filename[:-4]))
            except:
                pass

        if SAVE_RUCT_3:
            try:
                os.mkdir(os.path.join(ROOT, FOLDER_NAME_RUCT))
            except:
                pass

    def plot(self):
        x1 = np.linspace(0, len(self.range_1), len(self.range_1))
        x2 = np.linspace(len(x1), len(x1) + len(self.range_2), len(self.range_2))
        ax = self.get_canvas()
        ax.plot(x1, self.range_1, linewidth=0.5, linestyle="--", color="blue")
        ax.plot(x2, self.range_2, linewidth=0.5, linestyle="--", color="red")
        ax.axhline(y=self.mean_range_1, color="blue", linestyle="-")
        ax.axhline(y=self.mean_range_2, color="red", linestyle="-")
        plt.savefig(
            os.path.join(ROOT, FOLDER_NAME_RUCT, self.filename[:-3] + FORMAT), dpi=DPI
        )
        plt.close()

    def plot_all(self, counter, data, start, stop):
        x = np.linspace(0, len(data), len(data))
        ax = self.get_canvas(spines_off=True)
        ax.plot(x, data, linewidth=0.5, linestyle="-", color="blue")
        ax.plot(
            x[start:stop], data[start:stop], linewidth=1, linestyle="-", color="red"
        )
        plt.savefig(
            os.path.join(
                ROOT, FOLDER_NAME_RUCT, self.filename[:-4], str(counter) + "." + FORMAT
            ),
            dpi=DPI,
        )
        plt.close()

    def plot_entire(self, data, peaks):
        x = np.linspace(0, len(data), len(data))
        ax = self.get_canvas(spines_off=True)
        ax.plot(data, linewidth=0.5, linestyle="-", color="blue")
        ax.plot(peaks, data[peaks], "x", color="orange")
        plt.savefig(
            os.path.join(ROOT, FOLDER_NAME_RUCT, "E_" + self.filename[:-3] + FORMAT),
            dpi=DPI,
        )
        plt.close()
