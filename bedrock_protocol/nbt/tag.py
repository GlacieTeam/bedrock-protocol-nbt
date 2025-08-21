# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt._internal.native_library import get_library_handle
from bedrock_protocol.binarystream import ReadOnlyBinaryStream, BinaryStream
from bedrock_protocol.nbt.tag_type import TagType
import ctypes


class Tag:
    """Base Tag Class"""

    _tag_handle: ctypes.c_void_p
    _lib_handle: ctypes.CDLL

    def __init__(self):
        """
        Warning:
            Internal function
            Do not construct this type
        """
        self._lib_handle = get_library_handle()
        self._tag_handle = None

    def __eq__(self, value):
        return self.equals(value)

    def __hash__(self):
        return self.hash()

    def __del__(self):
        """
        Warning:
            Internal function
            free memory
        """
        self._lib_handle.nbt_any_tag_destroy(self._tag_handle)

    def _update_type(self):
        """
        Warning:
            Internal function
            update object type
        """
        tag_type = self.get_type()
        if tag_type == TagType.End:
            from bedrock_protocol.nbt.end_tag import EndTag

            self.__class__ = EndTag
        elif tag_type == TagType.Byte:
            from bedrock_protocol.nbt.byte_tag import ByteTag

            self.__class__ = ByteTag
        elif tag_type == TagType.Short:
            from bedrock_protocol.nbt.short_tag import ShortTag

            self.__class__ = ShortTag
        elif tag_type == TagType.Int:
            from bedrock_protocol.nbt.int_tag import IntTag

            self.__class__ = IntTag
        elif tag_type == TagType.Int64:
            from bedrock_protocol.nbt.int64_tag import Int64Tag

            self.__class__ = Int64Tag
        elif tag_type == TagType.Float:
            from bedrock_protocol.nbt.float_tag import FloatTag

            self.__class__ = FloatTag
        elif tag_type == TagType.Double:
            from bedrock_protocol.nbt.double_tag import DoubleTag

            self.__class__ = DoubleTag
        elif tag_type == TagType.ByteArray:
            from bedrock_protocol.nbt.byte_array_tag import ByteArrayTag

            self.__class__ = ByteArrayTag
        elif tag_type == TagType.String:
            from bedrock_protocol.nbt.string_tag import StringTag

            self.__class__ = StringTag
        elif tag_type == TagType.List:
            from bedrock_protocol.nbt.list_tag import ListTag

            self.__class__ = ListTag
        elif tag_type == TagType.Compound:
            from bedrock_protocol.nbt.compound_tag import CompoundTag

            self.__class__ = CompoundTag
        elif tag_type == TagType.IntArray:
            from bedrock_protocol.nbt.int_array_tag import IntArrayTag

            self.__class__ = IntArrayTag

    def get_type(self) -> TagType:
        """
        Returns:
            TagType: the tag type.
        """
        return self._lib_handle.nbt_any_tag_get_type(self._tag_handle)

    def equals(self, other: "Tag") -> bool:
        """
        Args:
            Tag: other tag

        Returns:
            bool: equals to other tag
        """
        return self._lib_handle.nbt_any_tag_equals(self._tag_handle, other._tag_handle)

    def hash(self) -> int:
        """
        Returns:
            int: hash value of this tag
        """
        return self._lib_handle.nbt_any_tag_hash(self._tag_handle)

    def deep_copy(self) -> "Tag":
        """
        Returns:
            Tag: the deep copy of this tag
        """
        result = Tag()
        result._tag_handle = self._lib_handle.nbt_any_tag_copy(self._tag_handle)
        result._update_type()
        return result

    def write(self, stream: BinaryStream) -> None:
        """
        Args:
            BinaryStream: output stream
        """
        self._lib_handle.nbt_any_tag_write(self._tag_handle, stream._stream_handle)

    def load(self, stream: ReadOnlyBinaryStream) -> None:
        """
        Args:
            ReadOnlyBinaryStream: input stream
        """
        self._lib_handle.nbt_any_tag_load(self._tag_handle, stream._stream_handle)
