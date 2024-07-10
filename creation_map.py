# This script uses the diplacement file built with displacement_finder.py and maps the data for each frame of the animation.

# 0. Packages
import cartopy.crs as ccrs # Mapping tool
import cartopy
import geopandas as gpd
import matplotlib.pyplot as plt # Plotting tool
import matplotlib
matplotlib.use('TkAgg')
import pickle
from datetime import timedelta
import datetime
import travel_position
import cartopy.feature as cfeature
import matplotlib.image as mpimg

# Downloading the displacement data
with open('displacements.pkl','rb') as f:
    d1, d2, lat1, lon1, lat2, lon2, sexe, pays1 = pickle.load(f)

# Time of first frame. Change according to your data.
start_date = datetime.datetime(1610, 1, 1, 0, 0)
date = start_date

# Time of last frame
end_date = max(d2)

# Counter to name each frame
counter = 0

# Time between each frame, in days. Only for the first frame. Afterwards it changes according to the number of living ancestors.
timestep = 60

# I use this to pan the camera on a specific area at a chosen year. Change it according to your data.
zoom_dict = {
    (-120, 1, -1, 90): 1610,
    (-75, 41, -63, 49.5): 1635,
    (-75, 41, -63, 49.5000000001): 1735,
    (-75, 43.75, -68.5, 49): 1765,
    (-75, 43.75, -68.5, 49.0000001): 2034
}

# Loop through entire time interval
while date < end_date:
        # Frame date
        date = date + datetime.timedelta(timestep)

        # Loop progress
        print(date)

        # Initializing the coordinates of the dots and the flags in this frame
        lat_p = []
        lon_p = []
        sexe_p = []
        lon_flag = []
        lat_flag = []
        flag = []

        # Find every ancestor alive on the date of this frame
        for t in range(len(d1)):
            if d1[t] <= date <= d2[t]:
                # This ancestor was alive, find the % of progress between the departure and arrival
                if d2[t] - d1[t] == timedelta(0):
                    pourcentage = 1
                else:
                    pourcentage = (date - d1[t])/(d2[t] - d1[t])

                # With the coordinates and the percentage, find the coordinates between the 2 locations (linear interpolation)
                lon_t, lat_t = travel_position.travel_position(lon1[t], lat1[t], lon2[t], lat2[t], pourcentage)

                # Add to list
                lat_p.append(lat_t)
                lon_p.append(lon_t)
                sexe_p.append(sexe[t])

                # Criteria for adding a flag. These are the values for my project, to show the flags of people coming from Europe
                if lon_t > -70 and lon_t < 10 and pays1[t] != 'Canada' and pays1[t] != 'United States':
                    # Flag location, close to dot
                    lon_flag.append(lon_t)
                    lat_flag.append(lat_t)
                    # Country name
                    if pays1[t] == 'België / Belgique / Belgien':
                        pays1[t] = 'Belgium'
                    if pays1[t] == 'Schweiz/Suisse/Svizzera/Svizra':
                        pays1[t] = 'Switzerland'
                    flag.append(pays1[t])
            else:
                continue

        # Number of ancestors
        nb_ancestor = len(lat_p)
        print('Number of living ancestors = ')
        print(nb_ancestor)

        # I used this to decelarate the animation when there are a lot of ancestors on the map, and accelarate when there are less.
        timestep = round(1400*0.99**nb_ancestor)+60
        print('Length of timestep for next frame = ')
        print(timestep)

        # Make plot for this timeframe
        fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})

        # This is not very optimal. It's used to get the coordinates of the camera between 2 dates given in zoom_dict. 
        # It makes the camera transition smoother.
        min_diff_negative = datetime.timedelta(999999999)
        min_diff_positive = datetime.timedelta(999999999)

        for coords, year in zoom_dict.items():
            diff = date - datetime.datetime(year,1,1)
            if diff <= datetime.timedelta(0):
                if abs(diff) < min_diff_negative:
                    min_diff_negative = diff
                    year2 = year
                    minx2, miny2, maxx2, maxy2 = coords
            else:
                if diff < min_diff_positive:
                    min_diff_positive = diff
                    year1 = year
                    minx1, miny1, maxx1, maxy1 = coords

        progress = (date - datetime.datetime(year1,1,1))/(datetime.datetime(year2,1,1)-datetime.datetime(year1,1,1))

        minx = minx1 + progress*(minx2-minx1)
        maxx = maxx1 + progress*(maxx2-maxx1)
        miny = miny1 + progress*(miny2-miny1)
        maxy = maxy1 + progress*(maxy2-maxy1)

        # Coordinates where the current year will appear
        date_x = minx + (maxx-minx)*0.80
        date_y = miny + (maxy-miny)*0.05

        # Limit the map to the zoom we just calulated
        ax.set_extent([minx, maxx, miny, maxy])

        # Terrain background
        ax.add_feature(cfeature.NaturalEarthFeature(
            category='physical',
            name='land',
            scale='10m',
            edgecolor='face',
            facecolor=cfeature.COLORS['land']
        ))

        # Ocean background
        ax.add_feature(cfeature.NaturalEarthFeature(
            category='physical',
            name='ocean',
            scale='10m',
            edgecolor='none',
            facecolor=cfeature.COLORS['water']
        ))

        # Rivers, lakes and borders
        ax.add_feature(cartopy.feature.RIVERS, edgecolor='black', linewidth=0.1)
        ax.add_feature(cartopy.feature.LAKES, edgecolor='black', linewidth=0)
        ax.add_feature(cartopy.feature.BORDERS, linewidth=0.2)

        # Plotting each dot, the color depends on the gender
        for p in range(len(lat_p)):
            if sexe_p[p] == 'M':
                # Men
                m = ax.plot(lon_p[p], lat_p[p],
                            color=(1 / 255, 166 / 255, 234 / 255), linestyle="None", marker='o', markersize=8.7,
                            markeredgewidth=1.6, markeredgecolor='black', transform=ccrs.PlateCarree())
            elif sexe_p[p] == 'F':
                # Women
                f = ax.plot(lon_p[p], lat_p[p],
                            color=(255 / 255, 177 / 255, 203 / 255), linestyle="None", marker='o', markersize=8.7,
                            markeredgewidth=1.6, markeredgecolor='black', transform=ccrs.PlateCarree())

        # Adding flags above some dots
        width_flag = 0.007*(maxx-minx)
        height_flag = 0.0095*(maxy-miny)
        for g in range(len(lat_flag)):
            path = 'C:/Users/Edward/PycharmProjects/GENEALOGY_MAP/flags/flag' + flag[g] + '.jpeg'
            img = mpimg.imread(path)
            ax.imshow(img, origin='lower',
                      extent=(lon_flag[g] - width_flag/2, lon_flag[g] + width_flag/2, lat_flag[g] + height_flag*1.05, lat_flag[g] + height_flag*2),
                      transform=ccrs.PlateCarree(), zorder=10)

        # Text showing the year
        ax.text(date_x, date_y, f"{date.strftime('%Y')}", fontsize=50, ha='center', color='black')

        # Text showing the legend (colors for men and women)
        l1 = ax.plot(minx + 0.04*(maxx-minx), miny + 0.09*(maxy-miny),
                     color=(255 / 255, 177 / 255, 203 / 255), linestyle="None", marker='o', markersize=8.7,
                            markeredgewidth=1.6, markeredgecolor='black', transform=ccrs.PlateCarree())

        l2 = ax.plot(minx + 0.04*(maxx-minx), miny + 0.05*(maxy-miny), color=(1 / 255, 166 / 255, 234 / 255), linestyle="None", marker='o', markersize=8.7,
                            markeredgewidth=1.6, markeredgecolor='black', transform=ccrs.PlateCarree())

        ax.text(minx + 0.06*(maxx-minx), miny + 0.0845*(maxy-miny),'Woman',fontsize=15, ha='left', color='black')
        ax.text(minx + 0.06*(maxx-minx), miny + 0.0438*(maxy-miny), 'Man', fontsize=15, ha='left', color='black')

        # Forgot what this does...
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # Saving the map in sub folder 'frames'
        fig.savefig('/frames/frame_' + str(counter) + '.png', dpi=175, transparent=True, facecolor='black')
        plt.close(fig)

        counter = counter + 1