#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utilo

import capita_ref

DESCRIPTION = ('The sections tool analyses every single page of an pdf file '
               'and determines the likelihood to be an feature')

WORKPLAN = [
    utilo.create_step(
        'publication',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.File(name='pdfinfo', optional=True),
        ],
        output=('like',),
    ),
    utilo.create_step(
        'bibliography',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('groupme', 'hefopa_result', optional=True),
            utilo.ResultFile('sections_ref', 'publication_like', optional=True),
        ],
        output=('like',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=capita_ref.ROOT,
        featurepackage='capita_ref.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=capita_ref.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            profileflag=True,
            version=capita_ref.__version__,
        ),
    )
