# HARDIS Analyze 1.0

Software for analysis of measurement data obtained with the HARDIS instrument

## Installation (tested on 64-bit version of Windows 10)

1. download the _HARDIS Analyze.exe_ installer (_https://github.com/daniellechowicz/hardis-analyze/raw/main/HARDIS%20Analyze.exe_)
2. run the _HARDIS Analyze.exe_ installer and follow the instructions
3. allow the interpreter _Python 3.9.0_ to be installed
4. allow the application _HARDIS Analyze 1.0_ to be installed
5. go to the _bin_ folder and double-click the _HARDIS Analyze.exe_ to start the application

## Configuration

Before starting the application, go to _config.py_ and adjust the configuration of the analysis. The content of the file is shown below.

```
"""
General notes for those not familiar with Python.
1) Numbering always starts from 0, not from 1.
2) Uppercase and lowercase letters do differ.
3) Use a dot, not a comma, to express decimal values.
4) Never change the data type (e.g. 10.0 is not equal to 10) unless allowed.
   In simple terms, do not add (or remove) a dot where it does not (or does) exist.
5) If you want to edit a string value, do not remove the quotes.
"""


import os


# Paths to required files/directories.
ROOT                = os.path.join("..", "data")
FOLDER_NAME_DATA    = os.path.basename(ROOT)
FOLDER_NAME_FIGURES = "figures"
FOLDER_NAME_RUCT    = "ruct"


# Below are the main variables that determine the scope of the analysis
# and the activation or deactivation of specific software functionalities.
# The charts are saved by default in an automatically created folder inside the root directory.
ACTIVATE_X_AXIS = True
ACTIVATE_Y_AXIS = True
ACTIVATE_Z_AXIS = True
REVERSE_X_AXIS  = False
REVERSE_Y_AXIS  = False
REVERSE_Z_AXIS  = False
SAVE_FORCE      = True
SAVE_RUCT_1     = True # Activation or deactivation of the figure showing the final result of the chip thickness analysis (two horizontal lines representing values before and after cutting).
SAVE_RUCT_2     = True # Activation or deactivation of the graphs showing the found regions for each cut before and after cutting.
SAVE_RUCT_3     = True # Activation or deactivation of the overall graph showing the entire measurement file with the found regions (peak analysis) that were analyzed.


# DAQ-related parameters; frequencies given in [Hz].
SAMPLING_FREQUENCY = 200000
DELIMITER          = "," # Delimiter used in saved measurement files. To find out what delimiter was used, open the measurement file and see what character separates consecutive values. The most common are: ",", ";", "\t".


# Assign the appropriate parameters to the indices in the filename.
# Leave "None" as the default value in case no parameter is available.
# Note: cutting speed is essential and must not be omitted!
CUTTING_SPEED        = (20, 22)
FIBRE_ANGLE          = (11, 13)
MOISTURE_CONTENT     = None
REPETITION_NO        = (0, 3)
SPECIES              = (4, 8)
TOOL                 = None
UNCUT_CHIP_THICKNESS = (16, 18)


# For different data acquisition parameters, the channels corresponding to each force may change.
# Adjust the following values to your measurement data (having in mind that numbering always starts from 0).
CORRESPONDING_CHANNELS = {"x": 1, "y": 2, "z": 3, "distance": 4}


# Proper force names corresponding to the various axes of the force sensor.
CORRESPONDING_FORCES  = {"x": "tangential", "y": "feed", "z": "normal"}


# As the forces are sometimes shifted by a certain amount with respect to the abscissa axis,
# a correction is necessary. Correction is done by calculating the average of the first samples of the measurement file,
# the number of which is determined by the variable below,
# and then subtracting (or adding) the calculated value from each record present in the measurement file.
OFFSET_SAMPLES_NO = 10000


# Butterworth low-pass filter; frequencies given in [Hz].
# Through trial and error, it was determined that optimal results are obtained using a cutoff frequency of 1500 Hz and an order of 3.
CUTOFF_FREQUENCY = 1500 # Note: the term is somewhat misleading since the cutoff frequency is not the point at which the filter completely blocks frequencies, but rather the point at which the filter has just begun to take effect.
ORDER            = 3


# Workpiece's length (PUR, wood, PUR) in [m].
# This value, along with the cutting speed and sampling frequency, is used to calculate the cutting time,
# which is then used to find the corresponding cut in the measurement file.
WORKPIECE_LENGTH           = 0.2


# Required for chip thickness correction (peak finder).
# Do not change this value.
MAX_REVOLUTIONS_PER_SECOND = 8


# The following variable specifies an offset from the found start and end of cutting.
# Limits are needed to create figures - the larger the size of this variable,
# the more samples will be included in the figure.
# It does not affect the analytical part of the analysis - it is used for figures only.
# The number specified below is the default number for cutting speed of 10 [m/s].
# The higher the cutting speed, the lower the number of samples - the size of the figure
# will adapt automatically to the cutting speed.
WINDOW = 2000


# Due to the sensor delay and high sampling rate (the strength increases
# and only stabilizes at a certain level after some time), the whole range
# cannot be taken for analysis.
# Determine the left and right offsets (fraction of cutting time).
HORIZONTAL_OFFSET_LEFT  = 0.1  # must be < 0.5
HORIZONTAL_OFFSET_RIGHT = 0.1  # must be < 0.5


# Figure-related parameters.
DPI                  = 200 # Dots per inch; the higher the dot density, the higher the resolution of the figure.
FIGSIZE              = (10, 5) # Size of the figure. The dimensions correspond to the relative width and height of the figure, respectively.
FONTSIZE             = 16 # Fontsize of the following properties: title, labels, legend, statistics.
TICK_FONTSIZE_1      = 14
TICK_FONTSIZE_2      = 14
FORMAT               = "png" # Try out different formats (vector graphics formats included). Both lowercase and uppercase letters will work.
X_LABEL_FORCE        = "Sample [-]"
Y_LABEL_FORCE        = "Force [N]"
X_LABEL_RUCT         = "Sample [-]"
Y_LABEL_RUCT         = "Distance [mm]"
LEGEND_LABEL_1_FORCE = "Unfiltered"
LEGEND_LABEL_2_FORCE = "Filtered"
LEGEND_LABEL_3_FORCE = "Selected"


# Specify the number of decimal places for each value.
# The mean value and standard deviation will be rounded to the specified decimal place.
# This setting will have an effect on the statistics seen in the saved figures, as well as in the data file.
DECIMALS_MEAN                 = 2
DECIMALS_STD                  = DECIMALS_MEAN + 1
DECIMALS_UNCUT_CHIP_THICKNESS = 3
DECIMALS_RATIO                = 1


# Additional parameters required by the script.
DATE_FORMAT = "%d-%m-%Y %H.%M"
DB_NAME     = "stats"


# User inputs.
REQ_CUTTING_SPEED = "[INPUT] Enter the cutting speed used in the experiment: "
```
