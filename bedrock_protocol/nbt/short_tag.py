# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag


class ShortTag(Tag):
    """ShortTag

    A Tag contains a short (2 bytes)
    """

    def __init__(self, value: int = 0):
        """Create a ShortTag

        Args:
            value: short value (-32768 ~ 32767)
        """
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_short_tag_create(value)

    def set(self, value: int) -> None:
        """Set ShortTag value

        Args:
            value: short value (-32768 ~ 32767)
        """
        self._lib_handle.nbt_short_tag_set_value(self._tag_handle, value)

    def get(self) -> int:
        """Get ShortTag value

        Returns:
            short value (-32768 ~ 32767)
        """
        return self._lib_handle.nbt_short_tag_get_value(self._tag_handle)
