import bpy, mathutils

class Fruit:
	def __init__(self, position_x, position_y, data):
		self.position_x = position_x
		self.position_y = position_y
		self.vector_mole = mathutils.Vector((0,0,0))
		self.max_tension = 0.2
		self.data = data

	def getPosition(self):
		return self.position_x, self.position_y

	def update_vector_mole(self):
		self.vector_mole = mathutils.Vector((self.position_x, self.position_y)) - mathutils.Vector((self.center_position_x, self.center_position_y))
	