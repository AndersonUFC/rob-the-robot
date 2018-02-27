import bpy, Labirint, math, Fruit

class ManualLabirint(Labirint.Labirint):
	def __init__(self, size_block_space=1, dimension_x=10, dimension_y=10):
		Labirint.Labirint.__init__(self, size_block_space, dimension_x, dimension_y)

		# add backup fruit if add fruit is not called from reset fruit method
		self.backup_state = False
		self.wall_width = 0.05
		

	# rewards: key = <position x, position y>, value = <(reward value, object reference)>
	def add_reward(self, dimension_x, dimension_y, reward):
		bsh = self.size_block_space*0.5

		bpy.ops.mesh.primitive_plane_add()
		self.rewards[(dimension_x, dimension_y)] = (reward, bpy.context.object)

		bpy.ops.transform.resize(value=(bsh,bsh,bsh))
		bpy.ops.transform.translate(value=(bsh - self.floor_x*0.5 + dimension_x*self.size_block_space,\
		                                    bsh - self.floor_y*0.5 + dimension_y*self.size_block_space,\
		                                    0.01))

		material = bpy.data.materials.new("reward material")
		if(reward > 0):
			material.diffuse_color = (0,1.,0)
		else:
			material.diffuse_color = (1.,0,0)
		bpy.context.object.data.materials.append(material)		

	def add_fruit(self, position_x, position_y):
		bpy.ops.mesh.primitive_cube_add()
		bpy.context.object.name = "fruit({},{})".format(position_x, position_y)

		bpy.ops.transform.resize(value=(self.size_block_space*0.05, self.size_block_space*0.05, self.size_block_space*0.05))

		''' discrete
		bpy.ops.transform.translate(value=((self.size_block_space-self.floor_x)*0.5 + position_x*self.size_block_space,\
		                                    (self.size_block_space-self.floor_y)*0.5 + position_y*self.size_block_space,0))
		'''         
		bpy.ops.transform.translate(value=(position_x, position_y, 0.1))                          

		#self.grain_size += 1
		m = bpy.data.materials.new("fruit material")
		m.diffuse_color = (1,0.5,0)
		bpy.context.object.data.materials.append(m)

		fruit = Fruit.Fruit(position_x, position_y, bpy.context.object)
		self.fruits.append(fruit)

		if not self.backup_state:
			self.fruits_backup.append((position_x,position_y))

	def reset_fruits(self):
		self.backup_state = True
		
		for fruit in self.fruits:
			bpy.data.meshes.remove(fruit.data.data)
			bpy.data.objects.remove(fruit.data) 	
		
		del self.fruits[:]
		for x,y in self.fruits_backup:
			self.add_fruit(x,y)

		self.backup_state = False	

	# setters -------------------------------------------------------------

	def set_floor_dimension(self, dimension_x, dimension_y):
		self.floor_x = dimension_x
		self.floor_y = dimension_y

	def set_floor_center(self, center):
		self.floor_center = center
