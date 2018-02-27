import mathutils, bpy, config

last_action_state = ""

class Actuator:
	def __init__(self):
		pass

	def act(self, TYPE, robot, labirint, system):
		pass

	def get_front_location(self, dimension, robot_location):
		vb = config.direction_vector.normalized()

		vd = mathutils.Vector((vb[0]*dimension[1], vb[1]*dimension[1], vb[2]*dimension[1]))

		'''
		yv = (mathutils.Vector(((bound_box[1]-bound_box[0]).length,\
				                    (bound_box[1]-bound_box[5]).length,\
				                    (bound_box[1]-bound_box[2]).length)))

		nyv = mathutils.Vector((vb[0]*yv[0], vb[1]*yv[1], 0))
		return robot_location + nyv
		'''
		return robot_location + vd