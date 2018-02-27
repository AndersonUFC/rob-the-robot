import bpy, mathutils, Labirint, Fruit
import numpy as np
from random import random, sample

class AutomaticLabirint(Labirint.Labirint):
	def __init__(self, block_size=1, lab_size=10.,wall_width=0.05, wall_heigth=0.2):
		Labirint.Labirint.__init__(self)

		bpy.context.scene.cursor_location = mathutils.Vector((0,0,0))

		self.block_size = block_size
		self.lab_size = lab_size
		self.wall_width = wall_width
		self.wall_heigth = wall_heigth
		self.matrix_size = int(self.lab_size/self.block_size)
		self.lab_matrix = np.zeros((self.matrix_size, self.matrix_size)) - 1
		self.grain_size = 0
		self.grains = []
		self.grains_backup = []
		self.backup_state = False
		self.timestep = lab_size*2        

		self.rewards = {}

		# create labirint --------------------------------------------------------------
		bpy.ops.mesh.primitive_plane_add()
		m = bpy.data.materials.new("z")
		m.diffuse_color = (0.2,0.2,0.5)
		bpy.context.object.data.materials.append(m)
		bpy.ops.transform.resize(value=(self.lab_size*0.5,self.lab_size*0.5,1))
		# ------------------------------------------------------------------------------
		
		self.create_path()
		self.generate_walls()
		
		self.rewards.pop((0,0),None)
		self.rewards[(self.matrix_size-1, self.matrix_size-1)] = 1.
		self.gen_rewards()	

	def DFS_path(self,old_agent):
		agent = old_agent[:]
		actions = {0:'up', 1:'down', 2:'left', 3:'right'}
		move_list = sample([0,1,2,3], 4)
		move_count = 0

		for move in move_list:            
			new_agent, moved = self.mov(agent, actions, move)
			if moved:
				self.DFS_path(new_agent[:])
			else:
				move_count += 1

		if(move_count == 4):
			self.rewards[(agent[0],agent[1])] = -1.
    
	def mov(self, agent, actions, move):
		moved = False
		if(actions[move] == 'up' and agent[1] < self.matrix_size-1 and self.lab_matrix[agent[0]][agent[1]+1] < 0):
			agent[1] = agent[1] + 1
			self.lab_matrix[agent[0]][agent[1]] = 1
			moved = True
		if(actions[move] == 'down' and agent[1] > 0 and self.lab_matrix[agent[0]][agent[1]-1] < 0):
			agent[1] = agent[1] - 1
			self.lab_matrix[agent[0]][agent[1]] = 0
			moved = True
		if(actions[move] == 'left' and agent[0] > 0 and self.lab_matrix[agent[0]-1][agent[1]] < 0):
			agent[0] = agent[0] - 1
			self.lab_matrix[agent[0]][agent[1]] = 3
			moved = True
		if(actions[move] == 'right' and agent[0] < self.matrix_size-1 and self.lab_matrix[agent[0]+1][agent[1]] < 0):
			agent[0] = agent[0] + 1
			self.lab_matrix[agent[0]][agent[1]] = 2
			moved = True
		return agent, moved 

	def create_path(self):
		index = 0
		agent = [0,0]
		actions = {0:'up', 1:'down', 2:'left', 3:'right'}
		limit = 200

		# randompath ------------------------------------------------------------------------
		while(limit == 200):
			limit = 0
			while(index < self.timestep):
				move = int(random()*1000)%4
				agent, moved = self.mov(agent, actions, move)

				if moved:
					index += 1
					self.add_fruit(agent[0], agent[1])

				limit += 1
				if(limit == 200):
					for f in self.fruits:
						bpy.data.objects.remove(f.data)

					self.fruits.clear()
					self.fruits_backup.clear()

					agent = [0,0]
					index = 0
					self.lab_matrix = np.zeros((self.matrix_size, self.matrix_size)) - 1
					break

		# dfs path ---------------------------------------------------------------------------
		self.DFS_path(agent)

    # ---------------------------------------------------------------------------------------------------------------		

	def generate_walls(self): 
		actions = {0:'up', 1:'down', 2:'left', 3:'right'}                                                         
		for y in range(0, self.matrix_size):
			for x in range(0, self.matrix_size):

				if y != 0:
					self.add_wall('horizontal', x,y)
				if x != 0:
					self.add_wall('vertical', x, y)
		
		# border walls
		for i in range(0, self.matrix_size):	
			self.add_wall('horizontal', i, self.matrix_size)
			self.add_wall('horizontal', i, 0)
			self.add_wall('vertical',self.matrix_size,i)  
			self.add_wall('vertical',0,i)  
		
		# remove path walls
		for y in range(0, self.matrix_size):
			for x in range(0, self.matrix_size):
				ob = None
				key = ""
				if(self.lab_matrix[x][y] == 0):
					key = 'horizontal('+str(x)+","+str(y+1)+")"
					ob = self.wall_path_ref.get(key)
				elif(self.lab_matrix[x][y] == 1):
					key = 'horizontal('+str(x)+","+str(y)+")"
					ob = self.wall_path_ref.get(key)
				elif(self.lab_matrix[x][y] == 2):
					key = 'vertical('+str(x)+","+str(y)+")"
					ob = self.wall_path_ref.get(key)
				elif(self.lab_matrix[x][y] == 3):
					key = 'vertical('+str(x+1)+","+str(y)+")"
					ob = self.wall_path_ref.get(key) 
				if ob:
					self.wall_path_ref.pop(key)
					bpy.data.objects.remove(ob)
					

	def gen_rewards(self):
		self.rew_ref = {}

		for position in self.rewards:
			x = position[0]
			y = position[1]
			r = self.rewards[(x,y)]

			# block size half
			bsh = self.block_size*0.5

			bpy.ops.mesh.primitive_plane_add()
			bpy.ops.transform.resize(value=(bsh,bsh,bsh))
			bpy.ops.transform.translate(value=(bsh - self.lab_size*0.5 + x*self.block_size,\
			                                    bsh - self.lab_size*0.5 + y*self.block_size,\
			                                    0.01))


			self.rew_ref[(x,y)] = (r, bpy.context.object)
			m = bpy.data.materials.new("z")
			if(r > 0):
				m.diffuse_color = (0,1.,0)
			else:
				m.diffuse_color = (1.,0,0)
			bpy.context.object.data.materials.append(m)

		self.rewards = self.rew_ref

	def add_fruit(self, position_x, position_y):

		# continous
		# x = position_x
		# y = position_y

		# discrete
		x = (self.size_block_space-self.floor_x)*0.5 + position_x*self.size_block_space
		y = (self.size_block_space-self.floor_y)*0.5 + position_y*self.size_block_space

		bpy.ops.mesh.primitive_cube_add()
		bpy.context.object.name = "fruit({},{})".format(x, y)

		bpy.ops.transform.resize(value=(self.size_block_space*0.05, self.size_block_space*0.05, self.size_block_space*0.05))
		bpy.ops.transform.translate(value=(x,y,0.1))         

		# continous
		#bpy.ops.transform.translate(value=(position_x, position_y, 0.1))                          

		#self.grain_size += 1
		m = bpy.data.materials.new("fruit material")
		m.diffuse_color = (1,0.5,0)
		bpy.context.object.data.materials.append(m)

		# continous
		#fruit = Fruit.Fruit(position_x, position_y, bpy.context.object)

		# discrete
		fruit = Fruit.Fruit(x,y,bpy.context.object)

		self.fruits.append(fruit)

		if not self.backup_state:
			self.fruits_backup.append((position_x,position_y))		

	def reset_fruits(self):
		self.backup_state = True
		
		for fruit in self.fruits:
			bpy.data.objects.remove(fruit.data) 	
		
		del self.fruits[:]
		for x,y in self.fruits_backup:
			self.add_fruit(x,y)

		self.backup_state = False			