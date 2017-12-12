> ##Project 2. 确定的自顶向下分析 LL（1）
> ####编译原理
> ######俞科杰 软工1503 201526810129



#1. Overview
###1.1 目标
- *输入* -> 文法
- *输出* -> 预测分析表
- 通过预测分析表判断某一**语句**是否符合该**文法**

###1.2 过程
1. 判断是否为 LL(1) 文法
 - 提取左公因子
 - 消除左递归
2. 构建预测分析表
    - 构造FIRST集 和 FOLLOW 集
    - 判断是否符合 LL(1)
    - 构造表
3. 表驱动LL(1)分析程序
    - 预测分析表
    - 分析栈
    - 分析程序

#2.具体实现

###2.0 构造方法

```
#假设输入文法如下
E -> E + T | T
T -> T * F | F
F -> (E) | i
#文法
G = {
    'E' : ['E + T' , 'T'],
    'T' : ['T * F' , 'F'],
    'F' : ['(E)' , 'i']
}
#First 集
Fr = {
    'E' : {},
    'T' : {},
    'F' : {}
}
#Follow集
Fw = {
    'E' : {},
    'T' : {},
    'F' : {}
}
#预测分析表
M = {
    
}
```

###2.1 消除左递归和提取左公因子
#####2.1.2 原因
若存在上述情况，就会出现对于某一**非终结符**，其某些**产生式**的**可选集**会有相交的情况，即无法进行确定性预测，即无法正确构造**预测分析表**。
即该文法不是 LL(1)文法。

#####2.1.2 提取左公因子
```
   A --> aB|aC    ==>    A --> aM 、M --> B|C     
```
#####2.1.3 消除直接左递归
左递归 -> 右递归

```
   S --> Sa|b    ==>    S --> bM 、 M --> aM|&
```

#####2.1.3 消除间接左递归
```
   A --> aB|Bb 、 B --> Ac|d   
   ==>    代入(B产生式中A代掉) A 产生式还是不变 
   B --> aBc|Bbc|d 、 A --> aB|Bb
   ==>    B --> aBcM|dM 、 M --> bcM|& 、A --> aB|Bb
```
#####2.1.4 实现
```
def clean_left_recur(self):
	for nt in list(self.G):
		if self.__dete_dir_left(nt):  #判断递归
			newNt = self.__gene_new_NonTer() #生成新非终结符
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
```

#####2.1.5 结果
```
#Before
---------G---------
E -> E+T
E -> T
T -> T*F
T -> F
F -> (E)
F -> i
#After
---------G---------
E -> TA
T -> FB
F -> (E)
F -> i
A -> +TA
A -> &
B -> *FB
B -> &
```
###2.2 求 FIRST 、FOLLOW 集及预测分析表
#### 2.2.1求FIRST集算法
 ![](/Users/apple/Documents/大三上作业/编译原理/figure/FIRST 算法.png)
 
 
##### 2.2.1.1 求FIRST集 实现
 
```
for i in self.G:
			for j in self.G[i]:
				self.__dete_first(i,j

def __dete_first(self,nt,t):  #非终结符 规则右边
	if t in self.Te:       #为终结符 
		self.Fr[nt].add(t)
	else:
		for i in self.G[nt]:
			if nt == t or nt == i[0] or t == i[0]:   # 遇到 直接左递归，间接左递归，自己
				continue
			self.__dete_first(nt,i[0])
	pass
```

##### 2.2.1.2 求FIRST集 结果
```
---------FIRST---------
E :  i ( 
F :  i ( 
T :  i ( 
A :  & + 
B :  & * 
```

#### 2.2.2 求FOLLOW集算法
![](/Users/apple/Documents/大三上作业/编译原理/figure/FOLLOW算法.png)

##### 2.2.2.1 求FOLLOW集算法实现
```
for i in self.G:
	for j in self.G[i]:
		self.__dete_follow1(j[::-1])
for i in self.G:
	for j in self.G[i]:
		self.__dete_follow2(i,j[::-1])
		
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
```

```
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
```
##### 2.2.2.2 求FOLLOW集算法结果
```
---------FOLLOW---------
E :  ) # 
F :  ) + # * 
T :  ) + # 
A :  ) # 
B :  ) + # 
```

#### 2.2.3 构造预测分析表

![](/Users/apple/Documents/大三上作业/编译原理/figure/SELECT算法.png)

```
# 预测分析表 T = {}
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
```


```
-----------------Predict Table---------------
      )     &     i     (     +     *     #     
B     &     &     -     -     &     *FB   &     
F     -     -     i     (E)   -     -     -     
E     -     -     TA    TA    -     -     -     
A     &     &     -     -     +TA   -     &     
T     -     -     FB    FB    -     -     - 
```
###2.3 根据预测分析表分析文法
#####2.3.1 组成
- 预测分析表 M  =>  2维，左边对应分析栈中的**非终结符**，右边对应串中的**终结符**
- 输入串 string  => 从左往右
- 分析栈 stack  => 左边栈底，右边栈顶

#####2.3.2 步骤
- 分析 =>  分析栈的**栈顶**根据**预测分析表**以及**串的最左端**进行匹配，弹出栈顶，压入匹配项
- 替换 =>  分析栈和输入串遇到相同的**非终结符**，则都去掉

#####2.3.3 判断

- 正确 => 遇到分析栈和输入串都为空，输出『YES』，表示语句被文法接受。
- 错误 => 
    - 1.栈顶的终结符和串首不匹配
    - 2.栈顶的非终结符与串首在预测分析表中对应信息不匹配   

#####2.3.4 结果
```
----------Analyse-----------
#E        i+i+i#    
#AT       i+i+i#    
#ABF      i+i+i#    
#ABi      i+i+i#    
#AB       +i+i#     
#A        +i+i#     
#AT+      +i+i#     
#AT       i+i#      
#ABF      i+i#      
#ABi      i+i#      
#AB       +i#       
#A        +i#       
#AT+      +i#       
#AT       i#        
#ABF      i#        
#ABi      i#        
#AB       #         
#A        #         
#         #         
YES!
```

#3.其他
在确定自顶向下语法分析中还包含一些其他内容，实验并未要求。

###3.1 递归下降的 LL(1)分析法
是区别于**表驱动分析程序**的一种分析方法。
通过调用每一个**非终结符**的**分析子程序**进行分析。

###3.2 LL(1)分析时的错误处理
即当出现上述预测分析中产生错误的两种情况时。需进行**报错**和**错误恢复**，
一种方式是通过设置**同步词法单元**的应急模式（或恐慌模式）。

