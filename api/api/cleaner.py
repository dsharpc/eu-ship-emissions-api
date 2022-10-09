"""Cleaning function to process the raw data"""

import pandas as pd
import numpy as np

def clean_file(data: bytes) -> pd.DataFrame:
    """Function to clean and rename column to make it easier to work with in the insertion process

    Parameters
    ----------
    data : bytes
        Excel file for the raw data loaded into memory as bytes

    Returns
    -------
    pd.DataFrame
        Clean dataset
    """
    df = pd.read_excel(data, skiprows=2)
    # Clean columns to make them easier to work with
    df.columns = [x.lower().replace(" ", "_") for x in df.columns]
    # Remove rows that have unparsable dates
    df = df[df["doc_issue_date"] != "DoC not issued"]
    # Parse date columns into dates
    df["doc_issue_date"] = pd.to_datetime(df["doc_issue_date"], format="%d/%m/%Y")
    df["doc_expiry_date"] = pd.to_datetime(df["doc_expiry_date"], format="%d/%m/%Y")
    # Rename columns to make them easier to work with
    df = df.rename(columns={
        "total_fuel_consumption_[m_tonnes]": "total_fuel_consumption",
        "total_co₂_emissions_[m_tonnes]": "total_co2_emissions",
        "annual_total_time_spent_at_sea_[hours]": "annual_time_spent_at_sea",
        "annual_time_spent_at_sea_[hours]": "annual_time_spent_at_sea",
        "annual_average_fuel_consumption_per_distance_[kg_/_n_mile]": "average_fuel_consumption_per_distance",
        "annual_average_co₂_emissions_per_distance_[kg_co₂_/_n_mile]": "average_co2_emissions_per_distance"
    })
    # Remove strings from numeric columns
    df.loc[df["average_fuel_consumption_per_distance"] == "Division by zero!", "average_fuel_consumption_per_distance"] = 0
    df.loc[df["average_co2_emissions_per_distance"] == "Division by zero!", "average_co2_emissions_per_distance"] = 0
    # Replace NaNs with Nones, as NaNs cause JSON conversion issues
    df = df.where(df.notnull(), None)
    return df