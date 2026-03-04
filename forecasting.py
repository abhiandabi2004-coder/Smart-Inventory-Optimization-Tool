def demand_forecast(df):

    df["Forecast_Next_Month"] = df["Sales_Last_30_Days"]

    return df
