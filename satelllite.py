#!/usr/bin/python3
import sys

from orbit_predictor.sources import get_predictor_from_tle_lines, NoradTLESource
import config

if __name__ == '__main__':
    print("Can't run this file")
    sys.exit()

# Satellite class
class Satellite:
    def __init__(self, name, norad, priority, min_elevation, frequency, downlink, delete_processed_files):
        self.name = name
        self.norad = norad
        self.priority = priority
        self.min_elevation = min_elevation
        self.frequency = frequency
        self.downlink = downlink
        self.delete_processed_files = delete_processed_files
        self.tle_1 = ''
        self.tle_2 = ''

    def getPredictor(self):
        ts = NoradTLESource.from_file(config.tle_file)
        tle = ts._get_tle(str(self.name), None)
        # self.predictor = get_predictor_from_tle_lines((self.tle_1, self.tle_2))
        self.predictor = get_predictor_from_tle_lines((tle))
        return self.predictor

