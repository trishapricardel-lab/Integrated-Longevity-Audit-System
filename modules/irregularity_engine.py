import pandas as pd

def detect_mismatch(merged_df):

    mismatches = merged_df[
        merged_df["Error_Flag"] == True
    ]

    return mismatches
