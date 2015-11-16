﻿from easysettings import EasySettings
from unittest import TestCase


class TestBase(TestCase):
 
    US_app_id = "bbbbbc.xgjbvPdwkllw"
    US_app_key = "1E9E824E-A3F1-4F34-B4F4-9CC87471A564"
    EU_app_id = "bbbbbc.cnbbbhbKqvNh"
    EU_app_key = "46D8D6B7-7F09-4919-B81D-F1F6DEFFEEFF"

    def setUp(self):
        es = EasySettings("buddy.conf")
        es.clear()
        es.save()

    def javascript_datetime_from_datetime(self, datetime):
        return "/Date(" + str(round(self.ticks_from_timestamp(datetime.timestamp()))) + ")/"

    def ticks_from_timestamp(self, timestamp):
        return timestamp * 1000
