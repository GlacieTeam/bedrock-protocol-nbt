# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag


class IntTag(Tag):
    """IntTag

    A Tag contains an int (4 bytes)
    """

    def __init__(self, value: int = 0):
        """Create a IntTag

        Args:
            value: int value (-2147483648 ~ 2147483647)
        """
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_int_tag_create(value)

    def set(self, value: int) -> None:
        """Set IntTag value

        Args:
            value: int value (-2147483648 ~ 2147483647)
        """
        self._lib_handle.nbt_int_tag_set_value(self._tag_handle, value)

    def get(self) -> int:
        """Get IntTag value

        Returns:
            int value (-2147483648 ~ 2147483647)
        """
        
        return self._lib_handle.nbt_int_tag_get_value(self._tag_handle)
