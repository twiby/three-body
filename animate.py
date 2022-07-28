import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class Animator:
	def __init__(self):
		self._animations = []

	def make_animation(x,y,dt, history_len = 50):
		assert(len(x) == len(y))

		fig = plt.figure(figsize=(5, 4))
		ax = fig.add_subplot(
			autoscale_on=False, 
			xlim=(np.min(x), np.max(x)), 
			ylim=(np.min(y), np.max(y)))
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

		    history_x.appendleft(x[i])
		    history_y.appendleft(y[i])

		    marker.set_data([x[i]], [y[i]])
		    trace.set_data(history_x, history_y)
		    time_text.set_text(time_template % (i*dt))
		    return marker, trace, time_text


		return animation.FuncAnimation(
		    fig, animate, len(y), interval=dt*1000, blit=True)


	def animate_movement(self, movement, **kwargs):
		self._animations.append(Animator.make_animation(*movement, **kwargs))

	def show_animations(self):
		plt.show(block = True)
		self._animations = []
	
if __name__=="__main__":
	x = np.arange(0, 100)
	y = np.sin(np.arange(0, 100) / 10) * 50
	A = Animator()
	A.animate_movement((x, y, 0.02))
	A.animate_movement((x, y, 0.02), history_len = 5)
	A.show_animations()
