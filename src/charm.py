#!/usr/bin/env python3
# Copyright 2022 Penelope Valentine Gale
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from charms.defer_with_dispatch.v0.deferwithdispatch import AddDispatch
from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)


class DeferWithDispatchCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)

        # Add our deferrer.
        self.defer_with_dispatch = AddDispatch(self)

        # Setup an event to defer.
        self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_config_changed(self, event):
        deferred = MaintenanceStatus("Deferred")
        active = ActiveStatus("Run")

        if self.model.unit.status not in (deferred, active):
            self.defer_with_dispatch(event)
            self.model.unit.status = MaintenanceStatus("Deferred")
            return

        self.model.unit.status = active


if __name__ == "__main__":
    main(DeferWithDispatchCharm)
