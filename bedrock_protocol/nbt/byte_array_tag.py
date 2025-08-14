# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag
from typing import Union
import ctypes


class ByteArrayTag(Tag):
    """ByteArrayTag

    A Tag contains a byte array (binary data)
    """

    def __init__(self, value: Union[bytearray, bytes, None] = None):
        """Create a ByteArrayTag

        Args:
            value: binary data
        """
        super().__init__()
        if value is not None:
            length = len(value)
            if isinstance(value, bytes):
                char_ptr = ctypes.c_char_p(value)
                buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
            else:
                buf = (ctypes.c_uint8 * length).from_buffer(value)
            self._tag_handle = self._lib_handle.nbt_byte_array_tag_create(
                ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)), length
            )
        else:
            self._tag_handle = self._lib_handle.nbt_byte_array_tag_create(None, 0)

    def set(self, value: Union[bytearray, bytes]) -> None:
        """Set ByteArrayTag value

        Args:
            value: binary data
        """
        length = len(value)
        if isinstance(value, bytes):
            char_ptr = ctypes.c_char_p(value)
            buf = ctypes.cast(char_ptr, ctypes.POINTER(ctypes.c_uint8 * length))
        else:
            buf = (ctypes.c_uint8 * length).from_buffer(value)
        self._lib_handle.nbt_byte_array_tag_set_value(
            self._tag_handle,
            ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint8)),
            length,
        )

    def get(self) -> bytes:
        """Set ByteArrayTag value

        Returns:
            binary data
        """
        buf = self._lib_handle.nbt_byte_array_tag_get_value(self._tag_handle)
        result = bytes(ctypes.string_at(buf.data, buf.size))
        self._lib_handle.nbtio_buffer_destroy(ctypes.byref(buf))
        return result
