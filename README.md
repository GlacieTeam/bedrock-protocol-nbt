# bedrock-protocol-nbt
Part of Bedrock Protocol Library. Minecraft NBT Library.

## Install
```bash
pip install bedrock-protocol-nbt
```

## Usage
```Python
from bedrock_protocol.nbt import *

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
```

# Used Libraries
| Library          | License      | Link                                         |
| ---------------- | ------------ | -------------------------------------------- |
| NBT              | MPL-2.0      | <https://github.com/GlacieTeam/NBT>          |

## License
This project is licensed under the **Mozilla Public License 2.0 (MPL-2.0)**.  

### Key Requirements:
- **Modifications to this project's files** must be released under MPL-2.0.  
- **Using this library in closed-source projects** is allowed (no requirement to disclose your own code).  
- **Patent protection** is explicitly granted to all users.  

For the full license text, see [LICENSE](LICENSE) file or visit [MPL 2.0 Official Page](https://www.mozilla.org/en-US/MPL/2.0/).  

---


### Copyright © 2025 GlacieTeam. All rights reserved.