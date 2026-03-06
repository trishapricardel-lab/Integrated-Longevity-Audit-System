import pandas as pd
from datetime import datetime


# ============================
# GENERATE CASES
# ============================

def generate_cases(mismatches):

    if mismatches is None or mismatches.empty:
        return pd.DataFrame()

    cases = []

    for _, row in mismatches.iterrows():

        serial = row["Serial Number"]
        diff = row["LP_Difference"]

        # Determine issue type
        if diff > 1:
            issue = "Incorrect Longevity Pay (Overpayment)"
            amount = round(diff, 2)

        elif diff < -1:
            issue = "Incorrect Longevity Pay (Underpayment)"
            amount = round(abs(diff), 2)

        else:
            continue

        case = {
            "Case_ID": f"LP-{serial}",
            "Serial Number": serial,
            "Issue": issue,
            "Amount": amount,
            "Status": "Open",
            "Date Detected": datetime.now().strftime("%Y-%m-%d")
        }

        cases.append(case)

    cases_df = pd.DataFrame(cases)

    return cases_df