# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag
from typing import Union
import ctypes


class StringTag(Tag):
    """StringTag

    A Tag contains a std::string (C++ type)

    Note:
        std::string is different from str in Python
        std::string is same as bytearray in Python

    Warning:
        StringTag may contains binary data
    """

    def __init__(self, value: Union[str, bytes, bytearray]):
        """Create a StringTag

        Args:
            value: str / bytes / bytearray (can be binary data)
        """
        super().__init__()
        length = len(value)
        if isinstance(value, str):
            data = value.encode("utf-8")
            char_ptr = ctypes.c_char_p(data)
        elif isinstance(value, bytes):
            char_ptr = ctypes.c_char_p(value)
        else:
            char_ptr = (ctypes.c_char * length).from_buffer(value)
        self._tag_handle = self._lib_handle.nbt_string_tag_create(char_ptr, length)

    def set(self, value: Union[str, bytes, bytearray]) -> None:
        """Set StringTag value

        Args:
            value: str / bytes / bytearray (can be binary data)
        """
        length = len(value)
        if isinstance(value, str):
            data = value.encode("utf-8")
            char_ptr = ctypes.c_char_p(data)
        elif isinstance(value, bytes):
            char_ptr = ctypes.c_char_p(value)
        else:
            char_ptr = (ctypes.c_char * length).from_buffer(value)
        self._lib_handle.nbt_string_tag_set_value(self._tag_handle, char_ptr, length)

    def get(self) -> bytes:
        """Get StringTag value

        Returns:
            bytes (binary data, if you are sure it is a text, you can use get_str() instead)
        """
        buf = self._lib_handle.nbt_string_tag_get_value(self._tag_handle)
        result = bytes(ctypes.string_at(buf.data, buf.size))
        self._lib_handle.nbtio_buffer_destroy(ctypes.byref(buf))
        return result

    def get_str(self) -> str:
        """Get StringTag value as str

        Returns:
            Text string
        """
        data = self.get()
        try:
            if data is not None:
                return data.decode("utf-8")
            return ""
        except UnicodeDecodeError:
            return ""
