# Copyright 2022 Penelope Valentine Gale
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest

from ops.model import ActiveStatus, MaintenanceStatus
from ops.testing import Harness

from charm import DeferWithDispatchCharm


class TestCharm(unittest.TestCase):
    def setUp(self):
        self.harness = Harness(DeferWithDispatchCharm)
        self.addCleanup(self.harness.cleanup)

    def test_defer_with_dispatch(self):
        # Verify that our core charm logic works. The invocation of defer_with_dispatch
        # won't do anything in the test, because it spawns a child process. We'll test it
        # in an integration test.
        self.harness.begin_with_initial_hooks()
        self.assertEqual(self.harness.model.unit.status, MaintenanceStatus("Deferred"))

        # Simulate second run.
        self.harness.charm.on.config_changed.emit()
        self.assertEqual(self.harness.model.unit.status, ActiveStatus())
