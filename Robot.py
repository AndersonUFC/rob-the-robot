# imports --------------------------------------------------------
import config, math, bpy, Walk, Rotate, Mouth, WallSensor, FruitSensor, Brain

class Robot:
	def __init__(self, size=1):
		bpy.ops.object.select_all(action='DESELECT')

		# BB8
		#bpy.ops.import_scene.obj(filepath=config.DATA_PATH + 'BB8/bb8.obj')

		bpy.ops.import_scene.obj(filepath=config.DATA_PATH + 'rob/rob.obj')
		bpy.context.scene.objects.active = bpy.context.selected_objects[0]
		bpy.ops.object.join()

		bpy.ops.transform.resize(value=(size,size,size))
		
		# BB8
		#bpy.ops.transform.rotate(value=-math.pi/2, axis=(0,0,1))

		bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')

		self.data = bpy.context.object
		self.data.name = 'robot'

		# sensors ----------------------------------
		self.sensor_wall = WallSensor.WallSensor(number_of_features=4)
		self.sensor_fruit = FruitSensor.FruitSensor(number_of_features=2, radius=1.5)

		# actuators --------------------------------
		self.act_walk = Walk.Walk(velocity=0.05)
		self.act_rotate = Rotate.Rotate(degree_rotation=math.pi/10)
		
		self.act_mouth = Mouth.Mouth(robot_size=0.03)

		# brain ------------------------------------
		self.brain = Brain.Brain(number_of_actions=4)

	def set_location(self,x,y,z):
		bpy.ops.object.select_all(action='DESELECT')
		self.data.select = True	
		bpy.ops.transform.translate(value=(x,y,z))

	def map_actions(self, index, labirint, system):
		collision = None
		if index == 0:
			collision = self.act_walk.act('foward', self, labirint, system)
		if index == 1:
			collision = self.act_walk.act('backward', self, labirint, system)			
		if index == 2:
			collision = self.act_rotate.act('clockwise', self, labirint, system)			
		if index == 3:
			collision = self.act_rotate.act('counterclockwise', self, labirint, system)
		if index == 4:
			self.act_mouth.act(None, self, labirint, system)
		return collision