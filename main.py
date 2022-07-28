import numpy as np
import scipy.integrate as integrate

from animate import animate_movement

def circle_animated():

	RADIUS = 2
	CENTER = np.array([1, 1])

	# create a time array from 0..t_stop sampled at 0.02 second steps
	dt = 0.02
	t_stop = 10  # how many seconds to simulate
	t = np.arange(0, t_stop, dt)

	th = 0
	w = 2
	state = np.array([th, w])

	def derivs(state, t):
		dxdy = np.zeros_like(state)
		dxdy[0] = state[1]
		dxdy[1] = 0.5
		return dxdy

	y = integrate.odeint(derivs, state, t)
	x1 = CENTER[0] + RADIUS*np.cos(y[:, 0])
	y1 = CENTER[1] + RADIUS*np.sin(y[:, 0])





	animate_movement(x1, y1, dt)

if __name__=="__main__":
	circle_animated()