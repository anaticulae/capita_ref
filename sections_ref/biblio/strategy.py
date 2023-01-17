# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sections_ref.biblio.doublecolumn
import sections_ref.biblio.specialchars


def extract(normal: 'spa.Data', oneline: 'spa.Data') -> list:
    special = sections_ref.biblio.specialchars.extract(oneline)
    double = sections_ref.biblio.doublecolumn.extract(normal)
    # select "better" result
    special_sum = sum(item.content.value for item in special)
    double_sum = sum(item.content.value for item in double)
    result = special if special_sum > double_sum else double
    return result
