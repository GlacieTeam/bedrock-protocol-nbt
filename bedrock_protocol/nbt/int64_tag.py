# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag


class Int64Tag(Tag):
    """IntTag

    A Tag contains an int64 (8 bytes)
    """

    def __init__(self, value: int = 0):
        """Create a Int64Tag

        Args:
            value: int64 value (-9223372036854775808 ~ 9223372036854775807)
        """
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_int64_tag_create(value)

    def set(self, value: int) -> None:
        """Set IntTag value

        Args:
            value: int64 value (-9223372036854775808 ~ 9223372036854775807)
        """
        self._lib_handle.nbt_int64_tag_set_value(self._tag_handle, value)

    def get(self) -> int:
        """Get IntTag value

        Returns:
            int64 value (-9223372036854775808 ~ 9223372036854775807)
        """
        return self._lib_handle.nbt_int64_tag_get_value(self._tag_handle)
