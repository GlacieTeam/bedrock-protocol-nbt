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
    print(nbt.to_json())


if __name__ == "__main__":
    print("-" * 25, "Test1", "-" * 25)
    test1()
    print("-" * 25, "Test2", "-" * 25)
    test2()
