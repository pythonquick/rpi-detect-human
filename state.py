import time


class State:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "%s" % self.name
    def performStateAction(self):
        raise NotImplementedError()


class IdleState(State):
    def humanDetected(self):
        return HUMAN_DETECTED_STATE
    def nothingDetected(self):
        return IDLE_STATE
    def longPeriodPasses(self):
        return IDLE_STATE
    def performStateAction(self):
        return None


class HumanDetectedState(State):
    def humanDetected(self):
        return HUMAN_RECENTLY_DETECTED_STATE
    def nothingDetected(self):
        return HUMAN_RECENTLY_DETECTED_STATE
    def longPeriodPasses(self):
        return HUMAN_RECENTLY_DETECTED_STATE
    def performStateAction(self):
        return "PLAY_SOUND"


class HumanRecentlyDetectedState(State):
    def humanDetected(self):
        return HUMAN_RECENTLY_DETECTED_STATE
    def nothingDetected(self):
        return HUMAN_RECENTLY_DETECTED_STATE
    def longPeriodPasses(self):
        return IDLE_STATE
    def performStateAction(self):
        return None


IDLE_STATE = IdleState('Idle')
HUMAN_DETECTED_STATE = HumanDetectedState('Human Detected')
HUMAN_RECENTLY_DETECTED_STATE = HumanRecentlyDetectedState('Recently Detected')


if __name__ == '__main__':
    state = IDLE_STATE
    while True:
        entry = raw_input("H N or P: ")
        if entry == "H":
            state = state.humanDetected()
        elif entry == "N":
            state = state.nothingDetected()
        elif entry == "P":
            state = state.longPeriodPasses()

        print state, state.performStateAction


