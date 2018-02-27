import numpy as np
import mathutils, bpy

class Sensor:
	def __init__(self, number_of_features=0):
		self.number_of_features = number_of_features
		self.features = np.random.random(number_of_features+1)

	def sense(self, robot, labirint, system):
		pass

	def point_inside_triangle2(self,A,B,C,P):
		u = B-A
		v = C-A
		w = P-A

		vCrossW = v.cross(w)
		vCrossU = v.cross(u)

		if(vCrossW.dot(vCrossU) < 0):
			return False

		uCrossW = u.cross(w)
		uCrossV = u.cross(v)

		if(uCrossW.dot(uCrossV) < 0):
			return False

		denom = uCrossV.length
		r = vCrossW.length/denom
		t = uCrossW.length/denom

		test = r + t <= 1
		return test


	def point_inside_triangle(self,A,B,C,P,P0):
		V1 = A - P0
		V2 = B - P0
		N = V2.cross(V1)
		N.normalize()
		d = -P0.dot(N)
		if(P.dot(N) + d < 0):
			return False

		V1 = B - P0
		V2 = C - P0
		N = V2.cross(V1)
		N.normalize()
		d = -P0.dot(N)
		if(P.dot(N) + d < 0):
			return False

		V1 = C - P0
		V2 = A - P0
		N = V2.cross(V1)
		N.normalize()
		d = -P0.dot(N)
		if(P.dot(N) + d < 0):
			return False
		return True

	# ----------------------------------------------------------------

	def distance_sensor(self, source, direction_vector, labirint):
		P_0 = source
		V = direction_vector.normalized()
		min_t = 900
		face_normal = None

		#for obj in labirint.wall_path_ref.values():
		for obj in bpy.data.objects:
			if "horizontal" in obj.name or "vertical" in obj.name:
				mesh = obj.data
				faces = mesh.polygons
				vertices = mesh.vertices
				mw = obj.matrix_world

				for face in faces:
					vertice_face_index = face.vertices[0]
					N = (face.normal).normalized()
					P = mw * vertices[vertice_face_index].co

					if(V.dot(N) != 0):
						t = (P - P_0).dot(N)/(V.dot(N))				
						if(t > 0 and t < min_t):

							Pplane = P_0 + V*t
							A = P
							B = mw * vertices[face.vertices[1]].co
							C = mw * vertices[face.vertices[2]].co
							D = mw * vertices[face.vertices[3]].co

							tri1 = self.point_inside_triangle(A,B,C,Pplane,P_0)
							tri2 = self.point_inside_triangle(A,C,D,Pplane,P_0)

							if(tri1 or tri2):
								face_normal = N
								min_t = t

		if min_t == 900:
			return 0, mathutils.Vector((0,0,0))

		Pplane = P_0 + V*min_t
		return (Pplane - P_0).length, face_normal