import pandas as pd
import math
import os
from datetime import datetime


# ============================
# LOAD SOI DATA
# ============================

def load_soi():

    soi_files = os.listdir("data/soi")

    if len(soi_files) == 0:
        return None

    latest_soi = sorted(soi_files)[-1]

    soi_path = f"data/soi/{latest_soi}"

    soi_df = pd.read_csv(soi_path)

    soi_df.columns = soi_df.columns.str.strip()

    soi_df["Date of Entry"] = pd.to_datetime(
        soi_df["Date of Entry"],
        errors="coerce"
    )

    today = datetime.today()

    soi_df["Years_of_Service"] = (
        (today - soi_df["Date of Entry"]).dt.days / 365.25
    )

    soi_df["Eligible_LP_Level"] = soi_df["Years_of_Service"].apply(
        lambda x: min(math.floor(x / 5), 5)
    )

    return soi_df


# ============================
# LOAD PAYROLL FILES
# ============================

def load_payroll():

    payroll_files_repo = os.listdir("data/payroll")

    payroll_list = []

    for file in payroll_files_repo:

        path = f"data/payroll/{file}"

        df = pd.read_csv(path)

        df.columns = df.columns.str.strip()

        payroll_list.append(df)

    if len(payroll_list) == 0:
        return None

    payroll_df = pd.concat(payroll_list, ignore_index=True)

    payroll_df["Basic Salary"] = pd.to_numeric(
        payroll_df["Basic Salary"], errors="coerce"
    )

    payroll_df["Longevity Pay"] = pd.to_numeric(
        payroll_df["Longevity Pay"], errors="coerce"
    )

    payroll_df["Payroll_Date"] = pd.to_datetime(
        payroll_df["Payroll Month"] + "-01",
        errors="coerce"
    )

    return payroll_df


# ============================
# MERGE SOI + PAYROLL
# ============================

def merge_datasets(soi_df, payroll_df):

    merged_df = pd.merge(
        payroll_df,
        soi_df,
        on="Serial Number",
        how="inner"
    )

    return merged_df


# ============================
# COMPUTE CORRECT LONGEVITY PAY
# ============================

def compute_longevity(merged_df):

    merged_df["Years_of_Service"] = (
        (merged_df["Payroll_Date"] - merged_df["Date of Entry"]).dt.days / 365.25
    )

    merged_df["LP_Count"] = merged_df["Years_of_Service"].apply(
        lambda x: min(math.floor(x / 5), 5)
    )

    def compute_correct_lp(base_salary, lp_count):

        if lp_count <= 0:
            return 0

        elif lp_count == 5:
            return base_salary * 0.50

        else:
            return base_salary * (1.1 ** lp_count - 1)

    merged_df["Correct_Long_Pay"] = merged_df.apply(
        lambda row: compute_correct_lp(
            row["Basic Salary"],
            row["LP_Count"]
        ),
        axis=1
    )

    merged_df["LP_Difference"] = (
        merged_df["Longevity Pay"] - merged_df["Correct_Long_Pay"]
    ).round(2)

    merged_df["Error_Flag"] = merged_df["LP_Difference"].abs() > 1

    return merged_df


# ============================
# PERSONNEL SUMMARY
# ============================

def create_summary(merged_df):

    summary_df = merged_df.groupby("Serial Number").agg(
        Months_Incorrect=("Error_Flag", "sum"),
        Total_Variance=("LP_Difference", "sum"),
        Total_Overpaid=("LP_Difference", lambda x: x[x > 0].sum()),
        Total_Underpaid=("LP_Difference", lambda x: abs(x[x < 0].sum()))
    ).reset_index()

    return summary_df
