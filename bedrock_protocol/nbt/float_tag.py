# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag


class FloatTag(Tag):
    """FloatTag

    A Tag contains a float (4 bytes)
    """

    def __init__(self, value: float = 0):
        """Create a FloatTag

        Args:
            value: float value
        """
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_float_tag_create(value)

    def set(self, value: float) -> None:
        """Set FloatTag value

        Args:
            value: float value
        """
        self._lib_handle.nbt_float_tag_set_value(self._tag_handle, value)

    def get(self) -> float:
        """Set FloatTag value

        Args:
            value: float value
        """
        return self._lib_handle.nbt_float_tag_get_value(self._tag_handle)
