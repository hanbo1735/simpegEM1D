"""

:mod:`Waveforms` -- Known current Waveforms for airborne EM systems
==================================================================

XXX


"""

import numpy as np


class CurrentWaveforms:
    """Simple Class for CurrentWaveforms."""
    def __init__(self, name):
        """Add the filter name."""
        self.name = name


def skytem_HM_2015():
    """
        SkyTEM High moment (HM) current waveform
    """

    waveform = CurrentWaveforms('skytem high moment 2015')

    waveform.base_frequency = "30 Hz"
    waveform.currrent_amplitude = "122.5 A"
    waveform.current_times = np.array([
        -2.06670E-02,
        -2.05770E-02,
        -2.04670E-02,
        -1.66670E-02,
        -1.64726E-02,
        -1.64720E-02,
        -1.64706E-02,
        -4.00000E-03,
        -3.91000E-03,
        -3.80000E-03,
        0.00000E+00,
        1.94367E-04,
        1.95038E-04,
        1.96368E-04
    ])

    waveform.currents = np.array([
        0.00000E+00,
        -5.30000E-01,
        -9.73000E-01,
        -1.00000E+00,
        -2.81610E-03,
        -1.44356E-03,
        0.00000E+00,
        0.00000E+00,
        5.30000E-01,
        9.73000E-01,
        1.00000E+00,
        2.81610E-03,
        1.44356E-03,
        0.00000E+00
    ])

    # For Trapezoidal Waveform
    t0, t1, t2, t3 = -4.00000E-03, -3.80000E-03, 0., 1.96368E-04
    waveform.times_trapezoids = np.array([t0, t1, t2, t3])

    waveform.time_shift = 220 * 1e-6
    waveform.time_gate_center = np.array([
        12.715,
        16.215,
        20.715,
        26.215,
        33.215,
        42.215,
        53.715,
        68.215,
        86.215,
        108.715,
        136.715,
        172.215,
        217.715,
        274.715,
        346.715,
        437.715,
        551.715,
        695.715,
        877.215,
        1105.715,
        1394.215,
        1758.215,
        2216.715,
        2794.715,
        3523.715,
        4442.715,
        5601.215,
        7061.215,
        8902.215,
        11064.715
    ]) * 1e-6

    return waveform


def skytem_LM_2015():
    """
        SkyTEM Low moment (LM) current waveform
    """

    waveform = CurrentWaveforms('skytem low moment 2015')

    waveform.base_frequency = "210 Hz"
    waveform.currrent_amplitude = "8.3 A"
    waveform.current_times = np.array([
        -3.1810e-003,
        -3.1100e-003,
        -2.7860e-003,
        -2.5334e-003,
        -2.3820e-003,
        -2.3810e-003,
        -2.3798e-003,
        -2.3779e-003,
        -2.3762e-003,
        -2.3749e-003,
        -2.3733e-003,
        -2.3719e-003,
        -2.3716e-003,
        -8.0000e-004,
        -7.2902e-004,
        -4.0497e-004,
        -1.5238e-004,
        -1.0000e-006,
        0,
        1.1535e-006,
        3.0943e-006,
        4.7797e-006,
        6.1076e-006,
        7.7420e-006,
        9.0699e-006,
        9.4274e-006,
    ])

    waveform.currents = np.array([
        0,
        -1.0078e-001,
        -4.5234e-001,
        -7.6328e-001,
        -1.0000e+000,
        -1.0000e+000,
        -8.6353e-001,
        -3.4002e-001,
        -1.1033e-001,
        -4.4709e-002,
        -1.3388e-002,
        -4.4389e-003,
        0,
        0,
        1.0078e-001,
        4.5234e-001,
        7.6328e-001,
        1.0000e+000,
        1.0000e+000,
        8.6353e-001,
        3.4002e-001,
        1.1033e-001,
        4.4709e-002,
        1.3388e-002,
        4.4389e-003,
        0
    ])

    # For Trapezoidal Waveform
    t0, t1, t2, t3 = -8.0000e-04, -1e-6, 0., 9.4274e-006
    waveform.times_trapezoids = np.array([t0, t1, t2, t3])

    waveform.time_shift = 220 * 1e-6
    waveform.time_gate_center = np.array([
        10.215,
        12.715,
        16.215,
        20.715,
        26.215,
        33.215,
        42.215,
        53.715,
        68.215,
        86.215,
        108.715,
        136.715,
        172.215,
        217.715,
        274.715,
        346.715,
        437.715,
        551.715,
        695.715,
        877.215,
        1105.715,
        1394.215
    ]) * 1e-6

    return waveform
