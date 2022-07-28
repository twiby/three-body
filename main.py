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

	##### x = r cost
	##### dxdt = -r w sint
	##### y = r sint
	##### dydt = r w cost

	##### vx^2 + vy^2 = r^2 * w^2

	##### dvxdt = -r w^2 cost
	##### dvydt = -r w^2 sint

	x0 = CENTER[0] + RADIUS * np.cos(th)
	y0 = CENTER[1] + RADIUS * np.sin(th)
	vx0 = - RADIUS * w * np.sin(th)
	vy0 = RADIUS * w * np.cos(th)
	state = np.array([x0, y0, vx0, vy0])
	def derivs(state, t):
		dxdy = np.zeros_like(state)
		dxdy[0] = state[2]
		dxdy[1] = state[3]

		w = np.sqrt(state[2]**2 + state[3]**2) / RADIUS
		dxdy[2] = - RADIUS * w * w * (state[0] - CENTER[0]) / RADIUS
		dxdy[3] = - RADIUS * w * w * (state[1] - CENTER[1]) / RADIUS
		return dxdy

	y = integrate.odeint(derivs, state, t)

	animate_movement(y[:, 0], y[:, 1], dt)

if __name__=="__main__":
	circle_animated()