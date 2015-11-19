from datetime import datetime
from datetime import timezone
from datetime import timedelta
from easysettings import EasySettings
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

    def future_javascript_access_token_expires(self):
        return self.__javascript_access_token_expires(1)

    def past_javascript_access_token_expires(self):
        return self.__javascript_access_token_expires(-1)

    def __javascript_access_token_expires(self, days):
        delta = datetime.now(timezone.utc) + timedelta(days)
        return self.__javascript_access_token_expires_string(delta)

    def __javascript_access_token_expires_string(self, python_datetime):
        return "/Date(" + str(round(self.ticks_from_timestamp(python_datetime.timestamp()))) + ")/"

    def ticks_from_timestamp(self, timestamp):
        return timestamp * 1000
