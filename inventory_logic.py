import pandas as pd

def calculate_inventory_metrics(df):

    df["Daily_Sales"] = df["Sales_Last_30_Days"] / 30

    df["Daily_Sales"] = df["Daily_Sales"].replace(0, 0.01)

    df["Days_of_Stock"] = df["Current_Stock"] / df["Daily_Sales"]

    df["Inventory_Value"] = df["Current_Stock"] * df["Purchase_Cost"]

    def stock_status(days):
        if days < 7:
            return "Reorder"
        elif days <= 60:
            return "Normal"
        else:
            return "Overstock"

    df["Stock_Status"] = df["Days_of_Stock"].apply(stock_status)

    return df