import unittest
import pygsti
import os
import numpy as np
from pygsti.construction import std1Q_XYI as std
import pygsti.tools.basis as basis

class JamiolkowskiTestCase(unittest.TestCase):

    def setUp(self):
        # move working directories
        self.old = os.getcwd()
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

        #Set GateSet objects to "strict" mode for testing
        pygsti.objects.GateSet._strict = True


        # density matrix == 3x3 block diagonal matrix: a 2x2 block followed by a 1x1 block
        self.stateSpaceDims = [2,1]

        #labels which give a tensor product interp. for the states within each density matrix block
        self.stateSpaceLabels = [('Qhappy',),('Lsad',)]

        #Build a test gate   -- old # X(pi,Qhappy)*LX(pi,0,2)
        self.testGate = pygsti.construction.build_gate( self.stateSpaceDims, self.stateSpaceLabels, "LX(pi,0,2)","std")
        self.testGateGM_mx = basis.change_basis(self.testGate, 'std', 'gm', self.stateSpaceDims)
        self.expTestGate_mx = basis.resize_mx(self.testGate, self.stateSpaceDims, resize='expand')
        self.expTestGateGM_mx = basis.change_basis(self.expTestGate_mx, 'std', 'gm')

    def tearDown(self):
        os.chdir(self.old)

    def checkBasis(self, cmb):
        #Op with Jamio map on gate in std and gm bases
        Jmx1 = pygsti.jamiolkowski_iso(self.testGate, gateMxBasis='std',
                                       choiMxBasis=cmb, dimOrStateSpaceDims=self.stateSpaceDims)
        Jmx2 = pygsti.jamiolkowski_iso(self.testGateGM_mx, gateMxBasis='gm',
                                       choiMxBasis=cmb, dimOrStateSpaceDims=self.stateSpaceDims)

        #Make sure these yield the same trace == 1 matrix
        self.assertArraysAlmostEqual(Jmx1,Jmx2)
        self.assertAlmostEqual(np.trace(Jmx1), 1.0)

        #Op on expanded gate in std and gm bases
        JmxExp1 = pygsti.jamiolkowski_iso(self.expTestGate_mx,gateMxBasis='std',choiMxBasis=cmb)
        JmxExp2 = pygsti.jamiolkowski_iso(self.expTestGateGM_mx,gateMxBasis='gm',choiMxBasis=cmb)

        #Make sure these are the same as operating on the contracted basis
        self.assertArraysAlmostEqual(Jmx1,JmxExp1)
        self.assertArraysAlmostEqual(Jmx1,JmxExp2)

        #Reverse transform should yield back the gate matrix
        revTestGate_mx = pygsti.jamiolkowski_iso_inv(Jmx1,choiMxBasis=cmb,
                                                                   dimOrStateSpaceDims=self.stateSpaceDims,
                                                                   gateMxBasis='gm')
        self.assertArraysAlmostEqual(revTestGate_mx, self.testGateGM_mx)

        #Reverse transform without specifying stateSpaceDims, then contraction, should yield same result
        revExpTestGate_mx = pygsti.jamiolkowski_iso_inv(Jmx1,choiMxBasis=cmb,
                                                                      gateMxBasis='std')
        self.assertArraysAlmostEqual( basis.resize_mx(revExpTestGate_mx,self.stateSpaceDims, resize='contract'),
                                      self.testGate)


    def assertArraysAlmostEqual(self,a,b):
        self.assertAlmostEqual( np.linalg.norm(a-b), 0 )

class TestJamiolkowskiMethods(JamiolkowskiTestCase):

    def test_std_basis(self):
        cmb = 'std' #choi matrix basis
        self.checkBasis(cmb)

    def test_gm_basis(self):
        cmb = 'gm' #choi matrix basis
        self.checkBasis(cmb)


    def test_jamiolkowski_ops(self):
        mxGM  = np.array([[1, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0,-1, 0, 0],
                          [0, 0, 0, 1]], 'complex')

        mxStd = basis.change_basis(mxGM, 'gm', 'std')
        mxPP  = basis.change_basis(mxGM, 'gm', 'pp')

        choiStd = pygsti.jamiolkowski_iso(mxStd, "std","std")
        choiStd2 = pygsti.jamiolkowski_iso(mxGM, "gm","std")
        choiStd3 = pygsti.jamiolkowski_iso(mxPP, "pp","std")
        fastChoiStd = pygsti.fast_jamiolkowski_iso_std(mxStd, "std")
        fastChoiStd2 = pygsti.fast_jamiolkowski_iso_std(mxGM, "gm")
        fastChoiStd3 = pygsti.fast_jamiolkowski_iso_std(mxPP, "pp")

        choiGM = pygsti.jamiolkowski_iso(mxStd, "std","gm")
        choiGM2 = pygsti.jamiolkowski_iso(mxGM, "gm","gm")
        choiGM3 = pygsti.jamiolkowski_iso(mxPP, "pp","gm")

        choiPP = pygsti.jamiolkowski_iso(mxStd, "std","pp")
        choiPP2 = pygsti.jamiolkowski_iso(mxGM, "gm","pp")
        choiPP3 = pygsti.jamiolkowski_iso(mxPP, "pp","pp")

        self.assertArraysAlmostEqual( choiStd, choiStd2)
        self.assertArraysAlmostEqual( choiStd, choiStd3)
        self.assertArraysAlmostEqual( choiStd, fastChoiStd)
        self.assertArraysAlmostEqual( choiStd, fastChoiStd2)
        self.assertArraysAlmostEqual( choiStd, fastChoiStd3)
        self.assertArraysAlmostEqual( choiGM, choiGM2)
        self.assertArraysAlmostEqual( choiGM, choiGM3)
        self.assertArraysAlmostEqual( choiPP, choiPP2)
        self.assertArraysAlmostEqual( choiPP, choiPP3)

        gateStd = pygsti.jamiolkowski_iso_inv(choiStd, "std","std")
        gateStd2 = pygsti.jamiolkowski_iso_inv(choiGM, "gm","std")
        gateStd3 = pygsti.jamiolkowski_iso_inv(choiPP, "pp","std")

        gateGM = pygsti.jamiolkowski_iso_inv(choiStd, "std","gm")
        gateGM2 = pygsti.jamiolkowski_iso_inv(choiGM, "gm","gm")
        gateGM3 = pygsti.jamiolkowski_iso_inv(choiPP, "pp","gm")

        gatePP = pygsti.jamiolkowski_iso_inv(choiStd, "std","pp")
        gatePP2 = pygsti.jamiolkowski_iso_inv(choiGM, "gm","pp")
        gatePP3 = pygsti.jamiolkowski_iso_inv(choiPP, "pp","pp")

        fastGateStd = pygsti.fast_jamiolkowski_iso_std_inv(choiStd, "std")
        fastGateGM  = pygsti.fast_jamiolkowski_iso_std_inv(choiStd, "gm")
        fastGatePP  = pygsti.fast_jamiolkowski_iso_std_inv(choiStd, "pp")

        self.assertArraysAlmostEqual( gateStd, mxStd)
        self.assertArraysAlmostEqual( gateStd2, mxStd)
        self.assertArraysAlmostEqual( gateStd3, mxStd)
        self.assertArraysAlmostEqual( fastGateStd, mxStd)

        self.assertArraysAlmostEqual( gateGM,  mxGM)
        self.assertArraysAlmostEqual( gateGM2, mxGM)
        self.assertArraysAlmostEqual( gateGM3, mxGM)
        self.assertArraysAlmostEqual( fastGateGM, mxGM)

        self.assertArraysAlmostEqual( gatePP,  mxPP)
        self.assertArraysAlmostEqual( gatePP2, mxPP)
        self.assertArraysAlmostEqual( gatePP3, mxPP)
        self.assertArraysAlmostEqual( fastGatePP, mxPP)


        with self.assertRaises(NotImplementedError):
            pygsti.jamiolkowski_iso(mxStd, "foobar","gm") #invalid gate basis
        with self.assertRaises(NotImplementedError):
            pygsti.jamiolkowski_iso(mxStd, "std","foobar") #invalid choi basis
        with self.assertRaises(NotImplementedError):
            pygsti.jamiolkowski_iso_inv(choiStd, "foobar","gm") #invalid choi basis
        with self.assertRaises(NotImplementedError):
            pygsti.jamiolkowski_iso_inv(choiStd, "std","foobar") #invalid gate basis

        sumOfNeg  = pygsti.sum_of_negative_choi_evals(std.gs_target)
        sumsOfNeg = pygsti.sums_of_negative_choi_evals(std.gs_target)
        magsOfNeg = pygsti.mags_of_negative_choi_evals(std.gs_target)
        self.assertAlmostEqual(sumOfNeg, 0.0)
        self.assertArraysAlmostEqual(sumsOfNeg, np.zeros(3,'d')) # 3 gates in std.gs_target
        self.assertArraysAlmostEqual(magsOfNeg, np.zeros(12,'d')) # 3 gates * 4 evals each = 12

if __name__ == "__main__":
    unittest.main(verbosity=2)
