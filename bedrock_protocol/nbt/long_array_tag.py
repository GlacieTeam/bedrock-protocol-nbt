# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt._internal.native_library import get_library_handle
from bedrock_protocol.nbt.tag import Tag
from typing import List, Optional


class LongArrayTag(Tag):
    """LongArrayTag

    A Tag contains a list of int
    """

    def __init__(self, tag_list: List[int] = []):
        self._lib_handle = get_library_handle()
        self._tag_handle = self._lib_handle.nbt_long_array_tag_create()
        self.set_list(tag_list)

    def __getitem__(self, index: int) -> Optional[int]:
        """Get an int64 in the LongArrayTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            None if failed
        """
        return self.get(index)

    def __setitem__(self, index: int, value: int) -> bool:
        """Set an int64 in the LongArrayTag
        Args:
            index: the index of the int to pop (default the end)
            value: new int to set
        Returns:
            True if succeed
        """
        return self.set(index, value)

    def __delitem__(self, index: int) -> bool:
        """Delete value from the LongArrayTag
        Args:
            index: the index of the int to pop (default the end)
        Returns:
            True if pop succeed
        """
        return self.pop(index)

    def size(self) -> int:
        """Get size of the LongArrayTag
        Returns:
            size
        """
        return self._lib_handle.nbt_long_array_tag_size(self._tag_handle)

    def append(self, value: int) -> None:
        """Append a int to the end of the LongArrayTag
        Args:
            value: int
        """
        self._lib_handle.nbt_long_array_tag_add_value(self._tag_handle, value)

    def pop(self, index: int = -1) -> bool:
        """Delete value from the LongArrayTag
        Args:
            index: the index of the int to pop (default the end)
        Returns:
            True if pop succeed
        """
        if index < 0:
            return self._lib_handle.nbt_long_array_tag_remove_value(
                self._tag_handle, self.size() - 1
            )
        return self._lib_handle.nbt_long_array_tag_remove_value(self._tag_handle, index)

    def set(self, index: int, value: int) -> bool:
        """Set a int in the LongArrayTag
        Args:
            index: the index of the int to pop (default the end)
            value: new int to set
        Returns:
            True if succeed
        """
        return self._lib_handle.nbt_long_array_tag_set_value(
            self._tag_handle, index, value
        )

    def get(self, index: int) -> Optional[int]:
        """Get a tag in the LongArrayTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            None if failed
        """
        return self._lib_handle.nbt_long_array_tag_get_value(self._tag_handle, index)

    def clear(self) -> None:
        """Clear all tags in the LongArrayTag"""
        self._lib_handle.nbt_long_array_tag_clear(self._tag_handle)

    def get_list(self) -> List[int]:
        """Get all tags in the LongArrayTag
        Returns:
            List of tag
        """
        result = list()
        index = 0
        size = self.size()
        while index < size:
            result.append(self.get(index))
            index += 1
        return result

    def set_list(self, int_list: List[int]) -> None:
        """Set all tags in the LongArrayTag
        Args:
            tag_list: List of tag
        """
        self.clear()
        for val in int_list:
            self.append(val)
