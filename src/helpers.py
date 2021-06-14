from config import *
from scipy.signal import butter, hilbert, lfilter
from typing import Any, List, Tuple, Union
import database
import matplotlib.pyplot as plt
import numpy as np
import os


def import_data(filename: str, axis: int) -> np.ndarray:
    path = os.path.join(ROOT, filename)
    data = np.loadtxt(path, delimiter=DELIMITER)
    data = data[:, axis]
    return data


def offset(data: np.ndarray) -> np.ndarray:
    offset_Y = np.mean(data[0:OFFSET_SAMPLES_NO])
    if offset_Y > 0:
        data -= abs(offset_Y)
    else:
        data += abs(offset_Y)
    return data


def butter_lowpass_filter(data: np.ndarray) -> np.ndarray:
    nyq = 0.5 * SAMPLING_FREQUENCY
    normal_cutoff = CUTOFF_FREQUENCY / nyq
    b, a = butter(ORDER, normal_cutoff, btype="low", analog=False)
    y = lfilter(b, a, data)
    return y


def process_scanner(data: np.ndarray, cutting_speed: int) -> List[int]:
    # Specify cutting duration according to applied cutting speed and sampling rate.
    cutting_duration = int(WORKPIECE_LENGTH * SAMPLING_FREQUENCY / cutting_speed)

    # Find a window corresponding to the cutting process.
    values = []
    for i in range(0, len(data)):
        try:
            value = np.mean(abs(data[i : i + cutting_duration]))
            values.append(value)
        except Exception as e:  # in case if i + cutting_duration > len(data)
            pass

    temp_start = values.index(max(values))
    temp_stop = temp_start + cutting_duration
    start = temp_start + int(cutting_duration / 4)
    stop = start + int(cutting_duration / 2)

    # Compensate sensor's latency in its response.
    start = start + int((stop - start) * HORIZONTAL_OFFSET_LEFT)
    stop = stop - int((stop - start) * HORIZONTAL_OFFSET_RIGHT)

    return start, stop


def faster_process_scanner(data: np.ndarray, cutting_speed: int) -> List[int]:
    # Specify cutting duration according to applied cutting speed and sampling rate.
    cutting_duration = int((WORKPIECE_LENGTH / 2) * SAMPLING_FREQUENCY / cutting_speed)

    # Find a window corresponding to the cutting process.
    values = []
    for i in range(0, len(data)):
        try:
            value = np.mean(abs(data[i : i + cutting_duration]))
            values.append(value)
        except Exception as e:  # in case if i + cutting_duration > len(data)
            pass

    start = values.index(max(values))
    stop = start + cutting_duration

    # Compensate sensor's latency in its response.
    start = start + int((stop - start) * HORIZONTAL_OFFSET_LEFT)
    stop = stop - int((stop - start) * HORIZONTAL_OFFSET_RIGHT)

    return start, stop


def prepare(axis: Union[str, int], data: np.ndarray, cutting_speed: int) -> Any:
    """
    To make it more robust, this function accepts several choices.
    """
    axis = str(axis).lower()
    try:
        axis = axis.replace("axis", "")
    except:
        pass

    if (axis == "0") or ("x" in axis):
        if REVERSE_X_AXIS:
            data = (-1) * data
    elif (axis == "1") or ("y" in axis):
        if REVERSE_Y_AXIS:
            data = (-1) * data
    elif (axis == "2") or ("z" in axis):
        if REVERSE_Z_AXIS:
            data = (-1) * data
    else:
        raise Exception(
            f'"{axis}" was specified as the axis. The parameter must be between 0 and 2 or contain the letters "x", "y" or "z".'
        )

    data = offset(data)
    data = butter_lowpass_filter(data)
    start, stop = process_scanner(data, cutting_speed)

    return data, start, stop


def directories_exist() -> None:
    dirs = [
        os.path.join(ROOT, FOLDER_NAME_FIGURES),
        os.path.join(ROOT, FOLDER_NAME_RUCT),
    ]
    for dir_ in dirs:
        if os.path.isdir(dir_):
            if os.path.basename(dir_) == FOLDER_NAME_FIGURES:
                raise Exception(
                    f'The folder "{FOLDER_NAME_FIGURES}" exists. To start the program, cut, delete or rename the "{FOLDER_NAME_FIGURES}" folder.'
                )
            else:
                raise Exception(
                    f'The folder "{FOLDER_NAME_RUCT}" exists. To start the program, cut, delete or rename the "{FOLDER_NAME_RUCT}" folder.'
                )


def extract_parameters(filename: str) -> Tuple[int, float, str]:
    if CUTTING_SPEED != None:
        cutting_speed = int(filename[CUTTING_SPEED[0] : CUTTING_SPEED[1]])
        if (cutting_speed <= 0) or (cutting_speed > 100):
            raise Exception(
                f"Cutting speed equals {cutting_speed} m/s. Make sure that correct indexes are given."
            )
    else:
        raise Exception("Cutting speed is essential and must not be omitted.")

    if FIBRE_ANGLE != None:
        fibre_angle = float(filename[FIBRE_ANGLE[0] : FIBRE_ANGLE[1]])
        if (fibre_angle < 0) or (fibre_angle > 90):
            raise Exception(
                f"Fiber angle should be between 0.0° and 90.0°. Meanwhile, {fibre_angle}° was obtained. Make sure that correct indexes are given."
            )
    else:
        fibre_angle = None

    if MOISTURE_CONTENT != None:
        moisture_content = int(filename[MOISTURE_CONTENT[0] : MOISTURE_CONTENT[1]])
        if moisture_content < 0:
            raise Exception(
                f"Moisture content equals {moisture_content}. Make sure that correct indexes are given."
            )
    else:
        moisture_content = None

    if REPETITION_NO != None:
        repetition_no = int(filename[REPETITION_NO[0] : REPETITION_NO[1]])
    else:
        repetition_no = None

    if SPECIES != None:
        species = str(filename[SPECIES[0] : SPECIES[1]]).lower()
    else:
        species = None

    if TOOL != None:
        tool = str(filename[TOOL[0] : TOOL[1]]).lower()
    else:
        tool = None

    if UNCUT_CHIP_THICKNESS != None:
        uct = filename[UNCUT_CHIP_THICKNESS[0] : UNCUT_CHIP_THICKNESS[1]]
        if "-" in uct:
            uct = float(uct.replace("-", "."))
        else:
            # e.g. CH02 -> 2/10 -> 0.2
            uct = float(float(uct) / 10)

        if uct < 0:
            raise Exception(
                f"Uncut chip thickness equals {uct}. Make sure that correct indexes are given."
            )
    else:
        uct = None

    return (
        cutting_speed,
        fibre_angle,
        moisture_content,
        repetition_no,
        species,
        tool,
        uct,
    )


def save(filename: str, data: np.ndarray, start: int, stop: int) -> None:
    temp = {}

    # Fill in the dataset with the real value of uncut chip thickness.
    temp = {"uncut_chip_thickness_1": None}
    temp["uncut_chip_thickness_1"] = data["uncut_chip_thickness_1"]

    """
    If the X axis is activated, the following instructions will be executed. 
    If the X axis is desactivated, only the template will be created, however its values will be assigned "None".
    """
    if data["axis_x"]["on"] == True:
        """
        0 - raw data
        1 - processed data
        """
        data_0 = data["axis_x"]["0"]
        data_1 = data["axis_x"]["1"]
        temp["axis_x"] = {
            "0": {
                "mean": round(np.mean(data_0[start:stop]), DECIMALS_MEAN),
                "std": round(np.std(data_0[start:stop]), DECIMALS_MEAN),
            },
            "1": {
                "mean": round(np.mean(data_1[start:stop]), DECIMALS_MEAN),
                "std": round(np.std(data_1[start:stop]), DECIMALS_MEAN),
            },
        }
    else:
        temp["axis_x"] = {
            "0": {"mean": None, "std": None},
            "1": {"mean": None, "std": None},
        }

    """
    If the Y axis is activated, the following instructions will be executed. 
    If the Y axis is desactivated, only the template will be created, however its values will be assigned "None".
    """
    if data["axis_y"]["on"] == True:
        """
        0 - raw data
        1 - processed data
        """
        data_0 = data["axis_y"]["0"]
        data_1 = data["axis_y"]["1"]
        temp["axis_y"] = {
            "0": {
                "mean": round(np.mean(data_0[start:stop]), DECIMALS_MEAN),
                "std": round(np.std(data_0[start:stop]), DECIMALS_MEAN),
            },
            "1": {
                "mean": round(np.mean(data_1[start:stop]), DECIMALS_MEAN),
                "std": round(np.std(data_1[start:stop]), DECIMALS_MEAN),
            },
        }
    else:
        temp["axis_y"] = {
            "0": {"mean": None, "std": None},
            "1": {"mean": None, "std": None},
        }

    """
    If the Z axis is activated, the following instructions will be executed. 
    If the Z axis is desactivated, only the template will be created, however its values will be assigned "None".
    """
    if data["axis_z"]["on"] == True:
        """
        0 - raw data
        1 - processed data
        """
        data_0 = data["axis_z"]["0"]
        data_1 = data["axis_z"]["1"]
        temp["axis_z"] = {
            "0": {
                "mean": round(np.mean(data_0[start:stop]), DECIMALS_MEAN),
                "std": round(np.std(data_0[start:stop]), DECIMALS_MEAN),
            },
            "1": {
                "mean": round(np.mean(data_1[start:stop]), DECIMALS_MEAN),
                "std": round(np.std(data_1[start:stop]), DECIMALS_MEAN),
            },
        }
    else:
        temp["axis_z"] = {
            "0": {"mean": None, "std": None},
            "1": {"mean": None, "std": None},
        }
    params = extract_parameters(filename)
    database.Database().insert_into_table(filename, params, temp)


class Plotter(object):
    def plot(
        self, file, data_original, data_corrected, start, stop, axis, cutting_speed
    ):
        # Time and/or y-axis matrices.
        t = np.linspace(0, len(data_corrected), len(data_corrected))

        textstr = "\n".join(
            (
                r"$\mathrm{mean}=%s$ N"
                % str(round(np.mean(data_corrected[start:stop]), DECIMALS_MEAN)),
                r"$\mathrm{std}=%s$ N"
                % str(round(np.std(data_corrected[start:stop]), DECIMALS_STD)),
            )
        )

        props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

        # Adjust figure's range to cutting speed automatically.
        show_from = start - int(WINDOW * 10 / cutting_speed)
        show_to = stop + int(WINDOW * 10 / cutting_speed)

        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.plot(t, data_original, linewidth=0.5, color="dodgerblue", alpha=0.5)
        ax.plot(t, data_corrected, linewidth=0.5, color="red", alpha=1.0)
        ax.scatter(
            t[start:stop],
            data_corrected[start:stop],
            marker="*",
            color="dodgerblue",
            alpha=0.75,
        )
        ax.set_xlabel(X_LABEL_FORCE)
        ax.set_ylabel(Y_LABEL_FORCE)
        ax.set_xlim(show_from, show_to)
        ax.legend(
            [LEGEND_LABEL_1_FORCE, LEGEND_LABEL_2_FORCE, LEGEND_LABEL_3_FORCE],
            loc="upper right",
            fontsize=FONTSIZE,
        )
        ax.text(
            0.025,
            0.95,
            textstr,
            transform=ax.transAxes,
            fontsize=FONTSIZE,
            verticalalignment="top",
            bbox=props,
        )

        # Create a directory where figures will be stored.
        try:
            os.mkdir(os.path.join(ROOT, FOLDER_NAME_FIGURES))
        except:
            pass

        try:
            os.mkdir(os.path.join(ROOT, FOLDER_NAME_FIGURES, axis))
        except:
            pass

        if SAVE_FORCE:
            # Save figure.
            plt.savefig(
                os.path.join(ROOT, FOLDER_NAME_FIGURES, axis, file[:-4] + ".png"),
                dpi=DPI,
            )

        # Close figure (figures created through the pyplot interface may consume too much memory.
        plt.close()
