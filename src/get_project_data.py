from pathlib import Path
import pandas as pd


__all__ = ['locale_data', 'housing_data']

# zip code ranges
_AUSTIN_AREA_ZIP_CODES = [*range(78600, 78799)]
_HOUSTON_AREA_ZIP_CODES = [*range(77000, 77299)]
_DFW_AREA_ZIP_CODES = [*range(75000, 75499), (76000, 76299)]
_SAN_ANTONIO_ZIP_CODE = [*range(78000, 78299)]

_TEXAS_REGIONS = {"austin": _AUSTIN_AREA_ZIP_CODES,
                  "dallas": _DFW_AREA_ZIP_CODES,
                  "fort worth": _DFW_AREA_ZIP_CODES,
                  "dfw": _DFW_AREA_ZIP_CODES,
                  "houston": _HOUSTON_AREA_ZIP_CODES,
                  "san antonio": _SAN_ANTONIO_ZIP_CODE}


def locale_data() -> pd.DataFrame:
    """Get all Texas locale data from DoE NCES `ZCTA Locale Assignments 2021`

    ### DataFrame columns:
        - 'zipcode': 5 digit ZCTA code
        - 'LOCALE':  2 digit Locale assignment

    ---

    file source at: https://nces.ed.gov/programs/edge/Geographic/ZCTAAssignments

    file info at: [NCES PDF](https://nces.ed.gov/programs/edge/docs/EDGE_LOCALE_ZCTA_FILEDOC.pdf)

    :return: 2 column DataFrame for Texas zip codes
    """
    file_path = Path("data/EDGE_ZCTALOCALE_2021_LOCALE.sas7bdat")
    if not file_path.exists():
        raise FileNotFoundError("EDGE_ZCTALOCALE_2021_LOCALE.sas7bdat was not found in data folder")
    
    sas = pd.read_sas(file_path, encoding="utf8")
    sas = sas.astype("Int32")
    land_type = sas[sas["ZCTA5CE20"].between(75000, 79999)]
    land_type = land_type.rename(columns={"ZCTA5CE20": "zipcode"})
    return land_type


def housing_data(region: str = "tx") -> pd.DataFrame:
    """Gives the housing data for Texas with column types already set.

    Valid regions are:
    - austin
    - dallas, fort worth, dfw
    - houston
    - san antonio
    - tx, texas (Default, full state data)

    :param region: region string, defaults to "tx"
    :return: Housing DataFrame for Texas or Texas region
    """
    # check if region is valid
    region_choice = region.lower()
    if region_choice not in _TEXAS_REGIONS and region_choice not in ("tx", "texas"):
        raise ValueError("region: {} is not a valid Texas region. Use [austin, dallas, fort worth, dfw, houston, san antonio, tx, texas]".format(region_choice))

    file_path = Path("data/texas_zipcode_only_housing_data_monthly.csv")
    if not file_path.exists():
        raise FileNotFoundError("texas_zipcode_only_housing_data_monthly.csv was not found in data folder")
    
    # load csv
    as_type = {
        "month_date_yyyymm": str,
        "postal_code": int,
        "zip_name": str,
        "median_listing_price": "Int64",
        "median_listing_price_mm": float,
        "median_listing_price_yy": float,
        "active_listing_count": "Int64",
        "active_listing_count_mm": float,
        "active_listing_count_yy": float,
        "median_days_on_market": "Int64",
        "median_days_on_market_mm": float,
        "median_days_on_market_yy": float,
        "new_listing_count": "Int64",
        "new_listing_count_mm": float,
        "new_listing_count_yy": float,
        "price_increased_count": "Int64",
        "price_increased_count_mm": float,
        "price_increased_count_yy": float,
        "price_reduced_count": "Int64",
        "price_reduced_count_mm": float,
        "price_reduced_count_yy": float,
        "pending_listing_count": "Int64",
        "pending_listing_count_mm": float,
        "pending_listing_count_yy": float,
        "median_listing_price_per_square_foot": "Int64",
        "median_listing_price_per_square_foot_mm": float,
        "median_listing_price_per_square_foot_yy": float,
        "median_square_feet": "Int64",
        "median_square_feet_mm": float,
        "median_square_feet_yy": float,
        "average_listing_price": "Int64",
        "average_listing_price_mm": float,
        "average_listing_price_yy": float,
        "total_listing_count": "Int64",
        "total_listing_count_mm": float,
        "total_listing_count_yy": float,
        "pending_ratio": float,
        "pending_ratio_mm": float,
        "pending_ratio_yy": float,
        "quality_flag": float
        }
    housing_data = pd.read_csv(file_path, dtype=as_type)
    housing_data.rename(columns={"month_date_yyyymm": "date",
                                 "postal_code": "zipcode"}, inplace=True)
    housing_data["date"] = pd.to_datetime(housing_data["date"], format="%Y%m")
    if region in ("tx", "texas"):
        return housing_data
    
    # get only data that is in the correct zipcodes
    region_housing_df = housing_data[housing_data["zipcode"].isin(_TEXAS_REGIONS[region_choice])]
    return region_housing_df
