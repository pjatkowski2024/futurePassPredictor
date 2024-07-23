# futurePassPredictor

Produce a HTML page with future satellite passes.

The code was derived from the Auto137 project (doc included below) with the idea that config.yaml file format
should be shareable between the two projects.


### Overview
* futurePassPredictor uses a local copy of the TLE data that can be easily be refreshed via command line.  This keeps from hammering the TLE server and should be updated periodically (manually or via cron)
* The list of satellites is configured in `config.yaml`
* `config.yaml` in the current directory is used unless the `--basedir` option is used to specify an alternate directory.  
  User expansion is used to process the basedir so things like `~/` or `~www` as well as `/var/www/htm/..` will work.
* Paths in `config.yaml` (html_output_file, tle_file) also go through user expansion and accept the same types of  
  arguments.
* `html_output_file` can be specified as `-` to write the command output rather than a file.
### Operation
`python3 futurePassPredictor`  # for config.yaml in the current directory
`python3 futurePassPredictor --basedir <someDirectory>`  # for config.yaml in <someDirectory>

see config.yaml for other inputs/parameters.

Dependencies:

* [orbit-predictor](https://github.com/satellogic/orbit-predictor) (Pass prediction)
* `dominate`

# Auto137 (for reference)

There already is quite a bunch of programs fullfilling the same function, that is managing an automatic satellite receiving / decoding station aimed at NOAA / METEOR, but none worked the way I wanted it to... So was born Auto137, a python-based autonomous APT / LRPT / etc station made to easily support more options and be cleaner (only 1 language).

### What it does

This program, along with the necessary external tools and libraries, can do all this :
*  TLE fetching from Celestrak
*  Predict passes
*  Record satellites passes
*  Decode it
*  Pass conflict solving, including priorities
*  Easy support for other protocols
*  Multi-Threaded, decoding does not impact reception

All decoded data is saved into the chosen directory and an optional RSS feed can be enabled (no history saving to save on size).

### Requirements

* rtl_sdr (could be modified to use anything else)
* ffmpeg
* [noaa-apt](https://github.com/martinber/noaa-apt) (APT decoding)
* [Meteor M2 Demodulator](https://github.com/dbdexter-dev/meteor_demod) (QPSK demodulation)
* [LRPT Decoder](https://github.com/artlav/meteor_decoder) (LRPT image decoding)
* [satellitetle](https://gitlab.com/librespacefoundation/python-satellitetle) (TLE fetching)
* [orbit-predictor](https://github.com/satellogic/orbit-predictor) (Pass prediction)
* [pyyaml](https://github.com/yaml/pyyaml) (YAML config file)
* [apscheduler](https://github.com/agronholm/apscheduler) (Task scheduling)
* [PyRSS2Gen](http://dalkescientific.com/Python/PyRSS2Gen.html) (Rss feed generation)

### Installation

This procedure should work on any debian-based system (including Raspbian). If using anything else replace apt with your distro's package manager (eg. dnf, yum, pacman, opkg).

Start by installing all required packages through your package manager, including pip for other dependencies.

`sudo apt install ffmpeg rtl-sdr python3-pip python3-numpy fpc build-essential`

Then install all python libraries.

`sudo pip3 install satellitetle orbit_predictor apscheduler pyyaml PyRSS2Gen`

Now you need to install noaa-apt (download [here](https://noaa-apt.mbernardi.com.ar/download.html)), and compile meteor_demod and meteor_decoder :

`git clone https://github.com/artlav/meteor_decoder.git && cd meteor_decoder && sh ./build_medet.sh && sudo cp medet /usr/bin`

`git clone https://github.com/dbdexter-dev/meteor_demod.git && cd meteor_demod && make && sudo make install`


Now clone this git repo, edit the config file to your likings and start main.py using `python3 main.py`. If you experience an exception concerning `config = yaml.load(f, Loader=yaml.FullLoader)`, change it into `config = yaml.load(f)`.
