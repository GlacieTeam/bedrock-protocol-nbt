# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt import *


def test1():
    nbt = CompoundTag()
    nbt["string_tag"] = StringTag("Test String")
    nbt["byte_tag"] = ByteTag(114)
    nbt["short_tag"] = ShortTag(19132)
    nbt["int_tag"] = IntTag(114514)
    nbt["int64_tag"] = Int64Tag(1145141919810)
    nbt["float_tag"] = FloatTag(114.514)
    nbt["double_tag"] = DoubleTag(3.1415926535897)
    nbt["byte_array_tag"] = ByteArrayTag(b"13276273923")
    nbt["list_tag"] = ListTag([StringTag("1111"), StringTag("2222")])
    nbt["compound_tag"] = nbt
    nbt["int_array_tag"] = IntArrayTag([1, 2, 3, 4, 5, 6, 7])
    print(nbt.to_snbt())


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
    nbt.put_compound("tag_compound", nbt)
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


if __name__ == "__main__":
    print("-" * 25, "Test1", "-" * 25)
    test1()
    print("-" * 25, "Test2", "-" * 25)
    test2()
    print("-" * 25, "Test3", "-" * 25)
    test3()
    print("-" * 25, "END", "-" * 25)
