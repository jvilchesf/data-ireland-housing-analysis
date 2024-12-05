# Import necessary libraries
import requests  # For making HTTP requests to web APIs
import pandas as pd  # For data manipulation and analysis

# Function to classify a location as 'City' or 'County' based on its format
def cityCountMark(row):
    # Check if the 'Location' contains a comma or a space
    if ',' in row['Location'] or ' ' in row['Location']:
        return 'City'
    else:
        return 'County'

# Function to standardize the 'Location' field
def updateLocation(row):
    # If 'Location' contains a comma or a space, return it as is
    if ',' in row['Location'] or ' ' in row['Location']:
        return row['Location']
    else:
        # Otherwise, append ' County' to the 'Location'
        return row['Location'].split(' ')[0] + ' County'

# Function to retrieve geographic coordinates (latitude and longitude) for a given location
def get_coordinates(location):
    try:
        # Send a GET request to the Nominatim API with the location query
        response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={location}")
        # Parse the JSON response
        location_data = response.json()

        # If data is returned, extract latitude and longitude
        if location_data:
            return (location_data[0]['lat'], location_data[0]['lon'])
        else:
            # Return None if the location is not found
            return (None, None)
    except Exception as e:
        # Print any errors that occur during the request
        print(f"Error occurred: {e}")
        # Return None in case of an error
        return (None, None)

# Function to add standardized location information and geographic coordinates to the DataFrame
def add_location(dfRent):
    # Create a new column 'State/Province' initialized with 'Location' values
    dfRent['State/Province'] = dfRent['Location']
    # Initialize 'cityCountMark' column to store 'City' or 'County' classification
    dfRent['cityCountMark'] = ''

    # Iterate over each row in the DataFrame
    for index, row in dfRent.iterrows():
        County = row['State/Province']
        # If 'State/Province' contains a comma, split and take the second part
        if ',' in County:
            dfRent.at[index, 'State/Province'] = County.split(',')[1].strip()
        else:
            # Otherwise, split by space and take the first part
            dfRent.at[index, 'State/Province'] = County.split(' ')[0]

    # Append ' County' to 'State/Province' values
    dfRent['State/Province'] = dfRent['State/Province'] + ' County'
    # Apply 'cityCountMark' function to classify each location
    dfRent['cityCountMark'] = dfRent.apply(cityCountMark, axis=1)
    # Update 'Location' field using 'updateLocation' function
    dfRent['Location'] = dfRent.apply(updateLocation, axis=1)
    # Set 'Country' field to 'Ireland'
    dfRent['Country'] = 'Ireland'

    # Group by 'Location' and sum the 'Price' column
    dfRent_location = dfRent.groupby(['Location'])['Price'].sum().reset_index()
    # Apply 'get_coordinates' function to retrieve latitude and longitude for each location
    dfRent_location['Coordinates'] = dfRent_location['Location'].apply(get_coordinates)
    # Split 'Coordinates' into separate 'Latitude' and 'Longitude' columns
    dfRent_location[['Latitude', 'Longitude']] = pd.DataFrame(dfRent_location['Coordinates'].tolist(),
                                                              index=dfRent_location.index)

    # Merge the coordinates back into the original DataFrame
    dfRent = dfRent.merge(dfRent_location[['Location', 'Coordinates', 'Latitude', 'Longitude']], on='Location',
                          how='left')

    # Return the updated DataFrame
    return dfRent
