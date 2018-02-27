import ManualLabirint, bpy

def e1():
	lab = ManualLabirint.ManualLabirint()
	lab.create_floor()

	for i in range(0,10):
		lab.add_wall('vertical',0,i)
		lab.add_wall('vertical',10,i)
		lab.add_wall('horizontal',i,0)
		lab.add_wall('horizontal',i,10)

	
	lab.add_wall('horizontal', 0, 0)
	lab.add_wall('vertical', 0, 0)
	lab.add_wall('vertical', 1, 0)
	lab.add_wall('vertical', 0, 1)
	lab.add_wall('vertical', 1, 1)
	lab.add_wall('vertical', 0, 2)
	lab.add_wall('vertical', 1, 2)
	lab.add_wall('vertical', 0, 3)
	lab.add_wall('vertical', 1, 3)
	lab.add_wall('vertical', 0, 4)
	lab.add_wall('horizontal', 0, 5)
	lab.add_wall('horizontal', 1, 4)
	lab.add_wall('horizontal', 1, 5)
	lab.add_wall('horizontal', 2, 4)
	lab.add_wall('horizontal', 2, 5)
	lab.add_wall('horizontal', 3, 4)
	lab.add_wall('vertical', 4, 4)		
	lab.add_wall('vertical', 4, 5)
	lab.add_wall('vertical', 4, 6)
	lab.add_wall('vertical', 4, 7)
	lab.add_wall('vertical', 4, 8)
	lab.add_wall('vertical', 4, 9)
	lab.add_wall('vertical', 3, 5)
	lab.add_wall('vertical', 3, 6)
	lab.add_wall('vertical', 3, 7)
	lab.add_wall('vertical', 3, 8)
	lab.add_wall('vertical', 3, 9)
	lab.add_wall('horizontal', 3, 10)

	for i in range(0, 18):
		lab.add_fruit(-4.5, -4 + 0.2*i)

	
	for i in range(1, 16):
		lab.add_fruit(-4.5 + 0.2*i, -0.5)

	for i in range(1, 26):
		lab.add_fruit(-1.5, -0.5 + 0.2*i)

	lab.add_reward(3, 9, 1)
	

	return lab