import unittest
from SimPEG import *
import matplotlib.pyplot as plt
from simpegem1d import EM1D, EM1DAnalytics, BaseEM1D, DigFilter, EM1DSurveyFD
import numpy as np


class EM1D_FD_Jac_layers_ProblemTests(unittest.TestCase):

    def setUp(self):

        FDsurvey = EM1DSurveyFD()
        FDsurvey.rx_location = np.array([0., 0., 100.+50.])
        FDsurvey.src_location = np.array([0., 0., 100.+50.])
        FDsurvey.field_type = 'secondary'

        nearthick = np.logspace(-1, 1, 2)
        deepthick = np.logspace(1, 2, 5)
        hx = np.r_[nearthick, deepthick]

        mesh1D = Mesh.TensorMesh([hx], [0.])
        depth = -mesh1D.gridN[:-1]
        n_layer = depth.size
        topo = np.r_[0., 0., 100.]
        FDsurvey.depth = depth
        FDsurvey.topo = topo

        FDsurvey.frequency = np.logspace(2, 4, 10)
        sig_half = 1e-1
        chi_half = 0.

        expmap = Maps.ExpMap(mesh1D)
        tau = 1e-3
        eta = 2e-1
        c = 1.

        modelReal = expmap
        m_1D = np.log(np.ones(n_layer)*sig_half)

        FDsurvey.rxType = 'Hz'

        prob = EM1D(mesh1D, sigmaMap = modelReal)
        prob.pair(FDsurvey)
        prob.chi = np.zeros(FDsurvey.n_layer)

        self.survey = FDsurvey
        self.modelReal = modelReal
        self.prob = prob
        self.mesh1D = mesh1D
        self.showIt = False


    def test_EM1DFDJvec_Layers(self):
        self.prob.CondType = 'Real'
        self.prob.survey.src_type = 'CircularLoop'

        I = 1e0
        a = 1e1
        self.prob.survey.I = I
        self.prob.survey.a = a

        sig_half = 0.01
        sig_blk = 0.1
        sig = np.ones(self.prob.survey.n_layer)*sig_half
        sig[3] = sig_blk
        m_1D = np.log(sig)

        self.prob.jacSwitch = True
        Hz, dHzdsig = self.prob.fields(m_1D)

        def fwdfun(m):
            self.prob.jacSwitch = False
            resp = self.prob.survey.dpred(m)
            return resp
            # return Hz

        def jacfun(m, dm):
            self.prob.jacSwitch = True
            f = self.prob.fields(m)
            Jvec = self.prob.Jvec(m, dm, f=f)
            return Jvec

        dm = m_1D*0.5
        derChk = lambda m: [fwdfun(m), lambda mx: jacfun(m, mx)]
        passed = Tests.checkDerivative(derChk, m_1D, num=4, dx = dm, plotIt=False, eps = 1e-15)

        if self.showIt == True:

            ilay = 3
            temp_r = Utils.mkvc((dHzdsig[:,ilay].copy()).real)
            temp_i = Utils.mkvc((dHzdsig[:,ilay].copy()).imag)
            frequency = Utils.mkvc(self.prob.survey.frequency)

            plt.loglog(frequency[temp_r>0], temp_r[temp_r>0], 'b.-')
            plt.loglog(frequency[temp_r<0], -temp_r[temp_r<0], 'b.--')
            plt.loglog(frequency[temp_i>0], temp_i[temp_i>0], 'r.-')
            plt.loglog(frequency[temp_i<0], -temp_i[temp_i<0], 'r.--')
            plt.show()

        if passed:
            print ("EM1DFD-layers Jvec works")

    def test_EM1DFDJtvec_Layers(self):
        self.prob.CondType = 'Real'
        self.prob.survey.src_type = 'CircularLoop'

        I = 1e0
        a = 1e1
        self.prob.survey.I = I
        self.prob.survey.a = a

        sig_half = 0.01
        sig_blk = 0.1
        sig = np.ones(self.prob.survey.n_layer)*sig_half
        sig[3] = sig_blk
        m_true = np.log(sig)

        self.prob.jacSwitch = False
        Hz_true = self.prob.fields(m_true)
        dobs = self.prob.survey.projectFields(u=Hz_true)

        m_ini  = np.log(np.ones(self.prob.survey.n_layer)*sig_half)
        Hz_ini = self.prob.fields(m_ini)
        resp_ini = self.prob.survey.projectFields(u=Hz_ini)
        dr = resp_ini-dobs

        def misfit(m, dobs):
            self.prob.jacSwitch = True
            Hz = self.prob.fields(m)
            dpred = self.survey.dpred(m, f = Hz)
            misfit = 0.5*np.linalg.norm(dpred-dobs)**2
            dmisfit = self.prob.Jtvec(m, dr, f = Hz)
            return misfit, dmisfit

        derChk = lambda m: misfit(m, dobs)
        passed = Tests.checkDerivative(derChk, m_ini, num=4, plotIt=False, eps = 1e-27)
        self.assertTrue(passed)
        if passed:
            print ("EM1DFD-layers Jtvec works")


if __name__ == '__main__':
    unittest.main()
_
