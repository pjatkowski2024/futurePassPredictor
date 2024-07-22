#!/bin/bash
# get the current TLE data and save locally so that we don't overload the TLE server and get blocked.
curl -o noaa.txt https://celestrak.org/NORAD/elements/weather.txt
