import Sensor, config, math, mathutils
import numpy as np

class WallSensor(Sensor.Sensor):
	def __init__(self, number_of_features=0):
		Sensor.Sensor.__init__(self, number_of_features)

	def sense(self, robot, labirint, system):
		interval = (2*math.pi)/float(self.number_of_features)
		self.features[0] = 1.
		lab_max_size = float(max([labirint.floor_x, labirint.floor_y]))
		
		for i in range(0, self.number_of_features):
			dir_copy = config.direction_vector.copy()
			dir_copy.rotate(mathutils.Euler((0,0,i*interval),'XYZ'))
			dir_copy = dir_copy.normalized()

			dist,norm = self.distance_sensor(robot.data.location, dir_copy, labirint)
			
			if dist > 0.2:
				self.features[i+1] = 0.
			else:
				a = dist/0.2
				self.features[i+1] = a

		#return self.features.tolist()[1:]

		#\ DEBUG
		return []
	# private methods -----------------------------------