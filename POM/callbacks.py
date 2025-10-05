

import sys
import time
import os
import copy
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import mcdm_func_lib.src.TOPSIC as topsis



def _SaveResult(data,method,filename=None):
    if not filename:
        # Get the current date and time
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_with_datetime = f"Output_results_{method}{timestamp_str}.txt"
    try:
        with open(filename_with_datetime, "w") as f:
            f.write(data)
        print(f"File '{filename_with_datetime}' created successfully.")
    except IOError as e:
        print(f"Error creating file: {e}")

def main_run(raw_df,normalize_method):
    ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP= topsis.TOPSIS_run(raw_df,normalize_method)
    return ALTS, NUM_ALTS, ATBS, NUM_ATBS,WEIGHTS,ATB_PROP
