from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_wav
import pickle, os, requests, random, time

__author__ = 'brihopki'
LOGGER = getLogger(__name__)

class TodayHistorySkill(MycroftSkill):

    def __init__(self):
        super(TodayHistorySkill, self).__init__(name="TodayHistorySkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        random_event_intent = IntentBuilder("RandomEventIntent").\
            require("RandomEventKeyword").build()
        self.register_intent(random_event_intent, self.handle_random_event_intent)

    def handle_random_event_intent(self, message):
        self.speak_dialog('event', data={'event': type(message.data.get('utterance'))})
        #self.speak_dialog('today')
        #time.sleep(0.3)

        #if "all" in message.data.get('utterance').split():
        #    for obj in self.getEvents():
        #        self.speakEntry(obj)
        #else:
        #    self.speakEntry(random.choice(self.getEvents()))

    def speakEntry(self, obj):
        play_wav(os.path.join(os.path.abspath(os.path.dirname(__file__, 'sounds', 'oneBeep.wav'))))
        time.sleep(0.3)
        s = "In " + obj['year'] + ", " + obj['text']
        self.speak_dialog('event', data={'event': s})

    def getEvents(self):
        url = 'http://history.muffinlabs.com/date'
        cacheFile = "/tmp/TodayInHistoryEvents.cache"
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
