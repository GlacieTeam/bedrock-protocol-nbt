# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt._internal.native_library import get_library_handle
from bedrock_protocol.nbt.compound_tag_variant import CompoundTagVariant
from bedrock_protocol.nbt.tag_type import TagType
from bedrock_protocol.nbt.tag import Tag
from typing import Any, List, Optional
import ctypes


class ListTag(Tag):
    """ListTag

    A Tag contains a list of tag
    """

    def __init__(self, tag_list: List[Tag] = []):
        self._lib_handle = get_library_handle()
        self._tag_handle = self._lib_handle.nbt_list_tag_create()
        self.set_list(tag_list)

    def __getitem__(self, index: int) -> Optional[Tag]:
        """Get a tag in the ListTag
        Args:
            index: the index of the tag to pop (default the end)
        Returns:
            None if failed
        """
        result = self.get(index)
        if result is not None:
            return CompoundTagVariant(self, result, index)
        return None

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

    def get_list_type(self):
        """Get tags type in this ListTag
        Returns:
            TagType
        """
        if self.size() == 0:
            return TagType.End
        else:
            return self.get(0).get_type()

    def append(self, val: Any) -> None:
        """Append a tag to the end of the ListTag
        Args:
            value: any Tag type
        """
        if isinstance(val, Tag):
            value = val
        else:
            if isinstance(val, list):
                value = ListTag(val)
            elif isinstance(val, dict):
                from bedrock_protocol.nbt.compound_tag import CompoundTag

                value = CompoundTag(val)
            elif isinstance(val, (bool, ctypes.c_uint8)):
                from bedrock_protocol.nbt.byte_tag import ByteTag

                value = ByteTag(val)
            elif isinstance(val, ctypes.c_int16):
                from bedrock_protocol.nbt.short_tag import ShortTag

                value = ShortTag(val)
            elif isinstance(val, (int, ctypes.c_int32)):
                from bedrock_protocol.nbt.int_tag import IntTag

                value = IntTag(val)
            elif isinstance(val, (int, ctypes.c_int64)):
                from bedrock_protocol.nbt.int64_tag import Int64Tag

                value = Int64Tag(val)
            elif isinstance(val, (float, ctypes.c_float)):
                from bedrock_protocol.nbt.float_tag import FloatTag

                value = FloatTag(val)
            elif isinstance(val, ctypes.c_double):
                from bedrock_protocol.nbt.double_tag import DoubleTag

                value = DoubleTag(val)
            elif isinstance(val, str):
                from bedrock_protocol.nbt.string_tag import StringTag

                value = StringTag(val)
            elif isinstance(val, (bytes, bytearray)):
                from bedrock_protocol.nbt.byte_array_tag import ByteArrayTag

                value = ByteArrayTag(val)
            else:
                raise TypeError("Wrong type of argument")
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

    def set(self, index: int, val: Any) -> bool:
        """Set a tag in the ListTag
        Args:
            index: the index of the tag to pop (default the end)
            value: new tag to set
        Returns:
            True if succeed
        """
        if isinstance(val, Tag):
            value = val
        else:
            if isinstance(val, list):
                value = ListTag(val)
            elif isinstance(val, dict):
                from bedrock_protocol.nbt.compound_tag import CompoundTag

                value = CompoundTag(val)
            elif isinstance(val, (bool, ctypes.c_uint8)):
                from bedrock_protocol.nbt.byte_tag import ByteTag

                value = ByteTag(val)
            elif isinstance(val, ctypes.c_int16):
                from bedrock_protocol.nbt.short_tag import ShortTag

                value = ShortTag(val)
            elif isinstance(val, (int, ctypes.c_int32)):
                from bedrock_protocol.nbt.int_tag import IntTag

                value = IntTag(val)
            elif isinstance(val, (int, ctypes.c_int64)):
                from bedrock_protocol.nbt.int64_tag import Int64Tag

                value = Int64Tag(val)
            elif isinstance(val, (float, ctypes.c_float)):
                from bedrock_protocol.nbt.float_tag import FloatTag

                value = FloatTag(val)
            elif isinstance(val, ctypes.c_double):
                from bedrock_protocol.nbt.double_tag import DoubleTag

                value = DoubleTag(val)
            elif isinstance(val, str):
                from bedrock_protocol.nbt.string_tag import StringTag

                value = StringTag(val)
            elif isinstance(val, (bytes, bytearray)):
                from bedrock_protocol.nbt.byte_array_tag import ByteArrayTag

                value = ByteArrayTag(val)
            else:
                raise TypeError("Wrong type of argument")
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
            return Tag._Tag__create_tag_by_handle(handle)
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

    def set_list(self, tag_list: List[Any]) -> None:
        """Set all tags in the ListTag
        Args:
            tag_list: List of tag
        """
        self.clear()
        for val in tag_list:
            self.append(val)

    def merge(self, other: "ListTag") -> None:
        if other.size() == 0:
            return
        if self.get_list_type() != other.get_list_type():
            self._lib_handle.nbt_any_tag_destroy(self._tag_handle)
            self._tag_handle = self._lib_handle.nbt_any_tag_copy(other._tag_handle)
        else:
            tag_list = self.get_list()
            for tag in other.get_list():
                if tag not in tag_list:
                    self.append(tag)
