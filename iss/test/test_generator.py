#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iss import generator

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC

import random
import numpy as np


def test_reads():
    random.seed(42)
    np.random.seed(42)
    ref_genome = SeqRecord(
        Seq(str('CGTTTCAACC' * 40),
            IUPAC.unambiguous_dna
            ),
        id='my_genome',
        description='test genome'
        )
    read_gen = generator.reads(ref_genome, 100, 1, 20, 40)
    big_read = ''.join(
        str(read_tuple[0].seq) + str(read_tuple[1].seq)
        for read_tuple in read_gen
    )
    print(big_read)
    assert big_read == 'ACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCG\
TTTCAACCCGTTTCAACCCGTTTCAACCCGGTTCAACCCGTTTCATGAAACGGGTTGAAACGGGTTGAAACGGGTTGAA\
ACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTGTTTCAACCCGTT\
TCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGTTTCAACCCGT\
TTCAACCCGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACGGGTTGAAACG\
GGTTGAAACGGGTTGAAACGGGTTGAAAC'