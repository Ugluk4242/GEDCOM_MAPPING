# GEDCOM_MAPPING
Python scripts to map the migration of ancestors from a GEDCOM file

INTRO:
        This project is in two parts because I couldnt make all the packages work with one single interpreter.

        I used:
        - Python 3.9 - PyCharm for Part 1
        - Python 3.9 - Anaconda 3 for Part 2

        I'm sure someone more experienced could make it work but I am a rookie!
        
PART 1:
        Parses the GEDCOM file, finds the ancestors of an individual and tracks the time and place of birts, weddings and deaths.
        
        1. 'displacement_finder.py' is the main script. Run this to produce the list of displacements.
        2. 'modification_ville.py' changes the names of the cities you want. It's filled with mine to give you an exemple. It's needed because the geolocator tool didnt recognize some city names.
        3. 'modification_temps.py' changes the time of the events to datetime. For exemple, 'ABT 1754' turns into a datetime with a random day close to 1754.
        
PART 2:
        Makes the map at different timesteps using the displacements from Part 1.
        
        1. 'map_creation.py' is the main script. It generates and saves an image at each timestep.
        2. 'position_chemin.py' is used to obtain the coordinates between two locations and a percentage of progress between the two.
        
