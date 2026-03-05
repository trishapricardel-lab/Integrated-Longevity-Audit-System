import os

def create_directories():

    os.makedirs("data", exist_ok=True)
    os.makedirs("data/soi", exist_ok=True)
    os.makedirs("data/orders", exist_ok=True)
    os.makedirs("data/payroll", exist_ok=True)
