# Copyright 2022 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This library adds helpers to defer an event, then wake Juju up.


"""
import logging
import subprocess

from ops.charm import CharmBase
from ops.framework import EventBase

logger = logging.getLogger(__name__)

# The unique Charmhub library identifier, never change it
LIBID = "TODO"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1


CMD = """\
sleep 1
juju-run JUJU_DISPATCH_PATH=hooks/local_wake ./dispatch
"""


class LocalWake(EventBase):
    pass


class AddDispatch:
    """Factory that generates a `defer_with_dispatch` helper."""

    def __init__(self, charm: CharmBase):
        """
        args:
            - charm: the charm that will be using the deferrer.

        """
        charm.on.define_event("local_wake", LocalWake)  # Register a no-op event.

    def __call__(self, event):
        subprocess.Popen(CMD, shell=True)
        event.defer()
