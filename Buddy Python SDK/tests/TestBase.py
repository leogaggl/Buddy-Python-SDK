import unittest

import easysettings


class TestBase(unittest.TestCase):
 
    US_app_id = "bbbbbc.xgjbvPdwkllw"
    US_app_key = "1E9E824E-A3F1-4F34-B4F4-9CC87471A564"
    EU_app_id = "bbbbbc.cnbbbhbKqvNh"
    EU_app_key = "46D8D6B7-7F09-4919-B81D-F1F6DEFFEEFF"

    def setUp(self):
        es = easysettings.EasySettings("buddy.conf")
        es.clear()
        es.save()

    def javascript_datetime_from_datetime(self, datetime):
        return "/Date(" + str(round(datetime.timestamp() * 1000)) + ")/"
