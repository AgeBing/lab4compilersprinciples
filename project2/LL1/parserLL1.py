class ParserLL1:
	G = {}   #文法
	Fr ={}   #FIRST集
	Fw ={}	 #FOLLOW集
	T = {}	 #预测分析表
	AllWord = set() #所以出现过的符号
	Te = set()   #终结符 Terminator
	Nt = set()   #非终结符 Non-Terminator


	def __init__(self):
		self.G['E'] = []
		self.G['E'].append('E+T')
		self.G['E'].append('T')
		self.G['T'] = []
		self.G['T'].append('T*F')
		self.G['T'].append('F')
		self.G['F'] = []
		self.G['F'].append('(E)')
		self.G['F'].append('i')

		self.Fr['E'] = set()
		self.Fr['F'] = set()
		self.Fr['T'] = set()
		self.Fw['E'] = set('#')
		self.Fw['F'] = set()
		self.Fw['T'] = set()

	def clean_left_recur(self):
		for nt in list(self.G):
			if self.__dete_dir_left(nt):
				newNt = self.__gene_new_NonTer()
				self.G[newNt] = []
				self.Fr[newNt] =set()
				self.Fw[newNt] =set()
				temp = []
				k = 0
				for oneFormula in self.G[nt]:
					if nt == oneFormula[0]:
						temp.append(oneFormula)
						self.G[newNt].append(oneFormula[1:]+newNt)
						if "&" not in self.G[newNt]:
							self.G[newNt].append("&")
					else:
						self.G[nt].remove(oneFormula)
						self.G[nt].insert(k,oneFormula+newNt)
					k += 1
				for oneFormula in temp:
					self.G[nt].remove(oneFormula)

		self.__update_words_set()

	def gene_Fr_and_Fw(self):
		for i in self.G:
			for j in self.G[i]:
				self.__dete_first(i,j[0])
		for i in self.G:
			for j in self.G[i]:
				self.__dete_follow1(j[::-1])
		for i in self.G:
			for j in self.G[i]:
				self.__dete_follow2(i,j[::-1])
		pass

	def gene_pred_table(self):
		for i in self.Nt:
			for j in self.Te:
				self.T[i,j] = []

		for i in self.G:
			for j in self.G[i]:
				for k in self.__group_first(j):
					self.T[i,k].append(j)
				if '&' in self.__group_first(j):
					for l in self.Fw[i]:
						self.T[i,l].append(j)
		pass

	def analyse(self,string):
		print('----------Analyse-----------')
		s = string
		stack = 'E#'
		while True:
			if len(s) == 0 and len(stack) == 0:
				print("YES!")
				break
			if stack[0] == '&':
				stack = stack.replace(stack[0],'',1)
			print('{0:10}{1:10}'.format(stack[::-1],s))
			
			if stack[0] == s[0]:
				stack = stack.replace(stack[0],'',1)
				s = s.replace(s[0],'',1)
			else:
				if self.T.get((stack[0],s[0]),0) == 0 or len(self.T[stack[0],s[0]]) == 0:
					print('NO!')
					break
				else:
					stack=stack.replace(stack[0],self.T[stack[0],s[0]][0],1)
		pass
		
	def __dete_dir_left(self,nt): #传入非终结符
		for i in self.G[nt]:
			if nt == i[0]:
				return True
		return False

	def __dete_first(self,nt,t):  #非终结符 规则右边
		if t in self.Te:       #为终结符 
			self.Fr[nt].add(t)
		else:
			for i in self.G[t]:
				if nt == t or nt == i[0] or t == i[0]:   # 遇到 直接左递归，间接左递归，自己
					continue
				self.__dete_first(nt,i[0])
		pass

	def __dete_follow1(self,tr): #规则右边 reversed
		for i in range(0,len(tr)):
			if tr[i] in self.Nt: #为非终结符
				self.Fw[tr[i]] = self.Fw[tr[i]] | (self.__group_first(tr[:i]) - set('&'))
			pass

	def __dete_follow2(self,nt,tr): #非终结符 规则右边 reversed
		for i in range(0,len(tr)):
			if(i == 0 and tr[0] in self.Nt) or self.__group_empty(tr[:i]):
				self.Fw[tr[i]] = self.Fw[tr[i]] | self.Fw[nt]
			pass

	def __group_first(self,t):
		a = set()
		for i in t:
			if i in self.Te:
				a.add(i)
				return a
			else:
				if "&" in self.Fr[i]:
					a = a | self.Fr[i]
				else:
					a = self.Fr[i]
					return a
		return a
		pass

	def __group_empty(self,t):
		flag  = True
		if len(t) == 0:
			return False
		for i in t:
			if i == '&':
				temp = True
			elif i in self.Te:
				flag = False
				break
			else:   #为非终结符
				temp = False
				for j in self.G[i]:
					if j[-1] == i:
						continue
					temp = temp | self.__group_empty(j)
			flag = flag & temp
			if(flag!=True):
				return False
		return flag
		pass

	def __gene_new_NonTer(self): #生成新非终结符
		for i in range(65,91):
			if chr(i) not in set(self.G.keys()):
				newNt = chr(i)
				return newNt

	def __update_words_set(self):
		self.AllWord = set(k for i in self.G.values() for j in i for k in j)
		self.Nt = set(self.G.keys())
		self.Te = self.AllWord - self.Nt
		self.Te.add('#')

		print('-------Word Set---------')
		print("Terminator") 
		for one in self.Te:
			print(one,"  ",end='')
		print()
		print("Non-Terminator")
		for one in self.Nt:
			print(one,"  ",end='')
		print()

	def print_G(self):
		print("---------G---------")
		for i in self.G:
			for j in self.G[i]:
				print('{} -> {}'.format(i,j))

	def print_Fr(self):
		print("---------FIRST---------")
		for i in self.Fr:
			print(i,": ",end=" ")
			for j in self.Fr[i]:
				print(j,end=" ")
			print()

	def print_Fw(self):
		print("---------FOLLOW---------")
		for i in self.Fw:
			print(i,": ",end=" ")
			for j in self.Fw[i]:
				print(j,end=" ")
			print()

	def print_Tb(self): 
		print("-----------------Predict Table---------------")
		print("      ",end="")
		for j in self.Te:
			print('{0:5}'.format(j),end=" ")
		print()
		for i in self.Nt:
			print('{0:5}'.format(i),end=" ")
			for j in self.Te:
				d = self.T[i,j]
				if(len(d)>0):
					p = d[0]
				else:
					p = '-'
				print('{0:5}'.format(p),end=" ")
			print()
		pass

	def go(self,string):
		self.print_G()
		self.clean_left_recur()
		self.gene_Fr_and_Fw()
		self.gene_pred_table()
		self.print_G()
		self.print_Fr()
		self.print_Fw()
		self.print_Tb()
		self.analyse(string)
		pass

x = ParserLL1()
x.go('i+i+i#')
# x.go('(i-i(*i)#')
# x.print_G()
# x.clean_left_recur()
# x.gene_Fr_and_Fw()
# x.gene_pred_table()
# x.print_G()
# x.print_Fr()
# x.print_Fw()
# x.print_Tb()
# x.analyse('i+i+i#')


