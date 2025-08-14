# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag


class ByteTag(Tag):
    """ByteTag

    A Tag contains a byte (1 bytes)
    """

    def __init__(self, value: int = 0):
        """Create a ByteTag

        Args:
            value: byte value (0 ~ 255)
        """
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_byte_tag_create(value)

    def set(self, value: int) -> None:
        """Set ByteTag value

        Args:
            value: byte value (0 ~ 255)
        """
        self._lib_handle.nbt_byte_tag_set_value(self._tag_handle, value)

    def get(self) -> int:
        """Get ByteTag value

        Returns:
            byte value (0 ~ 255)
        """
        return self._lib_handle.nbt_byte_tag_get_value(self._tag_handle)
