import mock
import unittest

import buddy
from buddy_client import BuddyClient
from settings import Settings
from test_base import TestBase


class Test4(TestBase):

    @mock.patch("buddy_client.Settings")
    def test_register_device_us(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.US_app_id)
        self.setup_with_bad_tokens(settings_mock.return_value)

        self._register_device(self, TestBase.US_app_id, TestBase.US_app_key, "https://api")

    @mock.patch("buddy_client.Settings")
    def test_register_device_eu(self, settings_mock):
        settings_mock.return_value = Settings(TestBase.EU_app_id)
        self.setup_with_bad_tokens(settings_mock.return_value)

        self._register_device(self, TestBase.EU_app_id, TestBase.EU_app_key, "https://api-eu")

    def _register_device(self, test, app_id, app_key, service_root_starts_with):
        client = buddy.init(app_id, app_key, service_root_starts_with)

        access_token_string = client.get_access_token_string()

        settings = Settings(app_id)
        test.assertEqual(access_token_string, settings.access_token_string)
        test.assertTrue(settings.service_root.startswith(service_root_starts_with))

    @mock.patch.object(BuddyClient, "_BuddyClient__handle_dictionary_request")
    def test_hardware_info(self, handle_dictionary_request_mock):
        handle_dictionary_request_mock.return_value = {BuddyClient.result_name: None}
        
        # to run in Python Tools for VS, change to "tests\cpuinfo"
        BuddyClient._hardware_info_file_name = "cpuinfo"

        client = buddy.init(TestBase.US_app_id, TestBase.US_app_key, "test_hardware_info")

        client.get_access_token_string()

        cpuinfo = handle_dictionary_request_mock.call_args[0][2]
        self.assertEqual(cpuinfo["model"], "BCM2708-000e")
        self.assertEqual(cpuinfo["uniqueId"], "00000000********")


if __name__ == '__main__':
    unittest.main()
