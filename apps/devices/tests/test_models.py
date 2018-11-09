from apps.common.utils._tests import BaseTest

import datetime
import uuid


class DeviceModelTest(BaseTest):
    def test_should_create_device(self):
        self.assertIsNotNone(self.test_device)

    def test_should_assert_methods(self):
        self.assertEqual(str(self.test_device), str(self.test_device.id))