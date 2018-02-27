import bpy, math

class Display:
	def __init__(self):
		bpy.ops.object.text_add(radius=0.5, location=(6,6,0), rotation=(0,0,-math.pi/2))
		self.text = bpy.context.object

	def set_text(self,text_):
		print(bpy.context)
		bpy.ops.object.select_all(action='DESELECT')
		self.text.select = True
		bpy.ops.font.delete(type='ALL')
		bpy.ops.font.text_insert(text=text_)