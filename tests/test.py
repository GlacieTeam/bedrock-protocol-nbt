# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

import ctypes
from bedrock_protocol.nbt import *
from bedrock_protocol.binarystream import *


def test1():
    nbt = CompoundTag(
        {
            "string_tag": "Test String",
            "byte_tag": ctypes.c_ubyte(114),
            "bool_tag": False,
            "short_tag": ctypes.c_int16(65536),
            "int_tag": 114514,
            "test_list": ["237892", "homo", "114514"],
        }
    )
    nbt["test"]["int64_tag"] = ctypes.c_int64(1145141919810)
    nbt["test"]["float_tag"] = 114.514
    nbt["test"]["double_tag"] = ctypes.c_double(3.1415926535897)
    nbt["byte_array_tag"] = b"13276273923"
    nbt["list_tag"] = ["aaaaa", "bbbbb"]
    nbt["list_tag"].append("Homo")
    nbt["compound_tag"] = nbt
    nbt["int_array_tag"] = IntArrayTag([1, 2, 3, 4, 5, 6, 7])
    print(nbt.to_snbt())
    print(f'{nbt["test"]["double_tag"].get()}')
    print(f'{nbt["not_exist"]["not_exist"].get()}')
    print(f'{nbt["compound_tag"].get()}')
    print(f'{nbt["list_tag"][0].value()}')


def test2():
    snbt = '{"byte_array_tag": [B;49b, 51b, 50b, 55b, 54b, 50b, 55b, 51b, 57b, 50b, 51b],"double_tag": 3.141593,"byte_tag": 114b}'
    nbt = CompoundTag.from_snbt(snbt)
    # print(nbt.to_json())
    bnbt = nbt.to_binary_nbt()
    print(bnbt.hex())
    rnbt = CompoundTag.from_binary_nbt(bnbt)
    print(rnbt.to_snbt())


def test3():
    nbt = CompoundTag()
    nbt.put_string("tag_string", "aaaaa")
    nbt.put_binary_string("tag_binary_string", b"12345")
    nbt.put_byte("tag_byte", 114)
    nbt.put_short("tag_short", 26378)
    nbt.put_int("tag_int", 890567)
    nbt.put_int64("tag_int64", 3548543263748543827)
    nbt.put_float("tag_float", 1.2345)
    nbt.put_double("tag_double", 1.414213562)
    nbt.put_byte_array("tag_byte_array", b"45678909876")
    nbt.put_list("tag_list", [nbt, nbt])
    nbt.put_int_array("tag_int_array", [1, 2, 3, 4, 5, 6, 7])
    nbt.put_compound("tag_compound", {})
    print(nbt.to_snbt())
    print(f'{nbt.get_string("tag_string")}')
    print(f'{nbt.get_binary_string("tag_binary_string")}')
    print(f'{nbt.get_byte("tag_byte")}')
    print(f'{nbt.get_short("tag_short")}')
    print(f'{nbt.get_int("tag_int")}')
    print(f'{nbt.get_int64("tag_int64")}')
    print(f'{nbt.get_float("tag_float")}')
    print(f'{nbt.get_double("tag_double")}')
    print(f'{nbt.get_byte_array("tag_byte_array")}')
    print(f'{nbt.get_list("tag_list")}')
    print(f'{nbt.get_compound("tag_compound")}')
    print(f'{nbt.get_int_array("tag_int_array")}')
    print(f'{nbt.get_byte("not exist")}')


def test4():
    testnbt = CompoundTag(
        {
            "string_tag": StringTag("Test String"),
            "byte_tag": ByteTag(114),
            "short_tag": ShortTag(19132),
            "int_tag": IntTag(114514),
        }
    )
    stream = BinaryStream()
    stream.write_byte(23)
    testnbt.write(stream)
    buffer = stream.data()
    print(
        f"{buffer.hex()} | {buffer.hex() == '170a000108627974655f746167720307696e745f746167a4fd0d020973686f72745f746167bc4a080a737472696e675f7461670b5465737420537472696e6700'}"
    )

    print(f"{stream.get_byte()}")
    nbt = CompoundTag()
    nbt.read(stream)
    print(f"{nbt.to_snbt()}")
    nbt["aaa"]["bbb"] = [
        {"a": "b", "1": "2"},
        {"c": "d", "3": 4},
        {"e": "f", "5": True},
    ]
    mergeNbt = CompoundTag(
        {
            "string_tag": "merge string",
            "byte_array_tag": b"114514",
            "aaa": {"bbb": [{"c": "d", "3": 4}, {"g": "h", "7": ShortTag(8)}]},
        }
    )
    nbt.merge(mergeNbt, True)
    print(nbt.to_snbt())


if __name__ == "__main__":
    print("-" * 25, "Test1", "-" * 25)
    test1()
    print("-" * 25, "Test2", "-" * 25)
    test2()
    print("-" * 25, "Test3", "-" * 25)
    test3()
    print("-" * 25, "Test4", "-" * 25)
    test4()
    print("-" * 25, "END", "-" * 25)
