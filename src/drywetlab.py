import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt


# A map from neuron type abbreviation to ordered list of parameters
# a, b, c, d, C, k, Vr, Vt from Dynamical Systems in Neuroscience.
# NB: many of these models have some extra bonus features in the book,
# used to more accurately reproduce traces from electrophysiological
# experiments in the appropriate model organisms. In particular,
#  - LTS caps the value of u but (along with a few other types) allows
#     it to influence the effective value of spike threshold and c.
#  - I can't implement FS yet because its u nullcline is nonlinear.
#  - Several other types have PWL u nullclines.
#  - Different cell types have different spike thresholds.
NEURON_TYPES = {
    'rs':  [0.03, -2, -50, 100, 100, 0.7, -60, -40],
    'ib':  [0.01,  5, -56, 130, 150, 1.2, -75, -45],
    'ch':  [0.03,  1, -40, 150,  50, 1.5, -60, -40],
    'lts': [0.03,  8, -53,  20, 100, 1.0, -56, -42],
    'ls':  [0.17,  5, -45, 100,  20, 0.3, -66, -40]}


class PhysicalOrganoid():
    """
    A simulated 2D culture of cortical cells using models from Dynamical
    Systems in Neuroscience, with synapses implemented as straightforward
    exponential PSPs for both excitatory and inhibitory cells.

    The model represents the excitability of a neuron using two phase
    variables: the membrane voltage v : mV, and the "recovery" or
    "leakage" current u : pA.

    There is a single bifurcation parameter which is assumed to vary
    with time: the additional membrane current Iin.

    Additionally, the excitation model contains the following static
    parameters, all of which can be set globally by providing scalars,
    or on a per cell basis by providing arrays of size (N,):
     a : 1/ms time constant of recovery current
     b : nS steady-state conductance for recovery current
     c : mV membrane voltage after a downstroke
     d : pA bump to recovery current after a downstroke
     C : pF membrane capacitance
     k : nS/mV voltage-gated Na+ channel conductance
     Vr: mV resting membrane voltage
     Vt: mV threshold voltage when u=0

    The cells are assumed to be located at physical positions contained
    in the variable XY : um, but this is not used for anything other than
    display (simulated Ca2+ imaging etc).

    Finally, the synaptic model involves one extra phase variable Isyn
    as well as several additional parameters, most obviously the synaptic
    connectivity matrix S. Several of these are used for modeling STDP
    as described by Song (2000); these parameters are listed after those
    necessary for basic operation.
     Sij : pA peak postsynaptic current response at i to an AP in j
     tau : ms time constant of the exponential synapse
     tau_STDP : ms time constant for STDP
     EPSC_max : pA maximum allowable value of EPSC
     IPSC_max : pA biggest allowable absolute value of IPSC
     alpha_plus : pA maximum increase in EPSC per STDP event
     alpha_minus : pA maximum increase in IPSC per STDP event
    """
    def __init__(self, *args, XY, S,
                 a=0.02, b=0.2, c=-65, d=2, C=15, k=0.6, Vr=-70, Vt=-50,
                 tau=3, tau_STDP=20, EPSC_max=7, IPSC_max=10,
                 alpha_plus=0.02, alpha_minus=0.021):
        self.N = S.shape[0]
        assert S.shape==(self.N,self.N), 'S must be square!'
        assert XY.shape==(2,self.N), 'XY and S have inconsistent size!'
        assert tau >= 1, 'Forward Euler is unstable for small tau'

        self.S = S
        self.XY = XY
        self.a, self.b = a, b
        self.c = c * np.ones(self.N)
        self.d = d * np.ones(self.N)
        self.C, self.k, self.Vr, self.Vt = C, k, Vr, Vt
        self.tau = tau
        self.EPSC_max = EPSC_max
        self.IPSC_max = IPSC_max
        self.tau_STDP = tau_STDP
        self.alpha_plus = alpha_plus
        self.alpha_minus = alpha_minus
        self.VUI = np.zeros((3, self.N))
        self.reset()

    def reset(self):
        self.VUI[0,:] = self.Vr
        self.VUI[1:,:] = 0

    def VUIdot(self, Iin):
        Vdot = (self.k*(self.V - self.Vr)*(self.V - self.Vt) -
                self.U + self.Isyn + Iin) / self.C
        Udot = self.a * (self.b*(self.V - self.Vr) - self.U)
        Idot = -self.tau * self.Isyn
        return np.array([Vdot, Udot, Idot])

    def step(self, Iin=0):
        fired = self.V >= 30#mV
        self.V[fired] = self.c[fired]
        self.U[fired] += self.d[fired]
        self.Isyn += self.S @ fired

        self.VUI += self.VUIdot(Iin) * 0.5#ms
        self.VUI += self.VUIdot(Iin) * 0.5#ms
        return self.VUI, fired

    @property
    def V(self):
        return self.VUI[0,:]

    @V.setter
    def V(self, value):
        self.VUI[0,:] = value

    @property
    def U(self):
        return self.VUI[1,:]

    @U.setter
    def U(self, value):
        self.VUI[1,:] = value

    @property
    def Isyn(self):
        return self.VUI[2,:]

    @Isyn.setter
    def Isyn(self, value):
        self.VUI[2,:] = value

    # THE FOLLOWING METHODS ARE PART OF THE OLD VERSION OF ORGANOID,
    # AND STILL NEED TO BE UPDATED!
    def _STDP(self, fired):
        """
        Modify synaptic strength according to the spike-time-dependent
        plasticity model described in Song (2000).

        Whenever a cell fires, each incoming synapse is strengthened
        according to how recently it has fired, while each outgoing
        synapse is weakened if the postsynaptic cell has fired too
        recently.
        """
        if not np.any(fired): return

        expy = self.g_max * np.exp(-self.last_fired / self.tau_syn)
        self.S[fired, :] += self.alpha_plus * expy.reshape((1,-1))
        self.S[:, fired] -= self.alpha_minus * expy.reshape((-1,1))
        np.clip(self.S[fired,:], -self.g_max, self.g_max,
                out=self.S[fired,:])
        np.clip(self.S[:,fired], -self.g_max, self.g_max,
                out=self.S[:,fired])
        # This doesn't prevent itself from changing signs!

    def _plot(self, **kwargs):
        """
        Plot the cells in position, with arrow thickness proportional
        to the strength of the cell.
        """
        XY = self.positions
        plt.plot(XY[0,:], XY[1,:], 'o')
        plt.gca().set_aspect('equal')
        SS = np.abs(self.S)
        SS /= SS.max()

        for i in range(self.N):
            for j in range(self.N):
                if i == j or SS[i,j] < 1e-2:
                    continue
                clr = 'r' if self.S[i,j]<0 else 'b'
                x, y = XY[:,i]
                r = XY[:,j] - XY[:,i]
                dx, dy = r
                rhat = r / np.sqrt((r**2).sum())
                ofsx, ofsy = 0.03 * rhat
                perpx, perpy = 0.005 * np.array([-rhat[1], rhat[0]])
                plt.arrow(x + ofsx + perpx, y + ofsy + perpy,
                          r[0] - 2*ofsx, r[1] - 2*ofsy, color=clr,
                          shape='right', width=0.01*SS[i,j],
                          length_includes_head=True, head_width=0.02,
                          linewidth=0, **kwargs)


class Ca2tCamera():
    """
    Generate a Pyplot illustration of an Organoid, approximately simulating
    Ca2+ imaging.

    The simulated camera averages the number n of firing events per ms
    over some period, smooths it using a moving-average filter, and
    activation of each cell grows logarithmically in firing rate.
    This gives activation that corresponds to firing frequency, without
    being able to directly measure the membrane voltage, and it fluctuates
    only slowly.
    """
    def __init__(self, n, *args,
                 tick=None, frameskip=0, window_size=1, reactivity=30,
                 Iin=lambda *args: 0, scatterargs={},
                 **kwargs):
        """
        Create a Ca2+ imaging figure! Pass in a figure and an Organoid
        object.  Also takes input current as a function of time
        Iin(t), and a function tick(n,t,*) to run on the Organoid
        at each frame. Then some parameters control the frames.

        You can set the amount of simulation time and real time per frame
        by combining this frameskip argument with the animator's frame
        interval argument: the real-time interval between simulation
        frames is interval/(frameskip + 1) ms, or in reverse, the video
        is (frameskip + 1)/interval times faster than real-time.

        The moving average filter is controlled by the parameter
        window_size: this is the number of the last internal frames
        which are averaged to produce each frame you actually see.

        Reactivity determines what is considered a "long time"
        between spikes: a cell lights up 60% if its average firing interval
        is equal to the reactivity.
        """
        self.window_size = window_size
        self.ticks_per_update = frameskip + 1
        self.n = n
        self.Iin = Iin
        self.reactivity = reactivity
        self._tick = tick

        self.X = np.zeros((window_size, n.N))
        self.scatterargs = scatterargs

    def tick(self, t, *args):
        if self._tick is not None:
            self._tick(t, *args)

    def init(self, fig):
        "Creates the scatter plot, must call before starting to record."
        self.fig = fig or plt.figure()
        self.ax = self.fig.gca()
        self.ax.patch.set_facecolor((0,0,0))
        self.scat = self.ax.scatter(self.n.XY[0,:], self.n.XY[1,:],
                                    s=5, c=self.X.mean(axis=0), cmap='gray',
                                    norm=colors.Normalize(vmax=1, vmin=0,
                                                          clip=True),
                                    **self.scatterargs)

    def update(self, T, *args, show=True):
        """
        Calculate one frame forward, for the Tth sampling period.
        Additional arguments can be passed to the tick() method
        """
        Tmod = T % self.window_size
        self.X[Tmod, :] = 0
        for dt in range(self.ticks_per_update):
            t = T*self.ticks_per_update + dt
            _, fired = self.n.step(self.Iin(t))
            self.X[Tmod, fired] += 1 / self.ticks_per_update
            self.tick(t, *args)

        if show:
            xavg = self.X.mean(axis=0)
            self.scat.set_array(1 - np.exp(-xavg * self.reactivity))
            return self.scat


class UtahArray():
    """
    An electrical microelectrode array: a rectangular grid where
    each point stimulates nearby cells in a Neurons object.

    You pass a specification of the grid geometry, then an amount
    of activation per pin (output should have the same shape as the
    grid), and the array becomes a callable that can be
    """
    def __init__(self, *args,
                 spacing=None, shape=None, dimensions=None,
                 points=None, offset=(0,0), radius=10,
                 activation):
        if points is None:
            if dimensions is None:
                px, py = np.mgrid[:shape[0], :shape[1]] * spacing
            elif shape is None:
                try: spacing[0]
                except TypeError as _:
                    spacing = [spacing, spacing]
                px, py = np.mgrid[:dimensions[0]:spacing[0],
                                  :dimensions[1]:spacing[1]]
            elif spacing is None:
                px, py = np.mgrid[:dimensions[0]:shape[0]*1j,
                                  :dimensions[1]:shape[1]*1j]
            px = px.flatten() # - px.mean()
            py = py.flatten() # - py.mean()
            points = np.array((px, py))

        self.points = points + np.asarray(offset).reshape((2,1))
        self.activation = activation
        self.radius = radius

    def insert(self, n):
        """
        Insert this array into an organoid. Precomputes the connectivity
        matrix from the array's inputs to the cells.
        """
        # The distance from the ith cell to the jth probe.
        dij = n.XY.reshape((2,-1,1)) - self.points.reshape((2,1,-1))
        dij = (dij**2).sum(axis=0) / self.radius
        dij[dij < 1] = 1
        self.M = 1 / dij
        self.n = n

    def Vprobe(self):
        return (self.M.T @ self.n.V) / self.M.sum(axis=0)

    def Iout(self, t):
        return self.M @ self.activation(t)
