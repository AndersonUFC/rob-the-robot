import pickle, config

class IO_Robot:

	def __init__(self):
		self.save_state_number = 0

	def save_brain(self,robot):
		
		file = open(config.DATA_PATH + "robot_brain" + str(self.save_state_number) + ".brain", 'wb')
		pickle.dump(robot.brain, file)
		file.close()

		state_file = open(config.DATA_PATH +"save_state", "w")
		state_file.write(str(self.save_state_number))
		state_file.close()

		self.save_state_number += 1



	def load_brain(self):
		state_file = open(config.DATA_PATH +"save_state", "r")
		str_number = state_file.readline()

		self.save_state_number = int(str_number)
		state_file.close()
		
		file = None
		try:
			file = open(config.DATA_PATH +"robot_brain" + str(self.save_state_number) + ".brain", 'rb')
		except FileNotFoundError:
			return None	

		brain = pickle.load(file)
		file.close()
		return brain
		