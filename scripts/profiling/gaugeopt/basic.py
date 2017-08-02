#!/usr/bin/env python3
from pygsti.algorithms import gaugeopt_to_target
from pygsti.tools import timed_block

import pickle
from contextlib import contextmanager

from load import load

def main():
    gs, gs_target = load()
    #envSettings = dict(MKL_NUM_THREADS=1, NUMEXPR_NUM_THREADS=1, OMP_NUM_THREADS=1)

    with timed_block('Basic gauge opt:'):
        gs_gaugeopt = gaugeopt_to_target(gs, gs_target, 
                itemWeights={'spam' : 0.0001, 'gates':1.0},
                spamMetric='frobenius',
                gatesMetric='frobenius')

if __name__ == '__main__':
    main()
