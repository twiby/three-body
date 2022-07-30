import numpy as np
import scipy.integrate as integrate

from animate import Animator
from gravitational_system import GravitationalSystem

def circle_animated(
	RADIUS = 2,
	CENTER = np.array([1, 1])):

	# create a time array from 0..t_stop sampled at 0.02 second steps
	dt = 0.02
	t_stop = 10  # how many seconds to simulate
	t = np.arange(0, t_stop, dt)

	th = 0
	w = 2
	W = 0.5

	##### x = r cost
	##### dxdt = -r w sint
	##### y = r sint
	##### dydt = r w cost

	##### vx^2 + vy^2 = r^2 * w^2

	##### dvxdt = -r w^2 cost - r W sint
	##### dvydt = -r w^2 sint + r W cost

	x0 = CENTER[0] + RADIUS * np.cos(th)
	y0 = CENTER[1] + RADIUS * np.sin(th)
	vx0 = - RADIUS * w * np.sin(th)
	vy0 = RADIUS * w * np.cos(th)
	state = np.array([x0, y0, vx0, vy0])
	def derivs(state, t):
		dxdy = np.zeros_like(state)
		dxdy[0] = state[2]
		dxdy[1] = state[3]

		cost = (state[0] - CENTER[0]) / RADIUS
		sint = (state[1] - CENTER[1]) / RADIUS
		w = np.sqrt(state[2]**2 + state[3]**2) / RADIUS
		dxdy[2] = - RADIUS * w * w * cost - RADIUS * W * sint 
		dxdy[3] = - RADIUS * w * w * sint + RADIUS * W * cost
		return dxdy

	y = integrate.odeint(derivs, state, t)
	return y[:, 0], y[:, 1], dt

def pendulum(
	RADIUS = 2,
	CENTER = np.array([1, 1])):

	G = 9.8  # acceleration due to gravity, in m/s^2
	M = 0.5 # mass, in kg
	F_1 = 0.4 # linear friction coeficient, in N.s/m

	# create a time array from 0..t_stop sampled at 0.02 second steps
	dt = 0.01
	t_stop = 10  # how many seconds to simulate
	t = np.arange(0, t_stop, dt)

	th = 0

	##### x = r cost
	##### dxdt = -r w sint
	##### y = r sint
	##### dydt = r w cost

	##### vx^2 + vy^2 = r^2 * w^2

	##### dvxdt = -r w^2 cost - r W sint
	##### dvydt = -r w^2 sint + r W cost

	##### This feels like it's wrong
	##### m*W = -m*G*cost -F*v

	th =  0
	x0 = CENTER[0] + RADIUS * np.cos(th)
	y0 = CENTER[1] + RADIUS * np.sin(th)
	vx0 = 0
	vy0 = 5
	state = np.array([x0, y0, vx0, vy0])

	Etot = M*G*(y0-(CENTER[1]-RADIUS))
	def derivs(state, t):
		dxdy = np.zeros_like(state)
		dxdy[0] = state[2]
		dxdy[1] = state[3]

		cost = (state[0] - CENTER[0]) / RADIUS
		sint = (state[1] - CENTER[1]) / RADIUS
		v = np.sqrt(state[2]**2 + state[3]**2)
		w = np.sign(state[2]) * v / RADIUS
		W = -G * cost - F_1*np.sign(state[2])*v/M
		dxdy[2] = - RADIUS * w * w * cost - RADIUS * W * sint 
		dxdy[3] = - RADIUS * w * w * sint + RADIUS * W * cost
		return dxdy

	y = integrate.odeint(derivs, state, t)
	return y[:, 0], y[:, 1], dt

if __name__=="__main__":
	A = Animator()
	A.animate_movement(GravitationalSystem(3).run(dt = 60*60*24/4, t_stop = 60*60*24*365))
	A.show_animations()