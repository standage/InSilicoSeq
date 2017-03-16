#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Bio.Seq import MutableSeq
from Bio.SeqRecord import SeqRecord

import random
import numpy as np


def phred_to_prob(q):
    """Given a phred score q, return the probabilty p
    of the call being RIGHT"""
    p = 10 ** (-q / 10)
    return 1 - p


def prob_to_phred(p):
    """Given the probablity p of a basecall being RIGHT
    return the phred score"""
    q = int(round(-10 * np.log10(1 - p)))
    return q


def introduce_error_scores(record, mean_qual):
    """Add phred scores to a SeqRecord according to the basic error_model"""
    record.letter_annotations["phred_quality"] = basic(
        phred_to_prob(mean_qual), 0.01, len(record))
    return record


def introduce_advanced_scores(record, histograms):
    """Add phred scores to a SeqRecord according to the basic error_model"""
    record.letter_annotations["phred_quality"] = advanced(
        histograms)
    return record


def mut_seq(record):
    """modify the nucleotides of a SeqRecord according to the phred scores.
    Return a sequence"""
    nucl_choices = {
        'A': ['T', 'C', 'G'],
        'T': ['A', 'C', 'G'],
        'C': ['A', 'T', 'G'],
        'G': ['A', 'T', 'C']
        }
    mutable_seq = record.seq.tomutable()
    quality_list = record.letter_annotations["phred_quality"]
    position = 0
    for nucl, qual in zip(mutable_seq, quality_list):
        if random.random() > phred_to_prob(qual):
            mutable_seq[position] = random.choice(nucl_choices[nucl])
        position += 1
    return mutable_seq.toseq()


def basic(mean, stdev, length):
    """Generate a normal distribution, transform to phred scores"""
    # rate = 1
    norm = [min(q, 0.9999) for q in np.random.normal(mean, stdev, length)]
    # inverse transform sampling ? or lognormal distribution ?
    # uni = [min(q, 0.9999) for q in np.random.uniform()]
    # exp = [np.log(1 - q) / (- rate) for q in norm]
    phred = [prob_to_phred(p) for p in norm]
    return phred


def load_npy(numpy_file):
    """load the error profile npy file"""
    histograms = np.load(numpy_file)
    return histograms


def advanced(histograms):
    """Generate a list of phred scores based on real datasets"""
    phred_list = []
    for hist in histograms:
        values, indices = hist
        weights = values / np.sum(values)
        random_quality = np.random.choice(
            indices[1:], p=weights
        )
        phred_list.append(round(random_quality))
    return phred_list