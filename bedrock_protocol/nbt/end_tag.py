# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from bedrock_protocol.nbt._internal.native_library import get_library_handle
from bedrock_protocol.nbt.tag import Tag


class EndTag(Tag):
    """EndTag"""

    def __init__(self):
        """Create an EndTag"""
        self._lib_handle = get_library_handle()
        self._tag_handle = self._lib_handle.nbt_end_tag_create()
