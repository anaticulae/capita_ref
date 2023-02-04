#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import sections_ref

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

WORKPLAN = [
    utila.create_step(
        'publication',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.File(name='pdfinfo', optional=True),
        ],
        output=('like',),
    ),
    utila.create_step(
        'bibliography',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('groupme', 'hefopa_result'),
            utila.ResultFile('sections_ref', 'publication_like', optional=True),
        ],
        output=('like',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=sections_ref.ROOT,
        featurepackage='sections_ref.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=sections_ref.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            profileflag=True,
            version=sections_ref.__version__,
        ),
    )
