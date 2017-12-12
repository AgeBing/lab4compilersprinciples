#coding=utf-8

def jleft(c):
  global G
  for i in G[c]:
    if c == i[0]:
      return True
  return False

def gnend():
  UnTer = set(G.keys())
  print UnTer
  for i in range(65,91):
    if chr(i) not in UnTer:
      return chr(i)

def gfirst(c):
  global First
  a = set()
  for i in c:
    if i in Ter:
      a.add(i)
      return a
    else:
      if '^' in First[i]:
        a = a|First[i]
      else:
        a = First[i]
        return a
  return a

def ffirst(D,c):
  global First
  global G
  if c in Ter:
    First[D].add(c)
  else:
    for i in G[c]:
      if D==c or D==i[0] or c==i[0]:
        continue
      ffirst(D,i[0])

def jempty(c):
  global G
  flag = True
  if len(c) == 0:
    return False
  for i in c:
    if i == '^':
      temp = True
    elif i in Ter:
      flag = False
      break
    else:
      temp = False
      for j in G[i]:
        if j[-1] == i:
          continue
        temp = temp|jempty(j)
    flag = flag & temp
  return flag

def ffollow1(c):
  global Follow
  for i in range(0,len(c)):
    if c[i] in UnTer:
      Follow[c[i]] = Follow[c[i]]|(gfirst(c[:i])-set('^'))

def ffollow2(D,c):
  global Follow
  for i in range(0,len(c)):
    if (i == 0 and c[0] in UnTer) or jempty(c[:i]):
      Follow[c[i]] = Follow[c[i]]|Follow[D]


G = {}
G['E'] = []
G['E'].append('E+T')
G['E'].append('T')
G['T'] = []
G['T'].append('T*F')
G['T'].append('F')
G['F'] = []
G['F'].append('(E)')
G['F'].append('i')

First = {}
First['E'] = set()
First['F'] = set()
First['T'] = set()

Follow = {}
Follow['E'] = set('#')
Follow['F'] = set()
Follow['T'] = set()

for i in G.keys():
  print("NOW",i)
  if jleft(i):
    ch = gnend()
    print "gnend",ch
    G[ch] = []
    First[ch] = set()
    Follow[ch] = set()
    temp=[]
    k=0
    for j in G[i]:
      if i == j[0]:
        temp.append(j)
        G[ch].append(j[1:]+ch)
        if '^' not in G[ch]:
          G[ch].append('^')
      else:
        G[i].remove(j)
        G[i].insert(k,j+ch)
      k += 1
    for j in temp:
      G[i].remove(j)
print("kes",G.keys())
print 'AFTER'
for i in G:
  for j in G[i]:
    print '%s->%s'%(i,j)

M = {}

All = set(k for i in G.values() for j in i for k in j)
UnTer = set(G.keys())
Ter = All - UnTer
Ter.add('#')

for i in G:
  for j in G[i]:
    ffirst(i,j[0])


for i in G:
  for j in G[i]:
    ffollow1(j[::-1])

for i in G:
  for j in G[i]:
    ffollow2(i,j[::-1])

print '消除左递归之后的文法：'
for i in G:
  for j in G[i]:
    print '%s->%s'%(i,j)
print '\nFIRST集：'
for i in First:
  print i+':',
  for j in First[i]:
    print j,
  print '\n',
print '\nFOLLOW集：'
for i in Follow:
  print i+':',
  for j in Follow[i]:
    print j,
  print '\n',

for i in UnTer:
  for j in Ter:
    M[i,j]=[]

for i in G:
  for j in G[i]:
    for k in gfirst(j):
      M[i,k].append(j)
    if '^' in gfirst(j):
      for l in Follow[i]:
        M[i,l].append(j)

print '\n分析表：'
print '%-5s'%(''),
for j in Ter:
  print '%-5s'%(j),
print '\n',
for i in UnTer:
  print '%-5s'%(i),
  for j in Ter:
    d = M[i,j]
    print '%-5s'%(d[0] if len(d)>0 else 'None'),
  print '\n'

print '分析字符串过程：'
s='i+i+i#'
# s='(i-i(*i)#'
stack='E#'
while True:
  if len(s)==0 and len(stack)==0:
    print '是句子'
    break
  if stack[0]=='^':
    stack=stack.replace(stack[0],'',1)
  print '%-10s%10s' %(stack[::-1],s)
  if stack[0]==s[0]:
    stack=stack.replace(stack[0],'',1)
    s=s.replace(s[0],'',1)
  else:
    if M.get((stack[0],s[0]),0) == 0 or len(M[stack[0],s[0]]) == 0:
      print '不是句子'
      break
    else:
      stack=stack.replace(stack[0],M[stack[0],s[0]][0],1)