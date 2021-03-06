import unittest
from SimPEG import *
import matplotlib.pyplot as plt
from simpegem1d import EM1D, EM1DAnal, BaseEM1D, DigFilter
from simpegem1d.Waveform import TriangleFun, TriangleFunDeriv


class EM1D_TD_general_Jac_layers_ProblemTests(unittest.TestCase):

    def setUp(self):

        TDsurvey = BaseEM1D.EM1DSurveyTD()
        TDsurvey.rxLoc = np.array([0., 0., 100.+50.])
        TDsurvey.srcLoc = np.array([0., 0., 100.+50.])
        TDsurvey.fieldtype = 'secondary'
        # TDsurvey.rxType = 'Bz'
        TDsurvey.rxType = 'dBzdt'
        TDsurvey.waveType = 'general'

        ta = 5.5*1e-4
        tb = 1.1*1e-3

        tonw = np.linspace(1e-6, tb, 2**9+1)
        dt = tonw[1]-tonw[0]
        toffw = np.linspace(tb+dt, tb+(2**13)*dt, 2**13)
        tconv = np.r_[tonw, toffw]

        waveform = TriangleFun(tconv, ta, tb)
        waveformDeriv = TriangleFunDeriv(tconv, ta, tb)
        tend = 0.01
        optionswave = {'toff': tb,'tconv': tconv,'waveform': waveform, 'waveformDeriv': waveformDeriv }
        TDsurvey.srcType = 'CircularLoop'

        I = 1e0
        a = 1e1

        TDsurvey.I = I
        TDsurvey.a = a

        TDsurvey.time = np.logspace(-5, -2, 64)+tb
        TDsurvey.setWaveform(**optionswave)
        TDsurvey.switchInterp = True
        TDsurvey.setFrequency(tconv)

        nearthick = np.logspace(-1, 1, 2)
        deepthick = np.logspace(1, 2, 2)
        hx = np.r_[nearthick, deepthick]

        mesh1D = Mesh.TensorMesh([hx], [0.])
        depth = -mesh1D.gridN[:-1]
        LocSigZ = -mesh1D.gridCC
        nlay = depth.size
        topo = np.r_[0., 0., 100.]
        TDsurvey.depth = depth
        TDsurvey.topo = topo
        TDsurvey.LocSigZ = LocSigZ
        TDsurvey.HalfSwitch = False
        TDsurvey.Setup1Dsystem()



        sig_half = 1e-1
        chi_half = 0.

        expmap = BaseEM1D.BaseEM1DMap(mesh1D)
        tau = 1e-3
        eta = 2e-1
        c = 1.
        options = {'Frequency': TDsurvey.frequency, 'tau': np.ones(nlay)*tau, 'eta':np.ones(nlay)*eta, 'c':np.ones(nlay)*c}
        colemap = BaseEM1D.BaseColeColeMap(mesh1D, **options)

        modelReal = expmap
        modelComplex = colemap * expmap
        m_1D = np.log(np.ones(nlay)*sig_half)

        WT0, WT1, YBASE = DigFilter.LoadWeights()
        options = {'WT0': WT0, 'WT1': WT1, 'YBASE': YBASE}

        prob = EM1D.EM1D(mesh1D, modelReal, **options)
        prob.pair(TDsurvey)
        prob.chi = np.zeros(TDsurvey.nlay)


        self.survey = TDsurvey
        self.options = options
        self.modelReal = modelReal
        self.prob = prob
        self.mesh1D = mesh1D
        self.showIt = False


    def test_EM1DTDJvec_Layers(self):
        self.prob.CondType = 'Real'

        sig_half = 0.001
        sig = np.ones(self.prob.survey.nlay)*sig_half
        m_1D = np.log(sig)

        def fwdfun(m):
            self.prob.jacSwitch = False
            resp = self.prob.survey.dpred(m)
            return resp

        def jacfun(m, dm):
            self.prob.jacSwitch = True
            u = self.prob.fields(m)
            Jvec = self.prob.Jvec(m, dm, u = u)
            return Jvec

        dm = m_1D*2
        derChk = lambda m: [fwdfun(m), lambda mx: jacfun(m, mx)]
        passed = Tests.checkDerivative(derChk, m_1D, num=2, dx = dm, plotIt=False, eps = 1e-15)

        if passed:
            print "EM1DTD-Layers Jvec works"

    def test_EM1DTDJtvec_Half(self):
        self.prob.CondType = 'Real'

        sig_half = 0.001
        sig_blk = 1
        sig = np.ones(self.prob.survey.nlay)*sig_half
        sig[3] = sig_blk

        m_true = np.log(sig)
        Hz_true = self.prob.fields(m_true)
        dobs = self.prob.survey.projectFields(u=Hz_true)

        m_ini  = np.log(np.ones(self.prob.survey.nlay)*sig_half*2)
        Hz_ini = self.prob.fields(m_ini)
        resp_ini = self.prob.survey.projectFields(u=Hz_ini)
        dr = resp_ini-dobs

        def misfit(m, dobs):
            self.prob.jacSwitch = True
            Hz = self.prob.fields(m)
            dpred = self.survey.dpred(m, u = Hz)
            misfit = 0.5*np.linalg.norm(dpred-dobs)**2
            dmisfit = self.prob.Jtvec(m, dr, u = Hz)
            return misfit, dmisfit

        derChk = lambda m: misfit(m, dobs)
        passed = Tests.checkDerivative(derChk, m_ini, num=3, plotIt=False, eps = 1e-26)
        self.assertTrue(passed)
        if passed:
            print "EM1DTD-layers Jtvec works"

if __name__ == '__main__':
    unittest.main()
