import easysettings
import unittest
from buddysdk import Settings

class TestBase(unittest.TestCase):
 
    def setUp(self):
        es = easysettings.EasySettings("buddy.conf")
        es.clear()
        es.save()

    def javascript_datetime_from_datetime(self, datetime):
        return "/Date(" + str(round(datetime.timestamp() * 1000)) + ")/"