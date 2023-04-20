from pathlib import Path
import pandas as pd


# ZIP CODE RANGES
# Greater Austin
# ~ Bastrop, Caldwell, Hays, Travis, Williamson Counties
_AUSTIN_AREA_ZIP_CODES = [*range(78600, 78605),
                          78610, 78612, 78613, 78615, 78616, 78617, 78619,
                          78620, 78621, 78622, 78626, 78628, 78633, 78634,
                          78640, 78641, 78642, 78644, 78645, 78648, 78653, 78656, 78659, 
                          78660, 78661, 78662, 78664, 78665, 78666, 78669, 78674, 78676, 78681,
                          78623, 78632, 78650, 78652, 78654, 78655,  # partial West
                          78663, 78670,  # edge outside
                          *range(78700, 78800), # Austin City
                          78953, 78957, # East Edge
                          76527, 76511, 76530, 76537, 76573, 76574, 76578 # North
                          ]
# Dallas/Fort Worth Metroplex
# Dallas ~: Collin, Dallas, Denton, Ellis, Hunt, Kaufman, Rockwall Counties
# Fort Worth ~: Johnson, Parker, Tarrant, Wise Counties
_DALLAS_AREA_ZIP_CODES = [*range(75000, 75020),
                          75022, 75023, *range(75024, 75058), 75060, *range(75061, 75076), *range(75077, 75090), 75091, *range(75093, 75100),
                          75101, 75104, 75114, 75115, 75116, 75119, 75125, 75126, 57132, 75134, 75135, 75137,
                          75141, 75142, 75143, 75146, 75149, 75150, 75152, 75154, *range(75157, 75162), 75164, 75165, 75166, 75167,
                          75172, 75173, 75180, 75181, 75182, 75189, 75390,
                          *range(75200, 75261), *range(75263, 75300),  # Dallas
                          75401, 75402, 75407, 75409, 75422, 75423, 75424, 75442, 75453, 75454, 75474,
                          75428, 75496,  # NW Corner
                          76201, 76203, 76205, *range(76207, 76211), 76226, 76227, 76247, 76249, 76258, 76259, 76262, 76266, # Denton city/county
                          76064, 76065, 76041, 76623, 76651, 76670, 
                          ]
_FORT_WORTH_AREA_ZIP_CODES = [75262, 76050, 76084, # intersect South Dallas
                              *range(76000, 76041), 76044, 76051, 76052, 76053, 76054, 76058, 76059,
                              76060, 76061, 76063, 76066, 76071, 76073, 76078,
                              76082, 76085, 76086, 76087, 76088, 76092, 76093,
                              76225, 76234, 76244, 76248, 76267,
                              *range(76100, 76200),  # Fort Worth City + 76155
                              76426, 76431, 76487, # NW Corner
                              75261  # DFW Airport
                              ]
_DFW_AREA_ZIP_CODES = _DALLAS_AREA_ZIP_CODES + _FORT_WORTH_AREA_ZIP_CODES
# Greater Houston
# ~ Austin, Brazoria, Chambers, Fort Bend, Galveston, Harris, Liberty, Montgomery, Waller Counties
_HOUSTON_AREA_ZIP_CODES = [*range(77000, 77100),  # Houston
                           *range(77200, 77300),  # Houston PO Boxes
                           77301, 77302, 77303, 77304, 77306, 77316, 77318, 77327,
                           77328,
                           77336, 77338, 77339, 77345, 77346, 77354, 77355, 77356, 77357, 77362, 77365, 77368, 77369, 77372,
                           77373, 77375, 77377, 77378, 77379, 77380, 77381, 77382, 77384, 77385, 77386, 77388, 77389, 77396,
                           77401, 77406, 77407, 77417, 77418, 77422, 77423,
                           77426, 77429, 77430, 77431, 77433, 77441, 77444, 77445, 77446, 77447, 77449, 77450,
                           77451, 77459, 77461, 77464, 77466, 77469, 77471, 77473, 77474, 77476, 77477, 77478, 77479,
                           77480, 77481, 77484, 77485, 77486, 77489, 77493, 77494, 77498,
                           77500,
                           *range(77500, 77519), *range(77520, 77585), *range(77586, 77600),
                           *range(77586, 77600),
                           77617, 77623, 77629, 77650, 77661, 77665,  # East
                           78931, 78933, 78944, 78950,  # West
                           ]
# Greater San Antonio
# ~ Atascosa, Bandera, Bexar, Comal, Guadalupe, Kendall, Medina, Wilson Counties
_SAN_ANTONIO_ZIP_CODE = [78002, 78003, 78004, 78006, 78008, 78009, 78010, 78011, 78012, 78013, 78015, 78016, 78023,
                         78026, 78027, 78039, 78050, 78052, 78055, 78056, 78059, 78062, 78063, 78064, 78065, 78066, 78069,
                         78070, 78073, 78074, 78101, 78108, 78109, 78112, 78113, 78114, 78121, 78123, 78124,
                         78130, 78132, 78133, 78143, 78147, 78148, 78150, 78152, 78154, 78155, 78160, 78161, 78163,
                         *range(78200, 78300), # San Antonio
                         78606, 78623, 78638,  # NE
                         78850, 78861, 78883, 78884, 78885, 78886, # West
                         ]

_TEXAS_REGIONS = {"austin": _AUSTIN_AREA_ZIP_CODES,
                  "dallas": _DALLAS_AREA_ZIP_CODES,
                  "fort worth": _FORT_WORTH_AREA_ZIP_CODES,
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
    land_type = sas[sas["ZCTA5CE20"].between(75000, 79999)]  # only Texas Zip Codes
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
    # convert YYYYmm string to datetime (first day of the month)
    housing_data["date"] = pd.to_datetime(housing_data["date"], format="%Y%m")
    if region in ("tx", "texas"):
        return housing_data
    
    # get only data that is in the correct zipcodes
    region_housing_df = housing_data[housing_data["zipcode"].isin(_TEXAS_REGIONS[region_choice])]
    return region_housing_df


def create_texas_only_housing_data(path_to_relator_data: str):
    """
    Create the Texas only CSV file for housing data and saves it to data/

    :param path_to_relator_data: path to the RDC_Inventory_Core_Metrics_Zip_History.csv file
    """
    print("Loading full csv file...")
    housing_csv_df_save = pd.read_csv(path_to_relator_data)
    housing_csv_df_save.drop(housing_csv_df_save.index[-1], inplace=True)
    housing_csv_df_save["zip_ints"] = housing_csv_df_save["postal_code"].astype('int32')
    texas_only = housing_csv_df_save[housing_csv_df_save["zip_ints"].between(75000, 79999)]  # only Texas Zip Codes
    texas_only = texas_only.drop("zip_ints", axis=1)  # not originally there so remove it
    texas_only.to_csv("data/texas_zipcode_only_housing_data_monthly.csv", index=False)
    print(f"File created at: {Path('data/texas_zipcode_only_housing_data_monthly.csv').absolute()}")



