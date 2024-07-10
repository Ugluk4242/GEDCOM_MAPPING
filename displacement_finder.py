import time  # This script is used to parse the GEDCOM file that contains the genealogical data
        # The ancestors of a chosen individual are listed and information is gathered on the time and place
        # of their birth, marriages and death. Each time enough data is available on 2 events of a person's life, a displacement
        # is obtained. This will define the trajectory and timing of a dot on the final map.

        #0. Packages
from gedcom.element.individual import IndividualElement # Parsing of gedcom file
from gedcom.parser import Parser

from geopy.geocoders import Nominatim # Find lat/lon of a city

import pickle
from datetime import date

from time_modification import time_modification # custom function used to read the time of an event
from city_modification import city_modification # custom function to change city names that are not recognized by the geopy tool

        #1. Parsing of the data

# Path to your `.ged` file. GEDCOM files are a very common way to store genealogical data
file_path = 'my_genealogy.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()

# Initialize the geopy tool, account needed on the site
geolocator = Nominatim(user_agent="ACCOUNT_NAME", timeout=3)

# Find the person for which you want to map the ancestors
# You might want to check that a person with the same name is not chosen instead of the one you mean
first_name = "FIRST_NAME"
last_name = "LAST_NAME"
for element in root_child_elements:
    if isinstance(element, IndividualElement):
        if element.surname_match(last_name):
            # Unpack the name tuple
            (first, last) = element.get_name()
            if first == first_name and last == last_name:
               break

# Get the list of all the ancestors of the chosen individual
ancestors = gedcom_parser.get_ancestors(element)

        #2. Getting the info on each displacement

# List of displacements, the info in each element of the list is:
# Gender, Departure time, Departure place, Arrival time, Arrival place
displacement = []

# Unique individuals, to prevent the same ancestor from different branch of the tree to appear several times on the map
ele = []

for element in ancestors:
    if element.get_pointer() in ele:
        continue
    else:
        ele.append(element.get_pointer())

    # Birth: place and time
    birth = element.get_birth_data()

    # List of weddings, with date and time
    mariages = gedcom_parser.get_marriages(element)

    # Death: place and time
    death = element.get_death_data()

    # Keeping track of the loop progression
    (first, last) = element.get_name()
    print(first + ' ' + last)

    # Data available from birth to first wedding? If so, new displacement.
    if len(birth) > 0 and len(mariages) > 0:
        if len(birth[0]) > 0 and len(birth[1]) > 0 and len(mariages[0][0]) > 0 and len(mariages[0][1]) > 0:
            displacement.append([element.get_gender(), birth[0], birth[1], mariages[0][0], mariages[0][1]])

    # Data available from wedding to wedding? If so, new displacement.
    for nb_mariage in range(len(mariages)-1):
        if len(mariages[nb_mariage][0]) > 0 and len(mariages[nb_mariage][1]) > 0 and len(mariages[nb_mariage+1][0]) > 0 and len(mariages[nb_mariage+1][1]) > 0:
            displacement.append([element.get_gender(), mariages[nb_mariage][0], mariages[nb_mariage][1], mariages[nb_mariage+1][0], mariages[nb_mariage+1][1]])

    # Data available from last wedding to death? If so, new displacement.
    if len(mariages) > 0 and element.is_deceased():
        if len(mariages[len(mariages)-1][0]) > 0 and len(mariages[len(mariages)-1][1]) > 0 and len(death[0]) > 0 and len(death[1]) > 0:
            displacement.append([element.get_gender(), mariages[len(mariages)-1][0], mariages[len(mariages)-1][1], death[0], death[1]])

    # Data available from birth to death without enough wedding data? If so, new displacement.
    if len(birth[0]) > 0 and element.is_deceased():
        if len(birth[0]) > 0 and len(birth[1]) > 0 and len(death[0]) > 0 and len(death[1]) > 0:
            if len(mariages) > 0:
                if len(mariages[0][0]) > 0 and len(mariages[0][1]) > 0:
                    continue
                else:
                    displacement.append([element.get_gender(), birth[0], birth[1], death[0], death[1]])
            else:
                displacement.append([element.get_gender(), birth[0], birth[1], death[0], death[1]])

# Manually adding displacements (I used this for the living individuals, but could be used for additional displacements in an ancestor's live)
D = date.today()
D = D.strftime("%d %b %Y")

# Example:
displacement.append(['F', '12 MAY 1962', 'Waterville, Estrie', '12 MAY 1967', 'Sherbrooke, Estrie'])


        #3. Transformation of the displacement data to make it mapable

# Initializing the departure and arrival time vectors
d1 = []
d2 = []

# Initializing the departure and arrival latitude vectors
lat1 = []
lat2 = []

# Initializing the departure and arrival longitude vectors
lon1 = []
lon2 = []

# Initializing the sex vector (for the dot color)
sex = []

# Initializing the country of origin vector (for the flags)
pays1 = []

# Change the time in datetime and the city in lat/lon

dict_lat = {}
dict_lon = {}
dict_pays = {}

# 'modification_temps' takes the time of an event and transforms it into a datetime variable
# a few cases are covered (exact date available, 'ABOUT' year X, 'BEFORE' year X, etc.)

for d in displacement:

    # Commented for first run, but since the geolocation takes a while I save the information and load it afterwards.

    #with open('dict_lat.pkl', 'rb') as pickle_file:
    #    dict_lat = pickle.load(pickle_file)

    #with open('dict_lon.pkl', 'rb') as pickle_file:
    #    dict_lon = pickle.load(pickle_file)

    #with open('dict_country.pkl', 'rb') as pickle_file:
    #   dict_pays = pickle.load(pickle_file)

    # Sex of the moving individual
    sex.append(d[0])

    # Date 1
    time_str = d[1]
    d1.append(time_modification(time_str))

    # Date 2
    time_str = d[3]
    d2.append(time_modification(time_str))

    # Lat/Lon of departure place already geolocated? If not, geolocate it.
    # If the geolocation doesnt work or gives the wrong place, the modification_ville function can be used
    # to change a location string to another that will work
    if d[2] not in dict_lat:
        dm = city_modification(d[2])
        location1 = geolocator.geocode(dm)
        time.sleep(2)
        # Saving the info to prevent calling geolocator for the same place over and over
        dict_lat[d[2]] = location1.latitude
        dict_lon[d[2]] = location1.longitude
        # To get the country of departure
        location = geolocator.reverse(str(location1.latitude) + "," + str(location1.longitude))
        time.sleep(2)
        address = location.raw['address']
        country = address.get('country', '')
        # And to save it
        dict_pays[d[2]] = country
        print(location1)

    # Adding to list
    lat1.append(dict_lat[d[2]])
    lon1.append(dict_lon[d[2]])
    pays1.append(dict_pays[d[2]])

    # Lat/Lon of arrival place already geolocated? If not, geolocate it.
    if d[4] not in dict_lat:
        dm = city_modification(d[4])
        location2 = geolocator.geocode(dm)
        time.sleep(3)
        # Saving the info to prevent calling geolocator for the same place over and over
        dict_lat[d[4]] = location2.latitude
        dict_lon[d[4]] = location2.longitude
        # To get the country of arrival
        location = geolocator.reverse(str(location2.latitude) + "," + str(location2.longitude))
        time.sleep(3)
        address = location.raw['address']
        country = address.get('country', '')
        # And to save it
        dict_pays[d[4]] = country
        print(location2)

    # Adding to list
    lat2.append(dict_lat[d[4]])
    lon2.append(dict_lon[d[4]])

    with open('dict_lat.pkl', 'wb') as f:
        pickle.dump(dict_lat, f)

    with open('dict_lon.pkl', 'wb') as f:
        pickle.dump(dict_lon, f)

    with open('dict_country.pkl', 'wb') as f:
        pickle.dump(dict_pays, f)

# Saving the list of displacements in a pickle file:
with open('displacements.pkl', 'wb') as f:
    pickle.dump([d1, d2, lat1, lon1, lat2, lon2, sex, pays1], f)