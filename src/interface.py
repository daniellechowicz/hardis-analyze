from pyfiglet import Figlet
from time import sleep
import os
import pyfiglet


class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    ENDL = "\033[0m"


class Emojis:
    THUMBS_UP = "\U0001f44d"
    NERD_FACE = "\U0001F913"
    BRAIN = "\U0001F9E0"
    EVERGREEN_TREE = "\U0001F332"
    DECIDUOUS_TREE = "\U0001F333"
    ROCKET = "\U0001F680"
    FLOPPY_DISK = "\U0001F4BE"
    E_MAIL = "\U0001F4E7"
    CHART_INCREASING = "\U0001F4C8"
    WRENCH = "\U0001F527"
    GLOBE = "\U0001F310"


colors = Colors()
emojis = Emojis()


# Some cool fonts:
# banner3-D; basic; larry3d; nancyj-fancy; rev; univers
def print_cool(text, clear=False):
    cool_text = Figlet(font="poison")
    if clear:
        os.system("cls")
    print(colors.GREEN, cool_text.renderText(text), colors.ENDL)


def greet():
    print_cool("HARDIS", clear=True)
    print_cool("Analyze")
    print(
        f"{colors.HEADER}{emojis.WRENCH} Change the settings in the configuration file{colors.ENDL}"
    )
    print(
        f"{colors.HEADER}{emojis.E_MAIL} Have questions? Contact me at d.lechowicz@wood-kplus.at{colors.ENDL}"
    )
    print(
        f"{colors.HEADER}{emojis.GLOBE} Wanna details? Go to https://github.com/daniellechowicz/hardis-analyze{colors.ENDL}"
    )
    print()
    print(f"{colors.WARNING}[INFO] Analysis in progress. Please be patient...")
    print()
