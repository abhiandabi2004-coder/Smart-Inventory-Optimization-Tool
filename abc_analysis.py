def abc_analysis(df):

    df["Sales_Value"] = df["Sales_Last_30_Days"] * df["Selling_Price"]

    df = df.sort_values(by="Sales_Value", ascending=False)

    total_sales = df["Sales_Value"].sum()

    df["Cumulative_Percentage"] = df["Sales_Value"].cumsum() / total_sales * 100

    def classify(p):

        if p <= 70:
            return "A"

        elif p <= 90:
            return "B"

        else:
            return "C"

    df["ABC_Category"] = df["Cumulative_Percentage"].apply(classify)

    return df