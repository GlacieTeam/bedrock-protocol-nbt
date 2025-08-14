# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

from enum import IntEnum


class SnbtFormat(IntEnum):
    Minimize = 0
    PrettyFilePrint = 1
    ArrayLineFeed = 2
    AlwaysLineFeed = 3
    ForceAscii = 4
    ForceQuote = 8
    Classic = 13
    CommentMarks = 16
    Jsonify = 24
