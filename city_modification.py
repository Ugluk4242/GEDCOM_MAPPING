# Used to change the name of cities that do not exist anymore or that the geolocator tool had difficulty finding

def city_modification(d):
    # Example:
    if 'Port-Royal' in d:
        d = 'Annapolis Royal, Nouvelle-Écosse'
    return d