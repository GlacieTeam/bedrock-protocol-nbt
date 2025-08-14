# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag
from bedrock_protocol.nbt.snbt_format import SnbtFormat
from bedrock_protocol.nbt._internal.native_library import get_library_handle
from typing import Optional, Union
import ctypes


class CompoundTag(Tag):
    """CompoundTag

    A Tag contains map of tags
    """

    def __init__(self):
        """Create a CompoundTag"""
        super().__init__()
        self._tag_handle = self._lib_handle.nbt_compound_tag_create()

    def __getitem__(self, key: Union[bytes, str]) -> Tag:
        """Get a tag in the CompoundTag
        Args:
            key: the key of the tag to pop (default the end)
        Returns:
            None if failed
        """
        return self.get(key)

    def __setitem__(self, key: Union[bytes, str], value: Tag) -> bool:
        """Set a tag in the CompoundTag
        Args:
            key: the key of the tag to pop (default the end)
            value: new tag to set
        Returns:
            True if succeed
        """
        return self.set(key, value)

    def __delitem__(self, key: Union[bytes, str]) -> bool:
        """Delete value from the CompoundTag
        Args:
            key: the key of the tag to pop (default the end)
        Returns:
            True if pop succeed
        """
        return self.pop(key)

    def size(self) -> int:
        """Get size of the CompoundTag
        Returns:
            size
        """
        return self._lib_handle.nbt_compound_tag_size(self._tag_handle)

    def pop(self, key: Union[bytes, str]) -> bool:
        """Delete value from the CompoundTag
        Args:
            key: the key of the tag to pop (default the end)
        Returns:
            True if pop succeed
        """
        index = key
        if isinstance(index, str):
            index = key.encode("utf-8")
        length = len(index)
        char_ptr = ctypes.c_char_p(index)
        return self._lib_handle.nbt_compound_tag_remove_tag(
            self._tag_handle, char_ptr, length
        )

    def set(self, key: Union[bytes, str], value: Tag) -> bool:
        """Set a tag in the CompoundTag
        Args:
            key: the key of the tag to pop (default the end)
            value: new tag to set
        Returns:
            True if succeed
        """
        index = key
        if isinstance(index, str):
            index = key.encode("utf-8")
        length = len(index)
        char_ptr = ctypes.c_char_p(index)
        return self._lib_handle.nbt_compound_tag_set_tag(
            self._tag_handle, char_ptr, length, value._tag_handle
        )

    def get(self, key: Union[bytes, str]) -> Optional[Tag]:
        """Get a tag in the CompoundTag
        Args:
            key: the key of the tag to pop (default the end)
        Returns:
            None if failed
        """
        index = key
        if isinstance(index, str):
            index = key.encode("utf-8")
        length = len(index)
        char_ptr = ctypes.c_char_p(index)
        handle = self._lib_handle.nbt_compound_tag_get_tag(
            self._tag_handle, char_ptr, length
        )
        if handle is not None:
            result = Tag()
            result._tag_handle = handle
            result._update_type()
            return result
        return None

    def clear(self) -> None:
        """Clear all tags in the CompoundTag"""
        self._lib_handle.nbt_compound_tag_clear(self._tag_handle)

    def to_binary_nbt(self, little_endian: bool = True) -> bytes:
        """Encode the CompoundTag to binary NBT format
        Args:
            little_endian: whether use little-endian bytes order
        Returns:
            serialized bytes
        """
        buffer = self._lib_handle.nbt_compound_to_binary_nbt(
            self._tag_handle, little_endian
        )
        result = bytes(ctypes.string_at(buffer.data, buffer.size))
        self._lib_handle.nbtio_buffer_destroy(ctypes.byref(buffer))
        return result

    def to_network_nbt(self) -> bytes:
        """Encode the CompoundTag to network NBT format
        Returns:
            serialized bytes
        """
        buffer = self._lib_handle.nbt_compound_to_network_nbt(self._tag_handle)
        result = bytes(ctypes.string_at(buffer.data, buffer.size))
        self._lib_handle.nbtio_buffer_destroy(ctypes.byref(buffer))
        return result

    def to_snbt(
        self, format: SnbtFormat = SnbtFormat.PrettyFilePrint, indent: int = 4
    ) -> str:
        """Encode the CompoundTag to network NBT format
        Returns:
            serialized bytes
        """
        buffer = self._lib_handle.nbt_compound_to_snbt(self._tag_handle, format, indent)
        result = bytes(ctypes.string_at(buffer.data, buffer.size))
        self._lib_handle.nbtio_buffer_destroy(ctypes.byref(buffer))
        try:
            return result.decode("utf-8")
        except UnicodeDecodeError:
            return ""

    def to_json(self, indent: int = 4) -> str:
        """Encode the CompoundTag to JSON
        Returns:
            serialized bytes

        Warning:
            JSON can NOT be deserialized to NBT
        """
        buffer = self._lib_handle.nbt_compound_to_json(self._tag_handle, indent)
        result = bytes(ctypes.string_at(buffer.data, buffer.size))
        self._lib_handle.nbtio_buffer_destroy(ctypes.byref(buffer))
        try:
            return result.decode("utf-8")
        except UnicodeDecodeError:
            return ""

    @staticmethod
    def from_binary_nbt(content: bytes, little_endian: bool = True) -> "CompoundTag":
        """Parse binary NBT
        Args:
            little_endian: whether use little-endian bytes order
        Returns:
            CompoundTag
        """
        length = len(content)
        char_ptr = ctypes.c_char_p(content)
        buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
        result = Tag()
        result._tag_handle = get_library_handle().nbt_compound_from_binary_nbt(
            ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)), length, little_endian
        )
        result.__class__ = CompoundTag
        return result

    @staticmethod
    def from_network_nbt(content: bytes) -> "CompoundTag":
        """Parse network NBT
        Returns:
            CompoundTag
        """
        length = len(content)
        char_ptr = ctypes.c_char_p(content)
        buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
        result = Tag()
        result._tag_handle = get_library_handle().nbt_compound_from_network_nbt(
            ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)), length
        )
        result.__class__ = CompoundTag
        return result

    @staticmethod
    def from_snbt(content: str) -> "CompoundTag":
        """Parse SNBT
        Returns:
            CompoundTag or None
        """
        value = content.encode("utf-8")
        length = len(value)
        char_ptr = ctypes.c_char_p(value)
        buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
        handle = get_library_handle().nbt_compound_from_snbt(
            ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)), length
        )
        if handle is not None:
            result = Tag()
            result._tag_handle = handle
            result.__class__ = CompoundTag
            return result
        return None
