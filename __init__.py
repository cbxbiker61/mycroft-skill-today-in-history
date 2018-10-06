from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_wav
import pickle, os, requests, random, time

__author__ = 'brihopki'
LOGGER = getLogger(__name__)

class TodayHistorySkill(MycroftSkill):

    beepWav = None

    def __init__(self):
        super(TodayHistorySkill, self).__init__(name="TodayHistorySkill")
        self.beepWav = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sounds', 'oneBeep.wav')

    def initialize(self):
        self.load_data_files(dirname(__file__))

        random_event_intent = IntentBuilder("RandomEventIntent").require("RandomEventKeyword").build()
        self.register_intent(random_event_intent, self.handle_random_event_intent)

    def handle_random_event_intent(self, message):
        self.speak_dialog('today')

        if "all" in message.data.get('utterance').split():
            for obj in self.getEvents():
                self.speakEvent(obj)
        else:
            self.speakEvent(random.choice(self.getEvents()))

    def speakEvent(self, obj):
        play_wav(self.beepWav)
        time.sleep(0.3)
        self.speak("In " + obj['year'] + ", " + obj['text'])

    def getEvents(self):
        url = 'http://history.muffinlabs.com/date'
        cacheFile = "/var/tmp/TodayInHistoryEvents.cache"
        cacheSeconds = (60*60*2) # 2 hours

        if not os.path.exists(cacheFile) or (os.path.getmtime(cacheFile) < time.time() - cacheSeconds):
            r = requests.get(url)

            with open(cacheFile, "wb") as f:
                # r.json is a dict
                pickle.dump(r.json()['data']['Events'], f)

        with open(cacheFile, "rb") as f:
            return pickle.load(f)

    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return TodayHistorySkill()
