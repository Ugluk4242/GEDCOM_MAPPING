# Part 2: Map mapping using the displacement data
# I used the anaconda 3 interpreter to make this run, couldnt make it work otherwise

# 0. Packages
import cartopy.crs as ccrs # Mapping tool
import cartopy
import cartopy.io.img_tiles as cimgt

import matplotlib.pyplot as plt # Plotting tool
import matplotlib
import pickle

from datetime import datetime, timedelta
from position_chemin import position_chemin # Function to get the position of a dot between 2 points with the % of progress

# Downloading the displacement data
with open('path to picke file here','rb') as f:
    d1, d2, lat1, lon1, lat2, lon2, sexe, pays1 = pickle.load(f)

# Time of first frame
start_date = min(d1)

# Time of last frame
end_date = max(d2)

# Map backgroung
stamen_terrain = cimgt.Stamen('terrain-background')

# IMPORTANT, it hides the plots and clears the memory
# Otherwise, my computer melts
# Commenting these lines during tests is very helpful because otherwise you will not see the map
matplotlib.use('agg')
plt.ioff()

# Counter to name each frame
counter = 0

# Time between each frames, in days
timestep = 75

# Loop through entire time interval
for ii, days in enumerate(range((end_date - start_date).days+1)):
    # Is the number of days divisible by the chosen timestep? If not, skip this frame.
    if days%timestep == 0:

        # Frame date
        date = start_date + timedelta(days)

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
                lon_t, lat_t = position_chemin(lon1[t], lat1[t], lon2[t], lat2[t], pourcentage)

                # Add to list
                lat_p.append(lat_t)
                lon_p.append(lon_t)
                sexe_p.append(sexe[t])

                # Criteria for adding a flag. These are the values for my project, to show the flags of people coming from Europe
                if lon1[t] > -60 and lon_t > -70:
                    # Flag location, close to dot
                    lon_flag.append(lon_t+0.1)
                    lat_flag.append(lat_t)
                    # Country name
                    flag.append(pays1[t])
            else:
                continue

        # Make plot for this timeframe
        fig = plt.figure()

        # Text to show the year
        fontname = 'Open Sans'
        fontsize = 60

        # Axis
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        # This allows changing the focus after a certain date, you will need to change the extent values to focus on a
        # different area for your project and change the zoom at a different time. The text location needs to be changed also.
        if date < datetime(1780,1,1):
            ax.set_extent([-75, -63, 43.4, 48], crs=ccrs.PlateCarree())
            date_x = -64.3
            date_y = 43.6
        else:
            ax.set_extent([-75, -69.4, 44.2, 48], crs=ccrs.PlateCarree())
            date_x = -70.1
            date_y = 44.5

        # Add background, the number is the resolution. The higher the better.
        ax.add_image(stamen_terrain, 8)

        # Adding different features to map
        ax.coastlines(linewidth=1.7)
        ax.add_feature(cartopy.feature.RIVERS, edgecolor='black', linewidth=1.3)
        ax.add_feature(cartopy.feature.LAKES, edgecolor='black', linewidth=1.3)
        ax.add_feature(cartopy.feature.BORDERS, linewidth=2.7)

        # Adding the text to show the year
        ax.text(date_x, date_y,
                f"{date.strftime('%Y')}",
                color='black',
                fontname=fontname, fontsize=fontsize * 1.3,
                transform=ccrs.PlateCarree())

        # Plotting each dot, the color depends on the gender
        for p in range(len(lat_p)):
            if sexe_p[p] == 'M':
                # Men
                m = ax.plot(lon_p[p], lat_p[p],
                        color=(4/255, 55/255, 242/255), linestyle="None", marker='o', markersize=12,
                        markeredgewidth=1.6, markeredgecolor='black',transform=ccrs.PlateCarree())
            elif sexe_p[p] == 'F':
                # Women
                f = ax.plot(lon_p[p], lat_p[p],
                        color=(243/255, 58/255, 106/255), linestyle="None", marker='o', markersize=12,
                        markeredgewidth=1.6, markeredgecolor='black',transform=ccrs.PlateCarree())

        # Adding flags above some dots
        for g in range(len(lat_flag)):
            img = plt.imread('path to saved image of needed flag' + flag[g] + '.png')
            ax.imshow(img, origin='lower', extent=(lon_flag[g]-0.15, lon_flag[g]-0.05, lat_flag[g]+0.08, lat_flag[g]+0.19), transform=ccrs.PlateCarree(),zorder=10)

        # Adding borders
        ax.spines['geo'].set_edgecolor('black')
        ax.spines['geo'].set_linewidth(6)

        # Figure size
        fig.set_size_inches(37, 16)
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        # Saving the map in sub folder 'frames'
        fig.savefig(f"frames/frame_{counter:05d}.png", dpi=175,transparent=True,facecolor='black')
        plt.close(fig)

        counter = counter + 1
