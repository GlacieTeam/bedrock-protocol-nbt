# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt._internal.native_library import get_library_handle
from bedrock_protocol.nbt.tag import Tag


class DoubleTag(Tag):
    """FloatTag

    A Tag contains a double (8 bytes)
    """

    def __init__(self, value: float = 0):
        """Create a DoubleTag

        Args:
            value: double value
        """
        self._lib_handle = get_library_handle()
        self._tag_handle = self._lib_handle.nbt_double_tag_create(value)

    def set(self, value: float) -> None:
        """Set DoubleTag value

        Args:
            value: double value
        """
        self._lib_handle.nbt_double_tag_set_value(self._tag_handle, value)

    def get(self) -> float:
        """Get DoubleTag value

        Args:
            value: double value
        """
        return self._lib_handle.nbt_double_tag_get_value(self._tag_handle)
