from config import *
import datetime
import os
import pandas as pd
import sqlite3


class Database:
    def __init__(self):
        self.db_name = DB_NAME
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()

        try:
            self.create_table()
        except Exception as e:
            pass

    def connect_to_database(self):
        connection = sqlite3.connect("{}.db".format(self.db_name))
        return connection

    def create_table(self):
        self.connection.cursor().execute(
            """CREATE TABLE data(
            filename TEXT NOT NULL,
            cutting_speed INTEGER NOT NULL,
            fibre_angle REAL,
            moisture_content INTEGER,
            repetition_no INTEGER,
            species TEXT,
            tool TEXT,
            uncut_chip_thickness_0 REAL,
            uncut_chip_thickness_1 REAL,
            axis_x_mean_0 REAL,
            axis_y_mean_0 REAL,
            axis_z_mean_0 REAL,
            axis_x_std_0 REAL,
            axis_y_std_0 REAL,
            axis_z_std_0 REAL,
            axis_x_mean_1 REAL,
            axis_y_mean_1 REAL,
            axis_z_mean_1 REAL,
            axis_x_std_1 REAL,
            axis_y_std_1 REAL,
            axis_z_std_1 REAL);"""
        )
        self.connection.commit()

    def insert_into_table(self, filename, params, data):
        params_ = (
            filename,
            params[0],  # cutting_speed
            params[1],  # fibre_angle
            params[2],  # moisture_content
            params[3],  # repetition_no
            params[4],  # species
            params[5],  # tool
            params[6],  # uncut_chip_thickness_0
            data["uncut_chip_thickness_1"],
            data["axis_x"]["0"]["mean"],
            data["axis_y"]["0"]["mean"],
            data["axis_z"]["0"]["mean"],
            data["axis_x"]["0"]["std"],
            data["axis_y"]["0"]["std"],
            data["axis_z"]["0"]["std"],
            data["axis_x"]["1"]["mean"],
            data["axis_y"]["1"]["mean"],
            data["axis_z"]["1"]["mean"],
            data["axis_x"]["1"]["std"],
            data["axis_y"]["1"]["std"],
            data["axis_z"]["1"]["std"],
        )
        self.cursor.execute(
            """INSERT INTO data (
            filename,
            cutting_speed,
            fibre_angle,
            moisture_content,
            repetition_no,
            species,
            tool,
            uncut_chip_thickness_0,
            uncut_chip_thickness_1,
            axis_x_mean_0,
            axis_y_mean_0,
            axis_z_mean_0,
            axis_x_std_0,
            axis_y_std_0,
            axis_z_std_0,
            axis_x_mean_1,
            axis_y_mean_1,
            axis_z_mean_1,
            axis_x_std_1,
            axis_y_std_1,
            axis_z_std_1) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
            params_,
        )
        self.connection.commit()

    def save_as_CSV(self):
        db = pd.read_sql_query("SELECT * FROM data;", self.connection)
        db.to_csv(
            "{}/{}.csv".format(
                ROOT, str(datetime.datetime.now().strftime(DATE_FORMAT))
            ),
            index=False,
        )

    def delete(self):
        self.connection.close()
        os.remove(self.db_name + ".db")
