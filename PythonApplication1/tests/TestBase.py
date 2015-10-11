import unittest
import easysettings
from buddysdk import Settings

class TestBase(unittest.TestCase):
 
    def setUp(self):
        es = easysettings.EasySettings("buddy.conf")
        es.clear()

    def convert_datetime_to_ticks(self, datetime):
        return "/Date(" + str(round(datetime.timestamp() * 1000)) + ")/"