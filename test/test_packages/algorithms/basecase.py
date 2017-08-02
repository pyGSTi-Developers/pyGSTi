import unittest
import pygsti
from pygsti.construction import std1Q_XYI as std
from pygsti.tools.basis import Basis

import numpy as np
from scipy import polyfit
import sys, os

from ..testutils import BaseTestCase, compare_files, temp_files

class AlgorithmsBase(BaseTestCase):
    def setUp(self):
        super(AlgorithmsBase, self).setUp()

        self.gateset = std.gs_target
        self.datagen_gateset = self.gateset.depolarize(gate_noise=0.05, spam_noise=0.1)

        self.fiducials = std.fiducials
        self.germs = std.germs
        self.specs = pygsti.construction.build_spam_specs(self.fiducials, effect_labels=['E0']) #only use the first EVec

        self.gateLabels = list(self.gateset.gates.keys()) # also == std.gates
        self.lgstStrings = pygsti.construction.list_lgst_gatestrings(self.specs, self.gateLabels)

        self.maxLengthList = [0,1,2,4,8]

        self.elgstStrings = pygsti.construction.make_elgst_lists(
            self.gateLabels, self.germs, self.maxLengthList )

        self.lsgstStrings = pygsti.construction.make_lsgst_lists(
            self.gateLabels, self.fiducials, self.fiducials, self.germs, self.maxLengthList )

        #Created in testAnalysis...
        self.ds = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/analysis.dataset")

        ##UNCOMMENT to create LGST analysis dataset
        #ds_lgst = pygsti.construction.generate_fake_data(self.datagen_gateset, self.lgstStrings,
        #   nSamples=10000,sampleError='binomial', seed=100)
        #ds_lgst.save(compare_files + "/analysis_lgst.dataset")
        self.ds_lgst = pygsti.objects.DataSet(fileToLoadFrom=compare_files + "/analysis_lgst.dataset")
