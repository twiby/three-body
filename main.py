import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.integrate as integrate
from collections import deque

def circle_animated():

	RADIUS = 2
	CENTER = np.array([1, 1])

	# create a time array from 0..t_stop sampled at 0.02 second steps
	dt = 0.02
	history_len = 50  # how many trajectory points to display
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

	fig = plt.figure(figsize=(5, 4))
	ax = fig.add_subplot(
		autoscale_on=False, 
		xlim=(CENTER[0] - 1.5*RADIUS, CENTER[0] + 1.5*RADIUS), 
		ylim=(CENTER[1] - 1.5*RADIUS, CENTER[0] + 1.5*RADIUS))
	ax.set_aspect('equal')
	ax.grid()

	marker, = ax.plot([], [], '.', markersize=10)
	trace, = ax.plot([], [], '.-', lw=1, ms=2)
	time_template = 'time = %.1fs'
	time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
	history_x, history_y = deque(maxlen=history_len), deque(maxlen=history_len)

	def animate(i):
	    if i == 0:
	        history_x.clear()
	        history_y.clear()

	    history_x.appendleft(x1[i])
	    history_y.appendleft(y1[i])

	    marker.set_data([x1[i]], [y1[i]])
	    trace.set_data(history_x, history_y)
	    time_text.set_text(time_template % (i*dt))
	    return marker, trace, time_text


	ani = animation.FuncAnimation(
	    fig, animate, len(y), interval=dt*1000, blit=True)
	plt.show()

if __name__=="__main__":
	circle_animated()