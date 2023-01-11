#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'sections_ref',
    'sections_ref.biblio',
    'sections_ref.feature',
]
ENTRY_POINTS = dict(console_scripts=[
    'sections_ref = sections_ref.cli:main',
])

if __name__ == "__main__":
    utila.install(__file__)
