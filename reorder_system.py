def reorder_calculation(df):

    safety_stock = 10

    df["Reorder_Point"] = (df["Daily_Sales"] * df["Lead_Time"]) + safety_stock

    df["Reorder_Quantity"] = df["Reorder_Point"] - df["Current_Stock"]

    df["Reorder_Quantity"] = df["Reorder_Quantity"].apply(lambda x: max(0, round(x)))

    return df
