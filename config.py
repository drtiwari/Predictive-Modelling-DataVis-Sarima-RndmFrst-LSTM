# ============================================================================ #
# FILE LOCATION DETAILS
from os.path import join, dirname

from typing import Final

# DIRECTORY PATH
main_loc: Final[str] = dirname(__file__)

########################
# MAIN FOLDERS
dir_DAT: Final[str] = "data"
dir_FIG: Final[str] = "figures"
dir_FUN: Final[str] = "functions"
dir_OUT: Final[str] = "output"
dir_PAR: Final[str] = "params"

#######################
# PRIMARY LOCATIONS
loc_dat: Final[str] = join(main_loc, dir_DAT)
loc_fig: Final[str] = join(main_loc, dir_FIG)
loc_fun: Final[str] = join(main_loc, dir_FUN)
loc_out: Final[str] = join(main_loc, dir_OUT)
loc_par: Final[str] = join(main_loc, dir_PAR)
