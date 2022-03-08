        # This script is used to parse the GEDCOM file that contains the genealogical data
        # The ancestors of a chosen individual are listed and information is gathered on the time and place
        # of their birth, marriages and death. Each time enough data is available on 2 events of a person's life, a displacement
        # is obtained. This will define the trajectory and timing of a dot on the final map.

        #0. Packages
from gedcom.element.individual import IndividualElement # Parsing of gedcom file
from gedcom.parser import Parser

from geopy.geocoders import Nominatim # Find lat/lon of a city

import pickle
from datetime import date

from modification_temps import modification_temps # custom function used to read the time of an event
from modification_ville import modification_ville # custom function to change city names that are not recognized by the geopy tool

        #1. Parsing of the data

# Path to your `.ged` file. GEDCOM files are a very common way to store genealogical data
file_path = 'path_to_your_gedcom_file_here.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)
root_child_elements = gedcom_parser.get_root_child_elements()

# Initialize the geopy tool, account needed on the site
geolocator = Nominatim(user_agent= "insert username here",timeout=3)

# Find the person for which you want to map the ancestors
# You might want to check that a person with the same name is not chosen instead of the one you mean
first_name = "Jane"
last_name = "Doe"
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
deplacement = []

# Unique individuals, to prevent the same ancestor from different branch of the tree to appear several times on the map
ele = []

for element in ancestors:
    if element.get_pointer() in ele:
        continue
    else:
        ele.append(element.get_pointer())

    # Birth place and time
    naissance = element.get_birth_data()

    # List of weddings, with date and time
    marriages = gedcom_parser.get_marriages(element)

    # Death place and time
    deces = element.get_death_data()

    # Keeping track of the loop progression
    (first, last) = element.get_name()
    print(first + ' ' + last)

    # Data available from birth to first wedding? If so, new displacement.
    if len(naissance) > 0 and len(marriages) > 0:
        if len(naissance[0]) > 0 and len(naissance[1]) > 0 and len(marriages[0][0]) > 0 and len(marriages[0][1]) > 0:
            deplacement.append([element.get_gender(),naissance[0],naissance[1],marriages[0][0],marriages[0][1]])

    # Data available from wedding to wedding? If so, new displacement.
    for nb_marriage in range(len(marriages)-1):
        if len(marriages[nb_marriage][0]) > 0 and len(marriages[nb_marriage][1]) > 0 and len(marriages[nb_marriage+1][0]) > 0 and len(marriages[nb_marriage+1][1]) > 0:
            deplacement.append([element.get_gender(),marriages[nb_marriage][0],marriages[nb_marriage][1],marriages[nb_marriage+1][0],marriages[nb_marriage+1][1]])

    # Data available from last wedding to death? If so, new displacement.
    if len(marriages) > 0 and element.is_deceased():
        if len(marriages[len(marriages)-1][0]) > 0 and len(marriages[len(marriages)-1][1]) > 0 and len(deces[0]) > 0 and len(deces[1]) > 0:
            deplacement.append([element.get_gender(),marriages[len(marriages)-1][0],marriages[len(marriages)-1][1], deces[0], deces[1]])

    # Data available from birth to death without enough wedding data? If so, new displacement.
    if len(naissance[0]) > 0 and element.is_deceased():
        if len(naissance[0]) > 0 and len(naissance[1]) > 0 and len(deces[0]) > 0 and len(deces[1]) > 0:
            if len(marriages) > 0:
                if len(marriages[0][0]) > 0 and len(marriages[0][1]) > 0:
                    continue
                else:
                    deplacement.append([element.get_gender(), naissance[0],naissance[1],deces[0], deces[1]])
            else:
                deplacement.append([element.get_gender(), naissance[0],naissance[1], deces[0],deces[1]])

# Manually adding displacements (I used this for the living individuals)
D = date.today()
D = D.strftime("%d %b %Y")
# exemple: deplacement.append(['F','12 MAY 1962','Waterville, Estrie',D,'Sherbrooke, Estrie'])

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
sexe = []

# Initializing the country of origin vector (for the flags)
pays1 = []

# Dictionnaries containing the coordinates and country of cities to lower Nominatim queries
dict_lat = {}
dict_lon = {}
dict_pays = {}

# Change the time in datetime and the city in lat/lon

# 'modification_temps' takes the time of an event and transforms it into a datetime variable
# a few cases are covered (exact date available, 'ABOUT' year X, 'BEFORE' year X, etc.)

for d in deplacement:
    # Loop progress
    print(d)

    # Gender of the moving individual
    sexe.append(d[0])

    # Date 1
    time_str = d[1]
    d1.append(modification_temps(time_str))

    # Date 2
    time_str = d[3]
    d2.append(modification_temps(time_str))

    # Lat/Lon of departure place already geolocated? If not, geolocate it.
    # If the geolocation doesnt work or gives wrong place, the modification_ville function can be used
    # to change a location string to another that will work
    if d[2] not in dict_lat:
        dm = modification_ville(d[2])
        location1 = geolocator.geocode(dm)
        # Saving the info to prevent calling geolocator for the same place over and over
        dict_lat[d[2]] = location1.latitude
        dict_lon[d[2]] = location1.longitude
        # To get the country of departure
        location = geolocator.reverse(str(location1.latitude) + "," + str(location1.longitude))
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
        dm = modification_ville(d[4])
        location2 = geolocator.geocode(dm)
        # Saving the info to prevent calling geolocator for the same place over and over
        dict_lat[d[4]] = location2.latitude
        dict_lon[d[4]] = location2.longitude
        # To get the country of arrival
        location = geolocator.reverse(str(location2.latitude) + "," + str(location2.longitude))
        address = location.raw['address']
        country = address.get('country', '')
        # And to save it
        dict_pays[d[4]] = country
        print(location2)

    # Adding to list
    lat2.append(dict_lat[d[4]])
    lon2.append(dict_lon[d[4]])

# Saving the list of displacements in a pickle file:
with open('deplacements.pkl', 'wb') as f:
    pickle.dump([d1, d2, lat1, lon1, lat2, lon2, sexe, pays1], f)