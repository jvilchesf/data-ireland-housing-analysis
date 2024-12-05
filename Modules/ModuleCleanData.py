# Import the pandas library for data manipulation and analysis
import pandas as pd

# Configure pandas to display all columns when printing a DataFrame
pd.set_option('display.max_columns', None)

# Function to clean and process the Rent dataset
def CleanDataRent(dfRent):
    # Rename columns to make them more concise and consistent
    dfRent = dfRent.rename(columns={
        'Number of Bedrooms': 'Number_of_bedrooms',  # Replace spaces with underscores
        'Property Type': 'Property_Type',
        'VALUE': 'Price'
    })

    # Drop unnecessary columns that are not relevant for the analysis
    dfRent = dfRent.drop(columns=['STATISTIC Label', 'UNIT'])

    # Define a condition to clean rows with unwanted or null values in the dataset
    # Remove rows where 'Number_of_bedrooms' or 'Property_Type' contains unwanted values
    indexDropRentBed = dfRent[
        (dfRent['Number_of_bedrooms'] != 'All bedrooms') |  # Exclude "All bedrooms" rows
        (dfRent['Property_Type'] != 'All property types')   # Exclude "All property types" rows
    ].index

    # Remove rows where 'Price' is empty while other key fields have valid values
    indexDropRentPrice = dfRent[
        (dfRent['Price'] == '') &                              # Empty price
        (dfRent['Year'].notnull()) &                          # Valid year
        (dfRent['Location'].notnull()) &                      # Valid location
        (dfRent['Number_of_bedrooms'] == 'All bedrooms') &    # All bedrooms specified
        (dfRent['Property_Type'] == 'All property types')     # All property types specified
    ].index

    # Drop the identified rows from the DataFrame
    dfRent = dfRent.drop(indexDropRentBed)
    dfRent = dfRent.drop(indexDropRentPrice)

    # Group the data by 'Number_of_bedrooms' and 'Property_Type', summing up the 'Price' column
    df_group = dfRent.groupby(['Number_of_bedrooms', 'Property_Type'])['Price'].sum()

    # Return the cleaned Rent DataFrame
    return dfRent

# Function to clean and process the Census dataset
def CleanDataCens(dfCensus):
    # Group the dataset by 'UNI' and sum the 'Male' column (example, might be placeholder logic)
    df_group = dfCensus.groupby(['UNI'])['Male'].sum()

    # Drop unnecessary columns that are not relevant for the analysis
    dfCensus = dfCensus.drop(columns=['STATISTIC', 'Statistic', 'TLIST(A1)', 'UNI'])

    # Rename columns to make them more meaningful and consistent
    dfCensus = dfCensus.rename(columns={
        'C02779V03348': 'CensusCountyIndex',  # Rename unclear column to a meaningful name
        'Male': 'CensusMale',
        'Female': 'CensusFemale',
        'Both sexes': 'CensusBothSex',
        'CensusYear': 'Year'
    })

    # Parse the 'CensusBothSex', 'CensusMale', and 'CensusFemale' columns as integers,
    # filling null values with 0 before conversion
    dfCensus['CensusBothSex'] = dfCensus['CensusBothSex'].fillna(0).astype('int64')
    dfCensus['CensusMale'] = dfCensus['CensusMale'].fillna(0).astype('int64')
    dfCensus['CensusFemale'] = dfCensus['CensusFemale'].fillna(0).astype('int64')

    # Group the data by 'Year' and 'County', summing up the 'CensusBothSex' column
    censusGroup = dfCensus.groupby(['Year', 'County'])['CensusBothSex'].sum()

    # Return the cleaned Census DataFrame
    return dfCensus
