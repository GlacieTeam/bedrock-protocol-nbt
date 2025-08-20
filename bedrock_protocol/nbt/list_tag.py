# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag
from typing import List, Optional


class ListTag(Tag):
    """ListTag

    A Tag contains a list of tag
    """

    def __init__(self, tag_list: List[Tag] = []):
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_list_tag_create()
        self.set_list(tag_list)

    def __getitem__(self, index: int) -> Optional[Tag]:
        """Get a tag in the ListTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            None if failed
        """
        return self.get(index)

    def __setitem__(self, index: int, value: Tag) -> bool:
        """Set a tag in the ListTag
        Args:
            index: the index of the tag to pop (default the end)
            value: new tag to set
        Returns:
            True if succeed
        """
        return self.set(index, value)

    def __delitem__(self, index: int) -> bool:
        """Delete value from the ListTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            True if pop succeed
        """
        return self.pop(index)

    def size(self) -> int:
        """Get size of the ListTag
        Returns:
            size
        """
        return self._lib_handle.nbt_list_tag_size(self._tag_handle)

    def append(self, value: Tag) -> None:
        """Append a tag to the end of the ListTag
        Args:
            value: any Tag type
        """
        self._lib_handle.nbt_list_tag_add_tag(self._tag_handle, value._tag_handle)

    def pop(self, index: int = -1) -> bool:
        """Delete value from the ListTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            True if pop succeed
        """
        if index < 0:
            return self._lib_handle.nbt_list_tag_remove_tag(
                self._tag_handle, self.size() - 1
            )
        return self._lib_handle.nbt_list_tag_remove_tag(self._tag_handle, index)

    def set(self, index: int, value: Tag) -> bool:
        """Set a tag in the ListTag
        Args:
            index: the index of the tag to pop (default the end)
            value: new tag to set
        Returns:
            True if succeed
        """
        return self._lib_handle.nbt_list_tag_set_tag(
            self._tag_handle, index, value._tag_handle
        )

    def get(self, index: int) -> Optional[Tag]:
        """Get a tag in the ListTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            None if failed
        """
        handle = self._lib_handle.nbt_list_tag_get_tag(self._tag_handle, index)
        if handle is not None:
            result = Tag()
            result._tag_handle = handle
            result._update_type()
            return result
        return None

    def clear(self) -> None:
        """Clear all tags in the ListTag"""
        self._lib_handle.nbt_list_tag_clear(self._tag_handle)

    def get_list(self) -> List[Tag]:
        """Get all tags in the ListTag
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

    def set_list(self, tag_list: List[Tag]) -> None:
        """Set all tags in the ListTag
        Args:
            tag_list: List of tag
        """
        self.clear()
        for tag in tag_list:
            self.append(tag)
