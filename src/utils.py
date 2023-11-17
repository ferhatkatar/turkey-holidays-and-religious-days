import pandas as pd
from workalendar.europe import Turkey
import holidays


def generate_holidays_dataset(holidays=holidays):
    """
    Creates a consolidated DataFrame containing both religious and non-religious holidays for the years 2022 to 2031.

    Returns:
    -------
    pd.DataFrame
        A DataFrame with columns 'ds' (date), secular holidays, and indicators for religious events
        such as 'Ramadan Feast', 'Sacrifice Feast', and 'Fasting'.
    """
    ####################################################################
    ############## CREATE RELIGIOUS DATAFRAME ##########################
    ####################################################################

    # Create a calendar object
    cal = Turkey()

    # Initialize lists to store holiday dates and names
    dates = []
    names = []

    # Iterate through Turkish holidays between 2022 and 2031
    for holiday in holidays.Turkey(years=range(2022, 2032)).items():
        date = holiday[0].strftime('%Y-%m-%d')
        name = holiday[1]
        # Check if the holiday is related to Ramadan or Sacrifice Feast
        if "Ramadan Feast" in name or "Sacrifice Feast" in name:
            names.append(name)
            dates.append(date)

    # Create a dictionary to store special days with dates as keys and names as values
    special_days = {}

    # Populate the dictionary with dates and corresponding holiday names
    for date, name in zip(dates, names):
        if date not in special_days:
            special_days[date] = [name]
        else:
            special_days[date].append(name)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame.from_dict(special_days, orient='index', columns=['name'])

    # Set the index to the date column
    df.index.name = 'date'
    df_religious = df.reset_index()

    # Sort the DataFrame by date
    df_religious = df_religious.sort_values('date')

    # Perform one-hot encoding for holiday names
    df_religious = pd.get_dummies(df_religious, columns=['name'], prefix='', prefix_sep='')

    # Reset index and sort the DataFrame
    df_religious.reset_index(drop=True, inplace=True)

    # Create a list of all dates between 2022-01-01 and 2031-12-31
    date_range = pd.date_range(start='2022-01-01', end='2031-12-31', freq='D').strftime('%Y-%m-%d')

    # Create a DataFrame with all dates in the range
    df_all_dates = pd.DataFrame({'date': date_range})

    # Merge the special days DataFrame with the all dates DataFrame
    df_religious_final = pd.merge(df_all_dates, df_religious, on='date', how='left')

    # Fill NaN values with 0
    df_religious_final.fillna(0, inplace=True)

    # Convert float to int for relevant columns
    convert_float_to_int = [i for i in df_religious_final if i != "date"]
    df_religious_final[convert_float_to_int] = df_religious_final[convert_float_to_int].astype(int)

    # Display the head of the DataFrame and column names
    print(df_religious_final.head())
    print(df_religious_final.columns)

    # Identify columns related to Ramadan Feast
    renamed_col_ramadan = [col for col in df_religious_final.columns if 'Ramadan Feast' in col]

    # Sum columns related to Ramadan Feast and create a new column
    df_religious_final['Ramadan Feast'] = df_religious_final[renamed_col_ramadan].sum(axis=1)

    # Drop the original columns
    df_religious_final = df_religious_final.drop(renamed_col_ramadan, axis=1)

    # Identify columns related to Sacrifice Feast
    renamed_col_sacrifice_feast = [col for col in df_religious_final.columns if 'Sacrifice Feast' in col]

    # Sum columns related to Sacrifice Feast and create a new column
    df_religious_final['Sacrifice Feast'] = df_religious_final[renamed_col_sacrifice_feast].sum(axis=1)

    # Drop the original columns
    df_religious_final = df_religious_final.drop(renamed_col_sacrifice_feast, axis=1)

    # Set 1 in the Ramadan Feast column for the two days following the first day of each year's Ramadan
    for year in range(2022, 2032):
        start_date = df_religious_final[(df_religious_final['date'].str.contains(str(year))) &
                                        (df_religious_final['Ramadan Feast'] == 1)].index[0]
        start_idx = df_religious_final.index.get_loc(start_date)
        df_religious_final.loc[start_idx + 1:start_idx + 2, 'Ramadan Feast'] = 1

    # Set 1 in the Sacrifice Feast column for the three days following the first day of each year's Sacrifice Feast
    for year in range(2022, 2032):
        start_date = df_religious_final[(df_religious_final['date'].str.contains(str(year))) &
                                        (df_religious_final['Sacrifice Feast'] == 1)].index[0]
        start_idx = df_religious_final.index.get_loc(start_date)
        df_religious_final.loc[start_idx + 1:start_idx + 3, 'Sacrifice Feast'] = 1

    #######################################################################
    ## Note:
    ## The Hijri calendar is a lunar calendar, so its year is about 11-12 days shorter than the Gregorian calendar.
    ## As a result, the Ramadan month shifts earlier in the Gregorian calendar each year.
    ## Approximately every 32 years, Ramadan aligns with the same dates.
    #######################################################################

    # Label the 30 days before each year's Kurban Bayramı as fasting (Fasting)
    df_religious_final["Fasting"] = 0
    for year in range(2022, 2032):
        start_date = df_religious_final[(df_religious_final['date'].str.contains(str(year))) &
                                        (df_religious_final['Ramadan Feast'] == 1)].index[0]
        start_idx = df_religious_final.index.get_loc(start_date)

        if str(year) == "2023":
            df_religious_final.loc[start_idx - 29:start_idx - 1, 'Fasting'] = 1
        else:
            df_religious_final.loc[start_idx - 30:start_idx - 1, 'Fasting'] = 1

    # Convert the 'date' column to datetime format
    df_religious_final['date'] = pd.to_datetime(df_religious_final['date'])

    ####################################################################
    ############## CREATE NON-RELIGIOUS DATAFRAME #####################
    ####################################################################

    # Dictionary containing the names and dates of secular holidays
    holidays = {
        'New Year\'s Day': '01-01',
        'National Sovereignty and Children\'s Day': '04-23',
        'Labour Day': '05-01',
        'Youth and Sports Day': '05-19',
        'Democracy and National Unity Day': '07-15',
        'Victory Day': '08-30',
        'Republic Day': '10-29'
    }

    # Generate dates between 2022-01-01 and 2031-12-31
    dates = pd.date_range(start='2022-01-01', end='2031-12-31')

    # Create an empty DataFrame
    df_without_religious = pd.DataFrame(index=dates)

    # Add secular holidays to the DataFrame
    for holiday, date in holidays.items():
        df_without_religious[holiday] = (df_without_religious.index.strftime('%m-%d') == date).astype(int)

    # Perform one-hot encoding
    df_without_religious_encoded = pd.get_dummies(df_without_religious, prefix='', prefix_sep='')

    # Reset the index
    df_without_religious_encoded = df_without_religious_encoded.reset_index()

    # Rename the 'index' column to 'date'
    df_without_religious_encoded = df_without_religious_encoded.rename(columns={"index": "date"})

    # Merge religious and non-religious holiday DataFrames
    df_holidays_final = df_without_religious_encoded.merge(df_religious_final)
    df_holidays_final = df_holidays_final.rename(columns={"date": "ds"})
    return df_holidays_final
