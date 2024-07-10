def travel_position(lon_i, lat_i, lon_f, lat_f, percentage):
    lon_t = lon_i + (lon_f-lon_i)*percentage
    lat_t = lat_i + (lat_f-lat_i)*percentage
    return lon_t, lat_t