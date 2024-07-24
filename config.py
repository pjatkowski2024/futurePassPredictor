#!/usr/bin/python3
import sys
from pathlib import Path

if __name__ == '__main__':
    print("Can't run this file")
    sys.exit()

import yaml
import io
from satelllite import Satellite
from orbit_predictor.locations import Location


# Config objects
satellites = list()
tle_update_interval = int()
location = 0
output_dir = str()
html_file = str()
html_elev_green_threshold = int()
html_elev_yellow_threshold: int()
maximum_overlap = 0
# RSS config
rss_enabled = bool()
rss_port = int()
rss_webserver = bool()
tle_file = str()


# Post-Processing hook config
post_processing_hook_command = str()
post_processing_hook_enabled = bool()
post_processing_hook_foreach = bool()

def loadConfig(basedir, verbose=True):
    global satellites, tle_file, tle_update_interval, location, output_dir, rss_enabled, rss_port, rss_webserver, post_processing_hook_command, post_processing_hook_enabled, post_processing_hook_foreach, maximum_overlap
    global html_file, html_elev_green_threshold, html_elev_yellow_threshold
    # Open config file relative to the base directory
    file = Path(str(basedir) + '/config.yaml').expanduser()
    f = io.open(file, mode="r", encoding="utf-8")

    # Parse it
    config = yaml.load(f, Loader=yaml.FullLoader)
    # open the tle file from the correct directory
    tle_file = Path(str(basedir) + '/' + config["config"]["tle_file"] ).expanduser()
    if verbose:
        print("TLE FILE: "+str(tle_file))
    html_file = str(  Path(config["config"]["html_output_file"]).expanduser())
    if verbose:
        print('html output file: '+ str(html_file))

    html_elev_green_threshold = int(config["config"]["html_elev_green_threshold"])
    html_elev_yellow_threshold = int(config["config"]["html_elev_yellow_threshold"])


    # Software options
    tle_update_interval = int(config["config"]["tle_update_interval"])
    output_dir = Path((config["config"]["output_dir"])).expanduser()
    #print("OUTPUT DIR:"+ str(output_dir))
    maximum_overlap = int(config["config"]["max_overlap"])

    # RSS
    rss_enabled = bool(config["config"]["rss"]["enabled"])
    rss_webserver = bool(config["config"]["rss"]["webserver"])
    rss_port = int(config["config"]["rss"]["port"])

    # Post-Processing Hook
    post_processing_hook_command = str(config["config"]["post_processing_hook"]["command"])
    post_processing_hook_enabled = bool(config["config"]["post_processing_hook"]["enabled"])
    post_processing_hook_foreach = bool(config["config"]["post_processing_hook"]["run_foreach"])
    if verbose:
        print("TLE Update interval : " + str(tle_update_interval) + " hour(s)")
        print('\n')

    # Ground station
    latitude = config["config"]["station"]["latitude"]
    longitude = config["config"]["station"]["longitude"]
    elevation = config["config"]["station"]["elevation"]
    if verbose:
        print("Groud station :")
        print("    Latitude     : " + str(latitude))
        print("    Longitude    : " + str(longitude))
        print("    Elevation    : " + str(elevation))
        print('\n')
    location = Location("Station", latitude, longitude, elevation)

    # Load satellites
    for sat in config["satellites"]:
        name = sat["name"]
        norad = sat["norad"]
        priority = sat["priority"]
        min_elevation = sat["min_elevation"]
        frequency = sat["frequency"]
        downlink = sat["downlink"]
        delete_processed_files = sat["delete_processed_files"]
        if verbose:
            print("Adding " + name + " :")
            print("     NORAD                   : " + str(norad))
            print("     Priority                : " + str(priority))
            print("     Minimum elevation       : " + str(min_elevation))
            print("     Frequency               : " + str(frequency))
            print("     Downlink type           : " + downlink)
            print("     Delete processed files  : " + str(delete_processed_files))
        satellite = Satellite(name, norad, priority, min_elevation, frequency, downlink, delete_processed_files)
        satellites.append(satellite)
    if verbose:
        print('\n')
    