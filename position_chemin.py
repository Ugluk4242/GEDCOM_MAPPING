def position_chemin(lon_i,lat_i,lon_f,lat_f, pourcentage):
    lon_t = lon_i + (lon_f-lon_i)*pourcentage
    lat_t = lat_i + (lat_f-lat_i)*pourcentage
    return lon_t,lat_t