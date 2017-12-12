class ParserLR0:
	G = {}  # 文法
	I = {}  # 状态
	C = {}  # 状态集
	C_go = set()
	C_end = set()
	tb_GOTO = {}
	tb_ACTION = {}

	DOT = '.'

	def __init__(self):
		'''
		S' -> S
		S  -> BB
		B  -> aB
		B  -> b
		'''
		self.G = {
			"S'": {'S'},
			'S': {'BB'},
			'B': {'aB', 'b'}
		}

		self.X = set(k for i in self.G.values() for j in i for k in j)
		self.Nt = set(i for i in self.G.keys())

		self.items()
		# self.print_G()
		# self.print_C()
		self.print_TB()

	def closure(self, I):
		J = I
		Flag_add = True
		while Flag_add:
			Flag_add = False
			for one_key in list(J):  # use list(J) instead of J.keys()
				for one in list(J[one_key]):
					Nt = self.find_NT(one)
					if Nt:
						find_string = self.G.get(Nt)
						# print(find_string)
						if find_string and not (Nt in J):
							J[Nt] = set()
							for one_string in find_string:
								J[Nt].add(self.DOT + one_string)
								Flag_add = True

						if find_string and (Nt in J):
							for one_string in find_string:
								J[Nt].add(self.DOT + one_string)
		return J

	def goto(self, I, x):
		J = {}
		for i in I:
			for one_string in I[i]:
				place = one_string.find(self.DOT + x)
				if place > -1:
					J[i] = set()
					J[i].add(self.back_on(one_string))

		# print(I,"--GO--",x,"--TO--",self.closure(J))

		return self.closure(J)

	def items(self):
		I = {"S'": {".S"}}
		self.C = {}
		self.C['I0'] = self.closure(I)
		Flag_add = True
		while Flag_add:
			Flag_add = False
			for i in list(self.C):
				# print(self.C[i],self.X)
				for x in self.X:
					GT = self.goto(self.C[i], x)
					find_i = self.find_in_C(GT)
					if GT and not find_i:
						new_i = 'I' + str(len(self.C))
						self.C[new_i] = GT
						self.C_go.add((i, x, new_i))
						self.find_C_end(new_i,GT)  # DOT in end
						Flag_add = True
					elif GT:
						self.C_go.add((i, x, find_i))

	def find_NT(self, one_string):
		Nt_place = one_string.find(self.DOT)
		if Nt_place == len(one_string) - 1:  # DOT in end
			return False
		else:
			Nt = one_string[Nt_place + 1]
			if Nt in self.Nt:
				return Nt
		return False

	def find_C_end(self,i,GT):
		for one in GT.values():
			for one_string in one:
				Nt_place = one_string.find(self.DOT)
				if Nt_place == len(one_string) - 1:
					self.C_end.add(i)


	def back_on(self, one_string):  # .SB -> S.B
		b_o_s = ""
		sign = False
		for t in one_string:
			if (t == '.'):
				sign = True
				continue
			b_o_s = b_o_s + t
			if sign:
				b_o_s = b_o_s + '.'
				sign = False
		return b_o_s

	def find_in_C(self, GT):  # !!!!
		for i in self.C:
			if self.C[i] == GT:
				return i
		return False

	def print_G(self):
		print("---------G---------")
		for i in self.G:
			for j in self.G[i]:
				print('{} -> {}'.format(i, j))

	def print_I(self):
		print("---------I---------")
		for i in self.I:
			for j in self.I[i]:
				print('{} -> {}'.format(i, j))

	def print_C(self):

		print("---------C---------")
		print(self.C)
		for i in self.C:
			print("----", i, "----")
			for j in self.C[i]:
				for k in self.C[i][j]:
					print('{} -> {}'.format(j, k))
		print("----C_go----")
		print(self.C_go)
		print("----C_end----")
		print(self.C_end)

	def createTable(self):
		for i in self.C:
			self.tb_GOTO[i] = {}
			self.tb_ACTION[i] = {}
			for one in self.C_go:
				if (one[0] == i):
					if (one[1] in self.Nt):
						self.tb_GOTO[i][one[1]] = one[2]
					else:
						self.tb_ACTION[i][one[1]] = one[2]


	def find_R(self,In,x):
		for values in self.C[In].values():
			for one in values:
				s = one[:-1]
				k = 0
				for g in self.G.values():         #使用文法中的哪条产生式
					for g_i in g:
						k = k+1
						if s == g_i:
							if s == 'S' and x != '$':
								return "-"
							return "R"+str(k)
		return -1

	def print_TB(self):
		self.createTable()
		print("------ACTION------")
		print(self.tb_ACTION)
		print("------GOTO2------")
		print(self.tb_GOTO)

		print("------Table------")
		print('{0:5}'.format(""), end="")

		self.X.add("$")  # warning!!!
		for one in self.X:
			print('{0:5}'.format(one), end="")
		print()
		for i in range(len(self.C)):
				In = 'I' + str(i)
				print('{0:2}{1:3}'.format(i,""), end="")

				if In in self.C_end:
					for one in self.X:
						if one in self.Nt:
							g = "-"
						else:
							g = self.find_R(In,one)
						print('{0:5}'.format(g), end="")
				else:
					for one in self.X:
						if one in self.Nt:
							g = self.tb_GOTO[In].get(one,"-")
						else:
							g = self.tb_ACTION[In].get(one,"-")
						if g != "-":
							g = 'S' + g[1]
						print('{0:5}'.format(g), end="")
				print()

class ParserLR:
	def __init__():
		pass

lr0 = ParserLR0()
