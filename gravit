#!/usr/bin/env python
import argparse

from animate import Animator
from gravitational_system import GravitationalSystem

def main(args):
	n = args.bodies
	dt = args.timestep
	t_stop = args.duration

	A = Animator()
	A.animate_movement(GravitationalSystem(n).run(dt, t_stop))
	A.show_animations()

if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Simulate and animate a gravitational system")
	parser.add_argument('-b','--bodies', type=int, help="number of bodies in the simulation", default=3)
	parser.add_argument('-t','--timestep', type=float, help="time step of the simulation, in seconds", default=60*60*24/4)
	parser.add_argument('-d','--duration', type=float, help="duration of the simulation, in seconds", default=60*60*24*365)
	args = parser.parse_args()
	main(args)