# Raspberry Pi Human Detection

## Components

This program enables a Raspberry Pi (tested with Raspberry pi 3 Model B), to
detect a human and plays a sound clip whenever it detects a human in the
vicinity of the sendor. It uses a PIR sensor (passive infrared) connected to the
Raspbery Pi's GPIO pin number 11.

The hardware components used are:

* Raspberry Pi device
* PIR sensor
* Speaker

## Sound clips

The sound clips are not included in this repository. They need to be .mp3 files
and placed in the soundclips directory.

**Note:** When connecting a speaker and the sound output is too low, run the
following command in a terminal window. This sets the output volume to 100%:
```
amixer sset PCM,0 100%
```


## Running the script

Script can be run from a terminal window using:

```
python main.py
```

This will produce a log file: output.log in the same directory where the main.py
file resides.

Alternatively, the main.py file can be executed directly. For this to work,
first set the script to be executable, for example:

```
chmod a+x main.py
```
And then it's callable directly:

```
./main.py
```

To make the program run in the background as soon as the Raspberry Pi restarts,
edit the file /etc/rc.local with an editor. For example, using vi:
```
sudo vi /etc/rc.local
```

Then add the following line to run the main.py file when the device starts up
the next time:
```
/home/pi/projects/rpi-detect-human/main.py &
```

**Note:** this assumes the main.py file was made executable before (see above) and
that the location is within the /home/pi/projects/rpi-detect-human directory.
