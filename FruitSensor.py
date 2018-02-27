import Sensor, config, mathutils, math, bpy
import numpy as np

# leva
class FruitSensor(Sensor.Sensor):
	def __init__(self, number_of_features=0, radius=1):
		Sensor.Sensor.__init__(self, number_of_features)
		self.radius = radius

	def sense(self, robot, labirint, system):
		F = [1., 0., 0., 0.]

		g75 = math.pi*(75./180.)
		g20 = math.pi*(20./180.)
		g55 = math.pi*(55./180.)

		gc = math.pi*(10./180.)
		gc_sum = math.pi*(20./180.)

		closest_fruit_index = -1

		robot_bound_box = system.get_BoundBox(robot.data.name)
		front_loc = robot.act_walk.get_front_location(robot.data.dimensions, robot.data.location)

		right_edge = config.direction_vector.copy()
		right_edge.rotate(mathutils.Euler((0,0,-g75),'XYZ'))
		right_edge.normalize()

		right = config.direction_vector.copy()
		right.rotate(mathutils.Euler((0,0,-g20),'XYZ'))
		right.normalize()

		left_edge = config.direction_vector.copy()
		left_edge.rotate(mathutils.Euler((0,0,g75),'XYZ'))
		left_edge.normalize()

		left = config.direction_vector.copy()
		left.rotate(mathutils.Euler((0,0,g20),'XYZ'))
		left.normalize()

		central_l = config.direction_vector.copy()
		central_l.rotate(mathutils.Euler((0,0,gc),'XYZ'))
		central_l.normalize()

		central_r = config.direction_vector.copy()
		central_r.rotate(mathutils.Euler((0,0,-gc),'XYZ'))
		central_r.normalize()		

		# center
		menor = 999
		cf = None
		for fruit in labirint.fruits:
			a = self.insideSector(front_loc, fruit.data.location, central_l, central_r, gc_sum , self.radius, el_print=True)
			if a < menor and a > 0:
				menor = a
				cf = fruit

		if menor == 999:
			F[1] = 0.
		else:
			F[1] = 1 - float(menor)/float(self.radius)
			'''
			vec = cf.data.location - front_loc
			dist, norm = self.distance_sensor(front_loc, vec,labirint)
			if dist > np.linalg.norm(vec) or math.fabs(dist) <= 0.00001:
				F[1] = 1 - float(menor)/float(self.radius)
			else:
				F[1] = 0.
			'''

		closest_fruit = F[1]
		closest_fruit_index = 1


		# left
		menor = 999
		for fruit in labirint.fruits:
			a = self.insideSector(front_loc, fruit.data.location, left_edge, left, g55 , self.radius)
			if a < menor and a > 0:
				menor = a
				cf = fruit
		if menor == 999:
			F[2] = 0.
		else:
			F[2] = 1 - float(menor)/float(self.radius)
			'''
			vec = cf.data.location - front_loc
			dist, norm = self.distance_sensor(front_loc, vec,labirint)

			if dist > np.linalg.norm(vec) or math.fabs(dist) <= 0.00001:
				F[2] = 1 - float(menor)/float(self.radius)
			else:
				F[2] = 0.
			'''

		if F[2] > closest_fruit:
			closest_fruit = F[2]
			closest_fruit_index = 2

		# right
		menor = 999
		for fruit in labirint.fruits:
			a = self.insideSector(front_loc, fruit.data.location, right_edge, right, g55, self.radius)
			if a < menor and a > 0:
				menor = a
				cf = fruit
		if menor == 999:
			F[3] = 0.
		else:
			F[3] = 1 - float(menor)/float(self.radius)
			'''
			vec = cf.data.location - front_loc
			dist, norm = self.distance_sensor(front_loc, vec,labirint)

			if dist > np.linalg.norm(vec) or math.fabs(dist) <= 0.00001:						
				F[3] = 1 - float(menor)/float(self.radius)
			else:
				F[3] = 0.				
			'''

		if F[3] > closest_fruit:
			closest_fruit = F[3]
			closest_fruit_index = 3

		for i in range(1, 4):
			if i != closest_fruit_index:
				F[i] = 0.

		return F[1:]

	# auxiliar private methods --------------------------------------------------------------------

	def insideSector(self, base, point, limit1, limit2, angle, radius, el_print=False):

		vector = (point - base)
		comp = vector.x**2 + vector.y**2
		vector = vector.normalized()
		limit1.z = 0
		limit2.z = 0
		vector.z = 0
		angle1 = math.acos(vector * limit1)
		angle2 = math.acos(vector * limit2)

		inside = angle1 <= angle and angle2 <= angle and (comp <= radius**2)

		if el_print:
			pass

		if inside:
			return comp**0.5
		return 0.