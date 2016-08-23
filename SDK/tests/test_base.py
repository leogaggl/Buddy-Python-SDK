from datetime import datetime
from datetime import timedelta
from dateutil.tz import tzutc
import os
from uuid import uuid4
import unittest

import buddy
from settings import Settings


class TestBase(unittest.TestCase):

    # TODO: Go to http://buddyplatform.com to get an app ID and app keys for US and EU apps.
    US_app_id = "bbbbbc.MMcgHkKJlFvnc"
    US_app_key = "c840f56d-8e73-b94d-150c-4888862ce362"
    EU_app_id = "bbbbbc.gfnGlNfJFvFP"
    EU_app_key = "76123a72-4d05-93db-f297-b8a7501fd2f7"

    def setUp(self):
        try:
            os.remove(Settings.buddy_cfg_name)
        finally:
            self.reset_module()
            return

    def reset_module(self):
        buddy.https_client = None
        buddy.mqtt_client = None
        buddy.settings = None
        buddy.events = None
        buddy.mqtt_events = None

    def setup_with_bad_tokens(self, settings):
        settings.set_device_token({"accessToken": "bad device token",
                                   "accessTokenExpires": self.past_javascript_access_token_expires()})
        settings.set_user({"id": "bad", "accessToken": "bad user token",
                           "accessTokenExpires": self.past_javascript_access_token_expires()})

    def future_javascript_access_token_expires(self):
        return self.__javascript_access_token_expires(1)

    def past_javascript_access_token_expires(self):
        return self.__javascript_access_token_expires(-1)

    def datetime_from_days(self, days):
        return datetime.now(tzutc()) + timedelta(days=days)

    def __javascript_access_token_expires(self, days):
        utc_now_plus_days = self.datetime_from_days(days)

        return self.__javascript_access_token_expires_string(utc_now_plus_days)

    def __javascript_access_token_expires_string(self, python_datetime):
        return "/Date({0:.0f})/".format(self.ticks_from_datetime(python_datetime))

    def ticks_from_datetime(self, python_datetime):
        return self.__ticks_from_timestamp(self.__total_seconds_from_datetime(python_datetime))

    def __total_seconds_from_datetime(self, python_datetime):
        return (python_datetime - datetime(1970, 1, 1, tzinfo=tzutc())).total_seconds()\
                / timedelta(seconds=1).total_seconds()

    def __ticks_from_timestamp(self, timestamp):
        return round(timestamp * 1000)

    def create_test_user(self, user_name=None):
        return buddy.https.create_user(self.get_test_user_name() if user_name is None else user_name,
                                 self.get_test_user_password())

    def get_test_user_name(self):
        return "testuser" + str(uuid4())

    def get_test_user_password(self):
        return "testpassword"
