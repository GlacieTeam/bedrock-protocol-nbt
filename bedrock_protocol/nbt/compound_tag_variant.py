# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt.tag import Tag
from bedrock_protocol.nbt.tag_type import TagType
from typing import Optional, Union, Any
import weakref


class CompoundTagVariant:
    """A proxy class to get / set CompoundTag value"""

    _parent: "weakref.ref[Tag]"
    _value: Optional[Tag]
    _index: Union[str, int]

    def __init__(self, parent: Tag, value: Optional[Tag], index: Union[str, int]):
        """
        Warning:
            Internal function
            Do not construct this type
        """
        if not isinstance(parent, Tag):
            raise TypeError("Type is not a Tag")
        self._parent = weakref.ref(parent)
        self._value = value
        self._index = index

    def __getitem__(self, index: Union[str, int]) -> Optional["CompoundTagVariant"]:
        parent = self._parent()
        if parent is None:
            return None
        result = self._value.get(index)
        if result is None and isinstance(index, str):
            from bedrock_protocol.nbt.compound_tag import CompoundTag

            if self._value.get_type() == TagType.Compound:
                self._value.put(index, CompoundTag())
            else:
                self._value.set(index, CompoundTag())
            result = self._value.get(index)
            return CompoundTagVariant(self._value, result, index)
        elif isinstance(result, Tag):
            return CompoundTagVariant(self._value, result, index)
        return result

    def __setitem__(self, index: Union[str, int], value: Any) -> Any:
        parent = self._parent()
        if parent is None:
            return None
        if self._value.get_type() == TagType.Compound:
            self._value.put(index, value)
        else:
            self._value.set(index, value)
        if parent.get_type() == TagType.Compound:
            parent.put(self._index, self._value)
        else:
            parent.set(self._index, self._value)

    def __delitem__(self, index: Union[str, int]) -> bool:
        return self.pop(index)

    def get_type(self) -> TagType:
        """
        Returns:
            the tag type.
        """
        return self.get().get_type()

    def get(self) -> Tag:
        """Get tag in this proxy class
        Returns:
            the tag
        """
        return self._value

    def value(self) -> Any:
        """Get tag value in this proxy class
        Returns:
            tag value
        """
        if self._value is not None:
            if self._value.get_type() == TagType.Compound:
                return self._value.get_tag_map()
            elif self._value.get_type() == TagType.List:
                return self._value.get_list()
            else:
                return self._value.get()
        return None

    def copy_tag(self) -> Tag:
        """
        Returns:
            Tag: the deep copy of this tag
        """
        return self.get().deep_copy()

    def is_object(self):
        return self.get_type() == TagType.Compound

    def is_array(self):
        return self.get_type() == TagType.List

    def is_integer(self):
        return (
            self.get_type() == TagType.Byte
            or self.get_type() == TagType.Short
            or self.get_type() == TagType.Int
            or self.get_type() == TagType.Int64
        )

    def is_float(self):
        return self.get_type() == TagType.Float or self.get_type() == TagType.Double

    def is_binary(self):
        return (
            self.get_type() == TagType.ByteArray or self.get_type() == TagType.IntArray
        )

    def is_string(self):
        return self.get_type() == TagType.String

    def pop(self, index: Union[str, int]) -> bool:
        parent = self._parent()
        if parent is None:
            return False
        result = self._value.pop(index)
        parent.set(self._index, self._value)
        return result

    def append(self, value: Any) -> None:
        """Append a tag to the end of the ListTag
        Args:
            value: any Tag type
        """
        parent = self._parent()
        if parent is None:
            return False
        if self._value.get_type() == TagType.List:
            self._value.append(value)
            if parent.get_type() == TagType.Compound:
                parent.put(self._index, self._value)
            else:
                parent.set(self._index, self._value)
        else:
            raise TypeError("Tag is not a ListTag")

    def to_snbt(self):
        """Encode the Tag to network NBT format
        Returns:
            serialized snbt string
        """
        return self.get().to_snbt()

    def to_json(self):
        """Encode the CompoundTag to JSON
        Returns:
            serialized json string

        Warning:
            JSON can NOT be deserialized to NBT
        """
        return self.get().to_json()
