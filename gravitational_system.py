import numpy as np
import scipy.integrate as integrate

def two_body_system():
	M1 = 2e30 ### mass of the sun
	M2 = 6e24 ### mass of the earth
	G = 6.67e-11 ### gravitational constant
	D = 152e9 ### distance earth-sun
	V = 30000 / 2

	state = np.array([D, 0, 0, V, 0, 0, 0, -V/2])

	# create a time array from 0..t_stop sampled at 0.02 second steps
	dt = 60*60*24
	t_stop = 60*60*24*365  # how many seconds to simulate
	t = np.arange(0, t_stop, dt)

	def derivs(state, t):
		dxdy = np.zeros_like(state)
		dxdy[0] = state[2]
		dxdy[1] = state[3]
		dxdy[4] = state[6]
		dxdy[5] = state[7]

		x = state[0] - state[4]
		y = state[1] - state[5]
		R = np.sqrt(x**2 + y**2)
		F = G / R / R
		Fx = -F * x / R
		Fy = -F * y / R

		dxdy[2] = Fx * M1
		dxdy[3] = Fy * M1
		dxdy[6] = -Fx * M1 / 2
		dxdy[7] = -Fy * M1 / 2
		return dxdy

	y = integrate.odeint(derivs, state, t)
	return y[:, 0], y[:, 1], y[:, 4], y[:, 5]