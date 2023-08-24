"""
x_i_ denote the input to the (i+1)-th round.
"""
from os import read

from gurobipy import *

import time


class SHADOW:
	def __init__(self, Round):
		self.Round = Round
		self.blocksize = 64
		self.filename_model = "SHADOW_" + str(self.Round) + "Round" + ".lp"
		self.filename_result = "result_SHADOW_" + str(self.Round) + "Round" + ".txt"
		fileobj = open(self.filename_model, "w")
		fileobj.close()
		fileboj = open(self.filename_result, "w")
		fileobj.close()
		self.Globaly = 0
		self.Xorcount = 0
		self.variablein0 = []
		self.variableoutN = []

	
	def CreateObjectiveFunction(self):
		"""
		Create objective function of the MILP model
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("MINIMIZE\n")
		eqn = []
		for i in range(0, self.Round * 32):
			eqn.append("y" + str(i))
		temp = " + ".join(eqn)
		fileobj.write(temp)
		fileobj.write("\n")
		fileobj.close()

	
	@staticmethod
	def CreateVariables_SHADOW(n, pos):
		"""
		Generate the variables used in the model.
		"""
		array = []
		for i in range(0, 8):
			# array.append(("x" + "_" + str(n) + "_" + str(pos) + "_" + str(i)))
			array.append(("x" + "_" + str(n) + "_" + pos + "_" + str(i)))
		return array	

	@staticmethod
	def CreateTempVariables_SHADOW(n,c):
		array = []
		for i in range(0, 8):
			array.append(("temp" + "_" + str(n) + "_" + c + "_" + str(i)))
		return array
	
	def ConstraintsBy_rotate_AND_SHADOW(self, variable1, variable2):
		"""
		Generate the constraints by nolinear layer.
		"""
		fileobj = open(self.filename_model, "a")
		for k in range(0, 8):

			fileobj.write("y" + str(self.Globaly) + " - " + variable2[k] + " >= 0")
			# fileobj.write(str(variable1[(k+1)%8]) + " + " + str(variable1[(k+7)%8]) + " - " + variable2[k] + " >= 0")
			fileobj.write("\n")
			fileobj.write(str(variable1[(k+1)%8]) + " - y" + str(self.Globaly) + " <= 0")
			fileobj.write("\n")
			fileobj.write(str(variable1[(k+7)%8]) + " - y" + str(self.Globaly) + " <= 0")
			fileobj.write("\n")
			fileobj.write(str(variable1[(k+1)%8]) + " + " + str(variable1[(k+7)%8]) + " - y" + str(self.Globaly) + " >= 0")
			fileobj.write("\n")
			self.Globaly += 1
		fileobj.close()

	def XORLayer(self, variable1, variable2, variable3):
		fileobj = open(self.filename_model, "a")
		for i in range(8):
			fileobj.write(
				str(variable1[i]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " - 2 a" + str(
					self.Xorcount) + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable1[i] + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable2[i] + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable3[i] + " >= 0\n")
			fileobj.write(str(variable1[i]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " <= 2\n")
			self.Xorcount += 1
		fileobj.close()

	def XORLayer_Shadow_2(self, variable1, variable2, variable3):
		fileobj = open(self.filename_model, "a")
		for i in range(8):
			fileobj.write(
				str(variable1[(i+2)%8]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " - 2 a" + str(
					self.Xorcount) + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable1[(i+2)%8] + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable2[i] + " >= 0\n")
			fileobj.write('a' + str(self.Xorcount) + ' - ' + variable3[i] + " >= 0\n")
			fileobj.write(str(variable1[(i+2)%8]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " <= 2\n")
			self.Xorcount += 1
		fileobj.close()

	def XORLayer_2017Sasaki(self, variable1, variable2, variable3, length):
		fileobj = open(self.filename_model, "a")
		for i in range(length):
			fileobj.write(str(variable1[i]) + " + " + str(variable2[i]) + " - " + str(variable3[i]) + " >= 0\n")
			fileobj.write(str(variable1[i]) + " + " + str(variable3[i]) + " - " + str(variable2[i]) + " >= 0\n")
			fileobj.write(str(variable3[i]) + " + " + str(variable2[i]) + " - " + str(variable1[i]) + " >= 0\n")
			fileobj.write(str(variable1[i]) + " + " + str(variable2[i]) + " + " + str(variable3[i]) + " <= 2\n")
		fileobj.close()


	def Constraints_kernelmodule_SHADOW(self, round, variable_IN_L, variable_IN_R, variable_OUT_R, identification):
		"""
		Generate the constraints for f-function by kernelmodule_SHADOW.
		"""
		variabletemp_AND = SHADOW.CreateTempVariables_SHADOW(round, str(identification) + "_and")
		variabletemp_XOR = SHADOW.CreateTempVariables_SHADOW(round, str(identification) + "_xor")	
		self.ConstraintsBy_rotate_AND_SHADOW(variable_IN_L, variabletemp_AND)
		self.XORLayer(variabletemp_AND, variable_IN_R, variabletemp_XOR)
		self.XORLayer_Shadow_2(variable_IN_L, variabletemp_XOR, variable_OUT_R)

	def Constraint(self):
		"""
		Generate the constraints used in the MILP model.
		"""
		assert (self.Round >= 1)
		fileobj = open(self.filename_model, "a")
		fileobj.write("Subject To\n")
		fileobj.close()

		for i in range(0, self.Round):
			variableinX_a = SHADOW.CreateVariables_SHADOW(i, "a")
			variableinX_b = SHADOW.CreateVariables_SHADOW(i, "b")
			variableinX_c = SHADOW.CreateVariables_SHADOW(i, "c")
			variableinX_d = SHADOW.CreateVariables_SHADOW(i, "d")
			variableoutX_a = SHADOW.CreateVariables_SHADOW(i+1, "a")
			variableoutX_b = SHADOW.CreateVariables_SHADOW(i+1, "b")
			variableoutX_c = SHADOW.CreateVariables_SHADOW(i+1, "c")
			variableoutX_d = SHADOW.CreateVariables_SHADOW(i+1, "d")
			self.Constraints_kernelmodule_SHADOW(i+1, variableinX_a, variableinX_b, variableoutX_c, "a")
			self.Constraints_kernelmodule_SHADOW(i+1, variableinX_c, variableinX_d, variableoutX_a, "b")
			self.Constraints_kernelmodule_SHADOW(i+1, variableoutX_c, variableinX_a, variableoutX_b, "c")
			self.Constraints_kernelmodule_SHADOW(i+1, variableoutX_a, variableinX_c, variableoutX_d, "d")

		return variableoutX_a, variableoutX_b, variableoutX_c, variableoutX_d


	def VariableBinary(self):
		"""
		Specify the variable type.
		"""
		fileobj = open(self.filename_model, "a")
		fileobj.write("Binary\n")
		for i in range(0, self.Round + 1):
			varin_a = self.CreateVariables_SHADOW(i, 'a')
			for item in varin_a:
				fileobj.write(str(item) + "\n")

			varin_b = self.CreateVariables_SHADOW(i, 'b')
			for item in varin_b:
				fileobj.write(str(item) + "\n")

			varin_c = self.CreateVariables_SHADOW(i, 'c')
			for item in varin_c:
				fileobj.write(str(item) + "\n")

			varin_d = self.CreateVariables_SHADOW(i, 'd')
			for item in varin_d:
				fileobj.write(str(item) + "\n")
				

		for i in range(1, self.Round + 1):
			vartemp_a_and =  SHADOW.CreateTempVariables_SHADOW(i,'a_and')
			vartemp_a_xor =  SHADOW.CreateTempVariables_SHADOW(i,'a_xor')
			vartemp_b_and =  SHADOW.CreateTempVariables_SHADOW(i,'b_and')
			vartemp_b_xor =  SHADOW.CreateTempVariables_SHADOW(i,'b_xor')			
			vartemp_c_and =  SHADOW.CreateTempVariables_SHADOW(i,'c_and')
			vartemp_c_xor =  SHADOW.CreateTempVariables_SHADOW(i,'c_xor')
			vartemp_d_and =  SHADOW.CreateTempVariables_SHADOW(i,'d_and')
			vartemp_d_xor =  SHADOW.CreateTempVariables_SHADOW(i,'d_xor')
			for item in vartemp_a_and:
				fileobj.write(str(item) + "\n")
			for item in vartemp_a_xor:
				fileobj.write(str(item) + "\n")		
			for item in vartemp_b_and:
				fileobj.write(str(item) + "\n")
			for item in vartemp_b_xor:
				fileobj.write(str(item) + "\n")	
			for item in vartemp_c_and:
				fileobj.write(str(item) + "\n")
			for item in vartemp_c_xor:
				fileobj.write(str(item) + "\n")	
			for item in vartemp_d_and:
				fileobj.write(str(item) + "\n")
			for item in vartemp_d_xor:
				fileobj.write(str(item) + "\n")							
		for i in range(0, self.Xorcount):
			fileobj.write('a' + str(i) + '\n')
		for i in range(0, self.Globaly):
			fileobj.write('y' + str(i) + '\n')
		fileobj.write("END")
		fileobj.close()


	def WriteObjective(self, obj):
		"""
		Write the objective value into filename_result.
		"""
		fileobj = open(self.filename_result, "a")
		fileobj.write("The objective value = %d\n" % obj.getValue())
		eqn1 = []
		eqn2 = []
		for i in range(0, self.blocksize):
			u = obj.getVar(i)
			if u.getAttr("x") != 0:
				eqn1.append(u.getAttr('VarName'))
				eqn2.append(u.getAttr('x'))
		length = len(eqn1)
		for i in range(0, length):
			s = eqn1[i] + "=" + str(eqn2[i])
			fileobj.write(s)
			fileobj.write("\n")
		fileobj.close()

	def Init(self, outX1, outX2, outX3, outX4):
		"""
		Iterative Difference Limits.
		"""
		fileobj = open(self.filename_model, "a")
		start_a, start_b, start_c, start_d = SHADOW.CreateVariables_SHADOW(0, "a"), SHADOW.CreateVariables_SHADOW(0, "b"), SHADOW.CreateVariables_SHADOW(0, "c"), SHADOW.CreateVariables_SHADOW(0, "d")
		for i in range(8):
			fileobj.write(str(start_a[i]) + " - " + str(outX1[i]) + " = 0 " "\n")
			fileobj.write(str(start_b[i]) + " - " + str(outX2[i]) + " = 0 " "\n")
			fileobj.write(str(start_c[i]) + " - " + str(outX3[i]) + " = 0 " "\n")
			fileobj.write(str(start_d[i]) + " - " + str(outX4[i]) + " = 0 " "\n")

		fileobj.close()


		"""
		Limit inputs to not all zeros.
		"""
		fileobj = open(self.filename_model, "a")
		Init_str = ' + '.join('x_0_a_' + str(i) for i in range(0, 8)) + ' + ' + ' + '.join('x_0_b_' + str(i) for i in range(0, 8)) + ' + ' + ' + '.join('x_0_c_' + str(i) for i in range(0, 8)) + ' + ' + ' + '.join('x_0_d_' + str(i) for i in range(0, 8)) + ' >= 1' #   语法留意学习,注意元素与计算符号间存在空格要
		fileobj.write(Init_str + '\n')
		fileobj.close()


	def MakeModel(self):
		"""
		Generate the MILP model of SHADOW given the round number and activebits.
		"""
		self.CreateObjectiveFunction()
		outX1, outX2, outX3, outX4 = self.Constraint()
		self.Init(outX1, outX2, outX3, outX4)
		self.VariableBinary()

	def SolveModel(self):
		"""
		Solve the MILP model to search the .
		"""
		time_start = time.time()
		m = read(self.filename_model)
		m.optimize()
		fileobj = open(self.filename_result, "a")
		if m.Status == 2:

			print("feasible")
			for i in range(0, self.Round + 1):
				fileobj.write('ROUND_' + str(i) + ':')
				# fileobj.write("\n")

				# fileobj.write('X' + str(i) + '_IN_1__' )
				for j in range(8):					
					a = m.getVarByName('x_' + str(i) + "_a_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))					
				# fileobj.write("\n")	

				fileobj.write('_')
				for j in range(8):					
					a = m.getVarByName('x_' + str(i) + "_b_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))				
				# fileobj.write("\n")	

				fileobj.write('_')
				for j in range(8):					
					a = m.getVarByName('x_' + str(i) + "_c_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))				
				# fileobj.write("\n")	

				fileobj.write('_')
				for j in range(8):					
					a = m.getVarByName('x_' + str(i) + "_d_" + str(j))					
					fileobj.write(str(int(a.getAttr("x"))))					
				fileobj.write("\n")	

				# for j in range(8):					
				# 	a = m.getVarByName('temp_' + str(i+1) + "_a_and_" + str(j))			
				# 	fileobj.write(str(int(a.getAttr("x"))))					
				# # fileobj.write("\n")	
				# for j in range(8):					
				# 	a = m.getVarByName('temp_' + str(i+1) + "_b_and_" + str(j))			
				# 	fileobj.write(str(int(a.getAttr("x"))))					
				# # fileobj.write("\n")
				# for j in range(8):					
				# 	a = m.getVarByName('temp_' + str(i+1) + "_c_and_" + str(j))			
				# 	fileobj.write(str(int(a.getAttr("x"))))					
				# # fileobj.write("\n")				
				# for j in range(8):					
				# 	a = m.getVarByName('temp_' + str(i+1) + "_d_and_" + str(j))			
				# 	fileobj.write(str(int(a.getAttr("x"))))					
				# fileobj.write("\n")

			for i in range(0, self.Globaly):
				a = m.getVarByName('y' + str(i))
				fileobj.write('y' + str(i) + ": " + str(a.getAttr("x")))
				fileobj.write("\n")
		print(m.getObjective().getValue())
		time_end = time.time()
		print(("Time used = " + str(time_end - time_start)))
		fileobj.close()


if __name__ == "__main__":
	ROUND = int(input("Input the target round number: "))
	while not (ROUND > 0):
		print("Input a round number greater than 0.")
		ROUND = int(input("Input the target round number again: "))
	
	shadow = SHADOW(ROUND)
	
	shadow.MakeModel()
	
	shadow.SolveModel()

