import numpy as np
import scipy.integrate as integrate

from animate import Animator
from gravitational_system import GravitationalSystem

if __name__=="__main__":
	A = Animator()
	A.animate_movement(GravitationalSystem(5).run(dt = 60*60*24/4, t_stop = 60*60*24*365))
	A.show_animations()