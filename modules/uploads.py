import streamlit as st
import os
from modules.audit import log_action


# ============================
# SOI UPLOAD
# ============================

def handle_soi_upload(cursor, conn):

    st.subheader("SOI Source")

    soi_option = st.radio(
        "SOI Data Source",
        ["Use Existing SOI File", "Upload New SOI File"]
    )

    soi_files = []

    if soi_option == "Use Existing SOI File":

        repo_files = os.listdir("data/soi")

        if len(repo_files) > 0:

            selected_files = st.multiselect(
                "Select SOI Files",
                repo_files
            )

            soi_files = [f"data/soi/{f}" for f in selected_files]

        else:
            st.info("No SOI files available in repository.")

    else:

        uploaded_soi = st.file_uploader(
            "Upload SOI CSV Files",
            type=["csv"],
            accept_multiple_files=True
        )

        if uploaded_soi:

            for file in uploaded_soi:

                path = f"data/soi/{file.name}"

                with open(path, "wb") as f:
                    f.write(file.getbuffer())

                log_action(
                    cursor,
                    conn,
                    st.session_state.username,
                    "Upload SOI",
                    file.name
                )

                soi_files.append(path)

            st.success("SOI files saved to repository")

    return soi_files


# ============================
# ORDERS UPLOAD
# ============================

def handle_orders_upload(cursor, conn):

    st.subheader("Longevity Orders Source")

    orders_option = st.radio(
        "Orders Data Source",
        ["Use Existing Orders", "Upload New Orders"]
    )

    orders_files = []

    if orders_option == "Use Existing Orders":

        repo_files = os.listdir("data/orders")

        if len(repo_files) > 0:

            selected_files = st.multiselect(
                "Select Orders Files",
                repo_files
            )

            orders_files = [f"data/orders/{f}" for f in selected_files]

        else:
            st.info("No order files available.")

    else:

        uploaded_orders = st.file_uploader(
            "Upload Orders CSV Files",
            type=["csv"],
            accept_multiple_files=True
        )

        if uploaded_orders:

            for file in uploaded_orders:

                path = f"data/orders/{file.name}"

                with open(path, "wb") as f:
                    f.write(file.getbuffer())

                log_action(
                    cursor,
                    conn,
                    st.session_state.username,
                    "Upload Orders",
                    file.name
                )

                orders_files.append(path)

            st.success("Orders saved to repository")

    return orders_files


# ============================
# PAYROLL UPLOAD
# ============================

def handle_payroll_upload(cursor, conn):

    st.subheader("Payroll Source")

    payroll_option = st.radio(
        "Payroll Data Source",
        ["Use Existing Payroll Files", "Upload New Payroll Files"]
    )

    payroll_files = []

    if payroll_option == "Use Existing Payroll Files":

        payroll_repo = os.listdir("data/payroll")

        if len(payroll_repo) > 0:

            selected_payroll = st.multiselect(
                "Select Payroll Files",
                payroll_repo
            )

            payroll_files = [f"data/payroll/{f}" for f in selected_payroll]

        else:
            st.info("No payroll files available.")

    else:

        uploaded_payroll = st.file_uploader(
            "Upload Payroll CSV Files",
            type=["csv"],
            accept_multiple_files=True
        )

        if uploaded_payroll:

            for file in uploaded_payroll:

                path = f"data/payroll/{file.name}"

                with open(path, "wb") as f:
                    f.write(file.getbuffer())

                log_action(
                    cursor,
                    conn,
                    st.session_state.username,
                    "Upload Payroll",
                    file.name
                )

                payroll_files.append(path)

            st.success("Payroll files saved to repository")

    return payroll_files
