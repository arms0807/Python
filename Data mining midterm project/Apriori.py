import mysql.connector
import sys
from itertools import permutations

mydb = mysql.connector.connect(
  host="localhost",
  database="data_mining",
  user="root",
  passwd="password"
)
mycursor = mydb.cursor()

def Apriori(columns, select_db, rows):
	count = 0
	columns_name = []
	every_support = {}
	for i in columns:
		if(i[0]=='ID'):
			continue
		columns_name.append(i[0])
	columns_name = sorted(columns_name)
	for i in columns_name:
		mycursor.execute("select count(ID) from "+select_db+" where "+i+" = 1")
		result = mycursor.fetchall()
		if float(result[0][0]/rows)>=support_val:
			every_support[i] = float(result[0][0]/rows)
	all_support.update(every_support)
	return every_support, columns_name, count

def Apriori1(every_support, columns_name, count, select_db, rows):
	count+=1
	key = [i for i in every_support.keys()]
	every_support = {}
	a, b, c, d = "select count(ID) from ", " where ", " = 1 and ", " = 1"
	for i in range(len(key)):
		sql = ''
		x = key[i].split(" ")
		if len(x)==1:
			sql+=x[0] + c
		else:
			for k in range(len(x)):
				sql += x[k] + c
		for j in range((columns_name.index(x[count-1])+1), len(columns_name)):
			sql_last = a + select_db + b + sql + columns_name[j] + d
			mycursor.execute(str(sql_last))
			result = float(mycursor.fetchall()[0][0]/rows)
			if result>=support_val:
				every_support[key[i]+" "+columns_name[j]] = result
	all_support.update(every_support)
	return every_support, count

def Permutation(key):
	d, ans = [], []
	for i in key:
		d2 = []
		d2+=i.split(' ')
		d.append(d2)
	for i in d:
		for j in permutations(i):
			ans.append(j)
	return ans
	

def Confidence(every_support, all_support, count):
	confidence_element = {}
	if not every_support:
		return
	key = [i for i in every_support.keys()]
	permutate_name = Permutation(key)
	arrow = len(permutate_name[0])-1
	name = []
	for j in permutate_name:
		b = []
		for k in range(arrow):
			b+=[j[k]]
			c = sorted(b)
			name.append(str(' '.join(c)))
	name = sorted(set(name))
	if len(key[0])-arrow==2:
		for i in name:
			for j in key:
				if i in j:
					result = every_support[j]/all_support[i]
					if result>=confidence_val:
						confidence_element[i+"->"+j] = result
	else:
		for j in key: 
			for i in name: 
				amount = 0
				for k in i: 
					if k in j:
						amount+=1
					else:
						break
				if amount == len(i):
					result = every_support[j]/all_support[i]
					if result>=confidence_val:
						confidence_element[i+"->"+j] = result
	return confidence_element

def setSupport():
	n = input("Enter a minimum support value \n")
	return n

def setConfidence():
	n = input("Enter a minimum confidence value\n")
	return n

def setInput():
	n = input("Enter a number from 1 to 5 to choose which database you want to see\n")
	return n

def db(x):
	return{1:'transactions1', 2:'transactions2', 3:'transactions3', 4:'transactions4', 5:'transactions5', 6:'test'}[x]

n = setInput()
support_val = float(setSupport())
confidence_val = float(setConfidence())
select_db = db(int(n))

mycursor.execute("select count(ID) from "+select_db)
rows = int(mycursor.fetchall()[0][0])

mycursor.execute("SHOW columns FROM "+select_db)
columns = mycursor.fetchall()
all_support = {}

every_support, columns_name, count = Apriori(columns, select_db, rows)
print("1. Support_Val\n", every_support)
if not every_support:
	sys.exit("1 end ----------Your support value is too high so no output from the first for loop------------------")
else:
	print("1 end ---------------------------------------------------\n")

for _ in range(9):
	every_support, count = Apriori1(every_support, columns_name, count, select_db, rows)
	confidence_element = Confidence(every_support, all_support, count)
	print(str(count+1)+". Support_Val\n", every_support)
	print(str(count+1)+". Confidence_Val\n", confidence_element)
	if not every_support:
		info = (str(count+1)+". end ----------There is no output from the "+str(count+1)+" for loop------------------")
		sys.exit(info)
	else:
		print(str(count+1)+". end ---------------------------------------------------\n")
