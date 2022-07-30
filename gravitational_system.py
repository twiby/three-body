import numpy as np
import scipy.integrate as integrate

class GravitationalSystem:
	def __init__(self, N = 2):
		assert(N >= 2)

		self.N = N
		self.M1 = 2e30 ### mass of the sun
		self.M2 = self.M1 / 2 
		self.M = [self.M2, self.M1, self.M1]
		self.G = 6.67e-11 ### gravitational constant
		self.D = 152e9/2 ### distance earth-sun
		self.V = 30000 / 2

		P = np.zeros(2)
		self.state = np.zeros(4*self.N)
		for n in range(self.N):
			th = n*2*np.pi/self.N

			self.state[self.x(n)] = self.D * np.cos(th)
			self.state[self.y(n)] = self.D * np.sin(th)

			if n == 0:
				V = np.array([0, self.V])
			elif n == N-1:
				V = -P / self.M[n]
			else:
				V = -P / self.M[n]/2

			P += V * self.M[n]
			self.state[self.vx(n)], self.state[self.vy(n)] = V


	def x(self, n):
		return 4*n
	def y(self, n):
		return 4*n+1
	def vx(self, n):
		return 4*n+2
	def vy(self, n):
		return 4*n+3


	def derivs(state, t, *args):
		self = args[0]

		positions = [np.array([state[self.x(n)], state[self.y(n)]]) for n in range(self.N)]
		speeds = [np.array([state[self.vx(n)], state[self.vy(n)]]) for n in range(self.N)]

		dxdy = np.zeros_like(state)

		for n in range(self.N):
			dxdy[self.x(n)], dxdy[self.y(n)] = speeds[n]

			F = np.zeros(2)
			for n2 in range(self.N):
				if n2 == n:
					continue
				relative_position = positions[n] - positions[n2]
				R = np.linalg.norm(relative_position)
				F += -relative_position / R * self.G / R / R * self.M[n2]

			dxdy[self.vx(n)], dxdy[self.vy(n)] = F

		return dxdy

	def run(self, dt = 60*60*24, t_stop = 60*60*24*365):

		# create a time array from 0..t_stop sampled at 0.02 second steps
		t = np.arange(0, t_stop, dt)
		y = integrate.odeint(GravitationalSystem.derivs, self.state, t, (self,))
		return [(y[:,self.x(n)], y[:, self.y(n)], 1/365) for n in range(self.N)]

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