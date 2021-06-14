"""
This is the first step of the analysis.
The following script calculates basic statistics from the measurement data,
then creates and saves figures for specified axes.
"""

from config import *
from distance import RUCT
from helpers import *
from interface import greet
from tqdm import tqdm
import database
import numpy as np
import os


def main():
    greet()
    directories_exist()
    files = os.listdir(ROOT)
    for file in tqdm(files):
        if not file.endswith(".txt"):
            continue

        # Empty dictionary.
        df = {}

        # Get real uncut chip thickness.
        ruct = RUCT(file)
        df["uncut_chip_thickness_1"] = ruct.ruct

        # Get cuttingn speed. Requirement of "prepare" function.
        cutting_speed = extract_parameters(file)[0]

        # Since "start" and "stop" variables can be found the most effectively
        # using the feed force, the script starts with Y-axis.
        # Therefore, independently from the user's choice, Y-axis is always analyzed.
        data_raw_y = import_data(file, CORRESPONDING_CHANNELS["y"])
        data_clean_y, start, stop = prepare("y", data_raw_y, cutting_speed)
        df["axis_y"] = {"on": True, "0": data_raw_y, "1": data_clean_y}
        Plotter().plot(
            file,
            data_raw_y,
            data_clean_y,
            start,
            stop,
            CORRESPONDING_FORCES["y"],
            cutting_speed,
        )

        # These will be overriden in case if either of X_AXIS or Z_AXIS is set to "True".
        df["axis_x"] = {
            "on": False,
        }
        df["axis_z"] = {
            "on": False,
        }

        if ACTIVATE_X_AXIS:
            data_raw_x = import_data(file, CORRESPONDING_CHANNELS["x"])
            data_clean_x, _, _ = prepare("x", data_raw_x, cutting_speed)
            df["axis_x"] = {"on": True, "0": data_raw_x, "1": data_clean_x}
            Plotter().plot(
                file,
                data_raw_x,
                data_clean_x,
                start,
                stop,
                CORRESPONDING_FORCES["x"],
                cutting_speed,
            )

        if ACTIVATE_Z_AXIS:
            data_raw_z = import_data(file, CORRESPONDING_CHANNELS["z"])
            data_clean_z, _, _ = prepare("z", data_raw_z, cutting_speed)
            df["axis_z"] = {"on": True, "0": data_raw_z, "1": data_clean_z}
            Plotter().plot(
                file,
                data_raw_z,
                data_clean_z,
                start,
                stop,
                CORRESPONDING_FORCES["z"],
                cutting_speed,
            )

        # Pass the dataframe and save it using SQL queries.
        # Then, the database will be converted to CSV.
        save(file, df, start, stop)

    database.Database().save_as_CSV()
    database.Database().delete()


if __name__ == "__main__":
    main()
