import streamlit as st
import os
import pandas as pd
from modules.audit import log_action


def admin_controls(cursor, conn):

    # Admin only
    if st.session_state.role != "Admin":
        return

    st.sidebar.markdown("## ⚙️ Admin Controls")

    # ============================
    # DELETE SOI FILE
    # ============================

    st.sidebar.subheader("Delete SOI File")

    soi_files = os.listdir("data/soi")

    if len(soi_files) > 0:

        soi_to_delete = st.sidebar.selectbox(
            "Select SOI File",
            soi_files,
            key="delete_soi"
        )

        confirm_soi = st.sidebar.checkbox(
            "Confirm SOI deletion",
            key="confirm_soi"
        )

        if confirm_soi and st.sidebar.button("Delete SOI File"):

            os.remove(f"data/soi/{soi_to_delete}")

            log_action(
                cursor,
                conn,
                st.session_state.username,
                "Delete SOI File",
                soi_to_delete
            )

            st.sidebar.success("SOI file deleted successfully")
            st.rerun()

    else:
        st.sidebar.write("No SOI files found")

    # ============================
    # DELETE ORDER FILE
    # ============================

    st.sidebar.subheader("Delete Order File")

    order_files = os.listdir("data/orders")

    if len(order_files) > 0:

        order_to_delete = st.sidebar.selectbox(
            "Select Order File",
            order_files,
            key="delete_order"
        )

        confirm_order = st.sidebar.checkbox(
            "Confirm order deletion",
            key="confirm_order"
        )

        if confirm_order and st.sidebar.button("Delete Order File"):

            os.remove(f"data/orders/{order_to_delete}")

            log_action(
                cursor,
                conn,
                st.session_state.username,
                "Delete Order File",
                order_to_delete
            )

            st.sidebar.success("Order file deleted successfully")
            st.rerun()

    else:
        st.sidebar.write("No order files found")

    # ============================
    # DELETE PAYROLL FILE
    # ============================

    st.sidebar.subheader("Delete Payroll File")

    payroll_repo_files = os.listdir("data/payroll")

    if len(payroll_repo_files) > 0:

        payroll_to_delete = st.sidebar.selectbox(
            "Select Payroll File",
            payroll_repo_files,
            key="delete_payroll"
        )

        confirm_payroll = st.sidebar.checkbox(
            "Confirm payroll deletion",
            key="confirm_payroll"
        )

        if confirm_payroll and st.sidebar.button("Delete Payroll File"):

            os.remove(f"data/payroll/{payroll_to_delete}")

            log_action(
                cursor,
                conn,
                st.session_state.username,
                "Delete Payroll File",
                payroll_to_delete
            )

            st.sidebar.success("Payroll file deleted successfully")
            st.rerun()

    else:
        st.sidebar.write("No payroll files found")

    # ============================
    # DELETE AUDIT LOG ENTRY
    # ============================

    st.sidebar.subheader("Delete Audit Log Entry")

    log_df = pd.read_sql_query(
        "SELECT id, username, action, filename, timestamp FROM audit_log ORDER BY id DESC",
        conn
    )

    if len(log_df) > 0:

        selected_log = st.sidebar.selectbox(
            "Select Log ID",
            log_df["id"]
        )

        confirm_log = st.sidebar.checkbox("Confirm log deletion")

        if confirm_log and st.sidebar.button("Delete Log Entry"):

            cursor.execute(
                "DELETE FROM audit_log WHERE id=?",
                (selected_log,)
            )

            conn.commit()

            st.sidebar.success("Log entry deleted")
            st.rerun()

    else:
        st.sidebar.write("No logs available")

    # ============================
    # RESET SYSTEM
    # ============================

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚠ Reset Entire System")

    confirm_reset = st.sidebar.checkbox("Confirm FULL system reset")

    if confirm_reset and st.sidebar.button("Reset System"):

        # Delete all files
        for folder in ["data/soi", "data/orders", "data/payroll"]:
            for file in os.listdir(folder):
                os.remove(f"{folder}/{file}")

        # Clear database tables
        cursor.execute("DELETE FROM soi")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM payroll")
        cursor.execute("DELETE FROM audit_log")

        conn.commit()

        st.sidebar.success("System has been fully reset")

        st.rerun()
