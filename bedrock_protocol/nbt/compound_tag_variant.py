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
    _index: Union[bytes, str, int]

    def __init__(
        self, parent: Tag, value: Optional[Tag], index: Union[bytes, str, int]
    ):
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

    def __getitem__(
        self, index: Union[bytes, str, int]
    ) -> Optional["CompoundTagVariant"]:
        parent = self._parent()
        if parent is None:
            return None
        result = self._value.get(index)
        if result is None and isinstance(index, (bytes, str)):
            from bedrock_protocol.nbt.compound_tag import CompoundTag

            self._value.set(index, CompoundTag)
            result = self._value.get(index)
        elif isinstance(result, Tag):
            return CompoundTagVariant(self._value, result, index)
        return result

    def __setitem__(self, index: Union[bytes, str, int], value: Tag) -> Any:
        parent = self._parent()
        if parent is None:
            return None
        self._value.set(index, value)
        parent.set(self._index, self._value)

    def __delitem__(self, index: Union[bytes, str, int]) -> bool:
        return self.pop(index)

    def get(self) -> Tag:
        """Get tag in this proxy class
        Returns:
            Tag: _description_
        """
        return self._value

    def get_value(self) -> Any:
        """Get tag value in this proxy class
        Returns:
            Tag: _description_
        """
        return self._value.get()

    def pop(self, index: Union[bytes, str, int]) -> bool:
        parent = self._parent()
        if parent is None:
            return False
        result = self._value.pop(index)
        parent.set(self._index, self._value)
        return result

    def append(self, value: Tag) -> None:
        parent = self._parent()
        if parent is None:
            return False
        if self._value.get_type() == TagType.List:
            self._value.append(value)
            parent.set(self._index, self._value)
        else:
            raise TypeError("Tag is not a ListTag")
