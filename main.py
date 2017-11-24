#!/usr/bin/python


import RPi.GPIO as GPIO
import time
import pygame
import os
from state import IDLE_STATE, HUMAN_DETECTED_STATE, HUMAN_RECENTLY_DETECTED_STATE


# SETUP:
IDLE_RESET_TIME = 15        # number of seconds until it returns to IDLE state
PIR_SENSOR_PIN = 11         # number of the GPIO pin connected to PIR sensor
playCount = 0               # count of how many times a sound clip was played


def base_dir():
    return os.path.dirname(os.path.realpath(__file__))


def clips_dir():
    return os.path.join(base_dir(), 'soundclips')


def log_file():
    return os.path.join(base_dir(), 'output.log')


def sound_clip_files():
    return [filename for filename in os.listdir(clips_dir()) if filename.endswith('mp3')]


def play_clip(filename):
    full_path = os.path.join(clips_dir(), filename)
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def play_next_clip():
    global playCount
    clips = sound_clip_files()
    nextClipIndex = playCount % len(clips)
    nextClip = clips[nextClipIndex]
    log("Playing %s" % nextClip)
    play_clip(nextClip)
    playCount += 1


def reset_log():
    f = open(log_file(), 'wt')
    f.close()


def log(msg):
    print msg
    f = open(log_file(), 'at')
    f.write("%s : %s\n" % (time.asctime(), msg))
    f.close()


def main():
    currentSensor = 0
    timeLastHumanDetected = 0
    contact_counter = 0
    state = IDLE_STATE

    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_SENSOR_PIN, GPIO.IN)
        pygame.mixer.init()
        reset_log()
        log("Starting up")
        log(state)
        while True:
            time.sleep(0.1)
            timeNow = time.time()
            sensor = GPIO.input(PIR_SENSOR_PIN)
            if sensor != currentSensor:
                if sensor == 1:
                    timeLastHumanDetected = timeNow
                    contact_counter += 1
                    log("HUMAN DETECTED! count: %d" % contact_counter)
                    state = state.humanDetected()
                else:
                    log("no human in sight")
                    state = state.nothingDetected()
            currentSensor = sensor

            # Perform some action if needed:
            action = state.performStateAction()
            if action == "PLAY_SOUND":
                #play_clip('darth-vader-breath.mp3')
                play_next_clip()
                state = HUMAN_RECENTLY_DETECTED_STATE

            time_since_human_detection = timeNow - timeLastHumanDetected
            if time_since_human_detection >= IDLE_RESET_TIME:
                if state != IDLE_STATE:
                    log("GOING BACK TO IDLE after %d seconds" % IDLE_RESET_TIME)
                state = state.longPeriodPasses()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
