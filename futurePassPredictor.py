import argparse
from datetime import datetime, timedelta
from pathlib import Path

import dominate
import pytz
from dominate.tags import *

import config

# formats for date/time display
localTimeFormat = '%H:%M:%S'
localDayFormat = '%m/%d/%Y'
localDateTimeFormat = '%m/%d/%Y %H:%M:%S'

print("------------------------------------------------------")
print("            Starting FuturePass Predictor             ")
print("------------------------------------------------------")
print('\n')
parser = argparse.ArgumentParser(description='Process command arguments.')
parser.add_argument('--basedir', default='.',
                    help='i/o base directory, including config file. Defaults to current directory')
args = parser.parse_args()

# use the base directory to find the config.yaml file. If no directory is specified the default
# is the current directory. expanduser allows ~/ to be used for the home directory if desired
baseDir = args.basedir
p = Path(baseDir + '/config.yaml').expanduser()
print("reading config from: " + str(p))

# Parse config
config.loadConfig(baseDir, verbose=False)


# calculate passes starting at now - 12 hours so that recent passes are displayed
passes = list()
startTimeUtc = datetime.utcnow() - timedelta(hours=12)

# Lookup next passes of all satellites
for satellite in config.satellites:
    passCount = 5  # 5 passes per satellite
    predictionStartTime = startTimeUtc
    predictor = satellite.getPredictor()

    while passCount > 0:
        next_pass = predictor.get_next_pass(config.location, when_utc=predictionStartTime,
                                            max_elevation_gt=satellite.min_elevation)
        max_elevation = next_pass.max_elevation_deg
        priority = satellite.priority
        passCount = passCount - 1;
        predictionStartTime = next_pass.los
        # add to list
        passes.append([next_pass, satellite, max_elevation, priority])


# for sorting results by AOS
def getAos(passData):
    [np, sat, maxe, prio] = passData
    return np.aos


# sort list by AOS
sortedPasses = passes.sort(key=getAos)


# print passes, deprecated
def printPasses(passes):
    for current_pass in passes:
        [np, sat, maxe, prio] = current_pass
        aos = np.aos
        los = np.los
        duration = np.duration_s / 60

        aos_aware = aos.replace(tzinfo=pytz.UTC)
        los_aware = los.replace(tzinfo=pytz.UTC)

        aos_local = aos_aware.astimezone().isoformat()
        los_local = los_aware.astimezone().isoformat()

        print("%s maxElev=%.1f freq=%f dur=%.1f min aos=%s los=%s" % (
            sat.name, np.max_elevation_deg, sat.frequency, duration, aos_local, los_local))

# build html document
def htmlPasses(passes):
    strNow = startTimeUtc.replace(tzinfo=pytz.UTC).astimezone().strftime(localDateTimeFormat)
    doc = dominate.document(title='Future Passes as of ' + strNow)
    body = doc.body
    body.add(h1('Future Passes as of ' + strNow))

    t = table()
    t.set_attribute('border', '1px solid')
    t.set_attribute('cellpadding', '3')
    body.add(t)
    tb = tbody()
    t.add(tb)
    h = tr()
    tb.add(h)
    # header row
    h.add(th('Satellite'))
    h.add(th("MaxElev"))
    h.add(th("Frequency"))
    h.add(th("Day"))
    h.add(th("AOS"))
    h.add(th("LOS"))
    h.add(th("Duration"))
    now = datetime.now()
    current_day = now.day

    for current_pass in passes:
        [np, sat, maxe, prio] = current_pass
        aos = np.aos
        los = np.los
        duration = np.duration_s / 60
        # add utc time zone to aos/los so we can display in local time
        aos_aware = aos.replace(tzinfo=pytz.UTC)
        los_aware = los.replace(tzinfo=pytz.UTC)

        aos_local = aos_aware.astimezone().strftime(localTimeFormat)
        los_local = los_aware.astimezone().strftime(localTimeFormat)

        row = tr()
        tb.add(row)
        # header row
        row.add(td(sat.name))
        max_pass_elev_cell = td(('%.1f' % np.max_elevation_deg))
        row.add(max_pass_elev_cell)
        if np.max_elevation_deg > config.html_elev_green_threshold:
            max_pass_elev_cell.set_attribute('bgcolor', '#80ff80')
        elif np.max_elevation_deg > config.html_elev_yellow_threshold:
            max_pass_elev_cell.set_attribute('bgcolor', 'yellow')
        row.add(td(sat.frequency))
        day_cell = td(aos_aware.astimezone().strftime(localDayFormat))
        if current_day != aos_aware.astimezone().day:
            day_cell.set_attribute('bgcolor', '#c0c0c0')
        row.add(day_cell)
        row.add(td(aos_local))
        row.add(td(los_local))
        row.add(td(('%.1f' % duration)))
        # print("%s maxElev=%.1f freq=%f dur=%.1f min aos=%s los=%s" % (
        # sat.name, np.max_elevation_deg, sat.frequency, duration, aos_local, los_local))

    html_file_name = config.html_file;
    html_file = open(html_file_name, "w")
    html_file.write(doc.render())
    html_file.close()
    print(doc)


htmlPasses(passes)
