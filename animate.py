import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class Animator:
	def __init__(self):
		self._animations = []

	def make_animation(movements, history_len = 50):
		dt = movements[0][2]
		max_dt = dt
		for m in movements:
			assert(len(m[0]) == len(m[1]))
			assert(len(m[0]) == len(movements[0][0]))
			if dt > m[2]:
				dt = m[2]
			if max_dt < m[2]:
				max_dt = m[2]
		nb_movements = len(movements)
		length = len(movements[0][0])
		nb_steps = int(length * max_dt / dt)

		min_x = np.min([np.min(m[0]) for m in movements])
		max_x = np.max([np.max(m[0]) for m in movements])
		min_y = np.min([np.min(m[1]) for m in movements])
		max_y = np.max([np.max(m[1]) for m in movements])

		fig = plt.figure(figsize=(5, 4))
		ax = fig.add_subplot(
			autoscale_on=False, 
			xlim=(min_x, max_x), 
			ylim=(min_y, max_y))
		ax.set_aspect('equal')
		ax.grid()

		markers = [[] for _ in range(nb_movements)]
		traces = [[] for _ in range(nb_movements)]
		history_x = [deque(maxlen=history_len) for _ in range(nb_movements)]
		history_y = [deque(maxlen=history_len) for _ in range(nb_movements)]

		for i in range(nb_movements):
			markers[i], = ax.plot([], [], '.', markersize=10)
			traces[i], = ax.plot([], [], '.-', lw=1, ms=2, color=markers[i].get_color())
		time_template = 'time = %.1fs'
		time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

		last_steps = [0 for _ in range(nb_movements)]
		def animate(i):
			for n in range(nb_movements):
				spent = i*dt
				step = int(spent//movements[n][2]) % length
				if step < last_steps[n]:
					history_x[n].clear()
					history_y[n].clear()
				last_steps[n] = step

				if len(history_x[n])==0 or history_x[n][-1] != movements[n][0][step]:
					history_x[n].appendleft(movements[n][0][step])
					history_y[n].appendleft(movements[n][1][step])

				markers[n].set_data([movements[n][0][step]], [movements[n][1][step]])
				traces[n].set_data(history_x[n], history_y[n])
			time_text.set_text(time_template % (i*dt))
			return *markers, *traces, time_text


		return animation.FuncAnimation(
		    fig, animate, nb_steps, interval=dt*1000, blit=True)


	def animate_movement(self, movement, **kwargs):
		if isinstance(movement, tuple):
			self._animations.append(Animator.make_animation([movement], **kwargs))
		elif isinstance(movement,list):
			self._animations.append(Animator.make_animation(movement, **kwargs))
		else:
			raise ValueError

	def show_animations(self):
		plt.show(block = True)
		self._animations = []
	
if __name__=="__main__":
	x = np.arange(0, 100)
	y = np.sin(np.arange(0, 100) / 10) * 50
	A = Animator()

	A.animate_movement((x, y, 0.02))
	A.animate_movement((x, y/2, 0.01), history_len = 5)
	A.show_animations()

	A.animate_movement([(x, y, 0.02), (x, y/2, 0.015)])
	A.show_animations()
