# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

import os
import platform
import sys
import ctypes
import threading


class NbtIoBuffer(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.POINTER(ctypes.c_uint8)),
        ("size", ctypes.c_size_t),
    ]


class NativeLibrary:
    _lock = threading.Lock()
    _lib_handle = None
    _initialized = False
    _initialization_error = None

    def __init__(self):
        raise RuntimeError("Use get_handle() method instead")

    @classmethod
    def _initialize(cls):
        if cls._initialized or cls._initialization_error is not None:
            return

        arch = platform.machine().lower()
        if arch == "amd64":
            arch = "x86_64"
        elif arch == "aarch64":
            arch = "arm64"

        lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), arch)
        platform_map = {
            "win32": "NBT.dll",
            "linux": "libNBT.so",
            "darwin": "libNBT.dylib",
        }

        if sys.platform not in platform_map:
            cls._initialization_error = OSError(f"Unsupported platform: {sys.platform}")
            raise cls._initialization_error

        lib_name = platform_map[sys.platform]
        dll_path = os.path.join(lib_dir, lib_name)

        if not os.path.isfile(dll_path):
            cls._initialization_error = FileNotFoundError(
                f"Native library not found at: {dll_path}"
            )
            raise cls._initialization_error

        try:
            cls._lib_handle = ctypes.CDLL(dll_path)
            cls._setup_function_prototypes()
            cls._initialized = True
        except Exception as e:
            cls._initialization_error = RuntimeError(
                f"Failed to load native library: {e}"
            )
            raise cls._initialization_error from e

    @classmethod
    def _setup_function_prototypes(cls):
        # AnyTag
        cls._lib_handle.nbtio_buffer_destroy.restype = None
        cls._lib_handle.nbtio_buffer_destroy.argtypes = [ctypes.POINTER(NbtIoBuffer)]
        cls._lib_handle.nbt_any_tag_get_type.restype = ctypes.c_int
        cls._lib_handle.nbt_any_tag_get_type.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_any_tag_equals.restype = ctypes.c_bool
        cls._lib_handle.nbt_any_tag_equals.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        cls._lib_handle.nbt_any_tag_copy.restype = ctypes.c_void_p
        cls._lib_handle.nbt_any_tag_copy.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_any_tag_hash.restype = ctypes.c_size_t
        cls._lib_handle.nbt_any_tag_hash.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_any_tag_write.restype = None
        cls._lib_handle.nbt_any_tag_write.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        cls._lib_handle.nbt_any_tag_load.restype = None
        cls._lib_handle.nbt_any_tag_load.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        cls._lib_handle.nbt_any_tag_destroy.restype = None
        cls._lib_handle.nbt_any_tag_destroy.argtypes = [ctypes.c_void_p]
        # EndTag
        cls._lib_handle.nbt_end_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_end_tag_create.argtypes = []
        # ByteTag
        cls._lib_handle.nbt_byte_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_byte_tag_create.argtypes = [ctypes.c_uint8]
        cls._lib_handle.nbt_byte_tag_set_value.restype = None
        cls._lib_handle.nbt_byte_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint8,
        ]
        cls._lib_handle.nbt_byte_tag_get_value.restype = ctypes.c_uint8
        cls._lib_handle.nbt_byte_tag_get_value.argtypes = [ctypes.c_void_p]
        # ShortTag
        cls._lib_handle.nbt_short_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_short_tag_create.argtypes = [ctypes.c_short]
        cls._lib_handle.nbt_short_tag_set_value.restype = None
        cls._lib_handle.nbt_short_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_short,
        ]
        cls._lib_handle.nbt_short_tag_get_value.restype = ctypes.c_short
        cls._lib_handle.nbt_short_tag_get_value.argtypes = [ctypes.c_void_p]
        # IntTag
        cls._lib_handle.nbt_int_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_int_tag_create.argtypes = [ctypes.c_int32]
        cls._lib_handle.nbt_int_tag_set_value.restype = None
        cls._lib_handle.nbt_int_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int32,
        ]
        cls._lib_handle.nbt_int_tag_get_value.restype = ctypes.c_int32
        cls._lib_handle.nbt_int_tag_get_value.argtypes = [ctypes.c_void_p]
        # Int64Tag
        cls._lib_handle.nbt_int64_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_int64_tag_create.argtypes = [ctypes.c_int64]
        cls._lib_handle.nbt_int64_tag_set_value.restype = None
        cls._lib_handle.nbt_int64_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int64,
        ]
        cls._lib_handle.nbt_int64_tag_get_value.restype = ctypes.c_int64
        cls._lib_handle.nbt_int64_tag_get_value.argtypes = [ctypes.c_void_p]
        # FloatTag
        cls._lib_handle.nbt_float_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_float_tag_create.argtypes = [ctypes.c_float]
        cls._lib_handle.nbt_float_tag_set_value.restype = None
        cls._lib_handle.nbt_float_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_float,
        ]
        cls._lib_handle.nbt_float_tag_get_value.restype = ctypes.c_float
        cls._lib_handle.nbt_float_tag_get_value.argtypes = [ctypes.c_void_p]
        # DoubleTag
        cls._lib_handle.nbt_double_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_double_tag_create.argtypes = [ctypes.c_double]
        cls._lib_handle.nbt_double_tag_set_value.restype = None
        cls._lib_handle.nbt_double_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_double,
        ]
        cls._lib_handle.nbt_double_tag_get_value.restype = ctypes.c_double
        cls._lib_handle.nbt_double_tag_get_value.argtypes = [ctypes.c_void_p]
        # ByteArrayTag
        cls._lib_handle.nbt_byte_array_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_byte_array_tag_create.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_byte_array_tag_set_value.restype = None
        cls._lib_handle.nbt_byte_array_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_byte_array_tag_get_value.restype = NbtIoBuffer
        cls._lib_handle.nbt_byte_array_tag_get_value.argtypes = [ctypes.c_void_p]
        # StringTag
        cls._lib_handle.nbt_string_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_string_tag_create.argtypes = [
            ctypes.c_char_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_string_tag_set_value.restype = None
        cls._lib_handle.nbt_string_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_string_tag_get_value.restype = NbtIoBuffer
        cls._lib_handle.nbt_string_tag_get_value.argtypes = [ctypes.c_void_p]
        # ListTag
        cls._lib_handle.nbt_list_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_list_tag_create.argtypes = []
        cls._lib_handle.nbt_list_tag_size.restype = ctypes.c_size_t
        cls._lib_handle.nbt_list_tag_size.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_list_tag_add_tag.restype = None
        cls._lib_handle.nbt_list_tag_add_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        cls._lib_handle.nbt_list_tag_get_tag.restype = ctypes.c_void_p
        cls._lib_handle.nbt_list_tag_get_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_list_tag_remove_tag.restype = ctypes.c_bool
        cls._lib_handle.nbt_list_tag_remove_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_list_tag_clear.restype = None
        cls._lib_handle.nbt_list_tag_clear.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_list_tag_set_tag.restype = ctypes.c_bool
        cls._lib_handle.nbt_list_tag_set_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_void_p,
        ]
        # CompoundTag
        cls._lib_handle.nbt_compound_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_compound_tag_create.argtypes = []
        cls._lib_handle.nbt_compound_tag_size.restype = ctypes.c_size_t
        cls._lib_handle.nbt_compound_tag_size.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_compound_tag_set_tag.restype = None
        cls._lib_handle.nbt_compound_tag_set_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
            ctypes.c_void_p,
        ]
        cls._lib_handle.nbt_compound_tag_get_tag.restype = ctypes.c_void_p
        cls._lib_handle.nbt_compound_tag_get_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_compound_tag_has_tag.restype = ctypes.c_bool
        cls._lib_handle.nbt_compound_tag_has_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_compound_tag_remove_tag.restype = ctypes.c_bool
        cls._lib_handle.nbt_compound_tag_remove_tag.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_compound_tag_clear.restype = None
        cls._lib_handle.nbt_compound_tag_clear.argtypes = [ctypes.c_void_p]
        # Serializer
        cls._lib_handle.nbt_compound_to_binary_nbt.restype = NbtIoBuffer
        cls._lib_handle.nbt_compound_to_binary_nbt.argtypes = [
            ctypes.c_void_p,
            ctypes.c_bool,
        ]
        cls._lib_handle.nbt_compound_to_network_nbt.restype = NbtIoBuffer
        cls._lib_handle.nbt_compound_to_network_nbt.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_compound_to_snbt.restype = NbtIoBuffer
        cls._lib_handle.nbt_compound_to_snbt.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_uint8,
        ]
        cls._lib_handle.nbt_compound_to_json.restype = NbtIoBuffer
        cls._lib_handle.nbt_compound_to_json.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint8,
        ]
        cls._lib_handle.nbt_compound_from_binary_nbt.restype = ctypes.c_void_p
        cls._lib_handle.nbt_compound_from_binary_nbt.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
            ctypes.c_bool,
        ]
        cls._lib_handle.nbt_compound_from_network_nbt.restype = ctypes.c_void_p
        cls._lib_handle.nbt_compound_from_network_nbt.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_compound_from_snbt.restype = ctypes.c_void_p
        cls._lib_handle.nbt_compound_from_snbt.argtypes = [
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_size_t,
        ]
        # IntArrayTag
        cls._lib_handle.nbt_int_array_tag_create.restype = ctypes.c_void_p
        cls._lib_handle.nbt_int_array_tag_create.argtypes = []
        cls._lib_handle.nbt_int_array_tag_size.restype = ctypes.c_size_t
        cls._lib_handle.nbt_int_array_tag_size.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_int_array_tag_add_value.restype = None
        cls._lib_handle.nbt_int_array_tag_add_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int32,
        ]
        cls._lib_handle.nbt_int_array_tag_get_value.restype = ctypes.c_int32
        cls._lib_handle.nbt_int_array_tag_get_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_int_array_tag_remove_value.restype = ctypes.c_bool
        cls._lib_handle.nbt_int_array_tag_remove_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
        ]
        cls._lib_handle.nbt_int_array_tag_clear.restype = None
        cls._lib_handle.nbt_int_array_tag_clear.argtypes = [ctypes.c_void_p]
        cls._lib_handle.nbt_int_array_tag_set_value.restype = ctypes.c_bool
        cls._lib_handle.nbt_int_array_tag_set_value.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_void_p,
        ]

    @classmethod
    def get_handle(cls):
        if cls._initialized:
            return cls._lib_handle
        if cls._initialization_error:
            raise cls._initialization_error
        with cls._lock:
            if cls._initialized:
                return cls._lib_handle
            if cls._initialization_error:
                raise cls._initialization_error
            try:
                cls._initialize()
            except Exception:
                pass
            if cls._initialization_error:
                raise cls._initialization_error
            return cls._lib_handle


def get_library_handle():
    return NativeLibrary.get_handle()
