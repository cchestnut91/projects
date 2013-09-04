import math

def main():
	#prompt user for puzzle
	print "Please enter a 4x4 sudoku, using 0 for empty spaces"
	#collect the puzzle
	values = raw_input()
	#values = "7 2 9 0 5 0 0 0 4 0 8 0 7 9 0 0 2 0 0 0 1 0 2 0 7 9 0 0 0 2 0 0 5 0 0 0 8 0 7 0 0 2 4 3 5 0 4 5 0 0 8 9 0 2 2 0 4 5 0 0 6 0 0 0 0 0 0 0 0 2 0 9 0 0 8 0 0 1 0 0 0"
	values = values.split()
	for i in range(len(values)):
		values[i] = int(values[i])
	puzzle = Sudoku(values)
	puzzle.show()
	solve(puzzle)

def solve(puzzle):
	puzzle.solveSimple()
	#solve the toughies
	puzzle.possible()
	puzzle.show()
	puzzle.tough()
	puzzle.unsol()
	if puzzle.com == True:
		puzzle.show()
	else:
		solve(puzzle)
    
class Sudoku:
	def __init__(self,values):
		if len(values) == 16:
			self.size = 4
		elif len(values) == 81:
			self.size = 9
		self.squares = []
		self.boxes = []
		self.cols = []
		self.rows = []
		for i in range(len(values)):
			self.squares.append(Square(i,values[i],self.size))
		for i in range(self.size):
			self.boxes.append(Box(i,self.squares,self.size))
			self.cols.append(Col(i,self.squares,self.size))
			self.rows.append(Row(i,self.squares,self.size))
		self.unsol()

	def unsol(self):
		self.com = True
		for i in range(self.size*self.size):
			if self.squares[i].value == 0:
				self.com = False

	def show(self):
		print ""
		if self.size == 4:
	        	for i in range(self.size):
    	    			for j in range(self.size):
					print self.squares[self.size*i+j].value,
				print ""
		elif self.size == 9:
			for i in range(self.size):
				if i == 3 or i == 6:
					print ""
				for j in range(self.size):
					if j == 3 or j == 6:
						print " ",
					print self.squares[self.size*i+j].value,
				print ""
    		print ""
		count = 0
		for i in range(len(self.squares)):
			if self.squares[i].value == 0:
				count += 1
				print count,": i: ",i,self.squares[i].possible

	def solveSimple(self):
		again = False
		count = 0
		for i in range(self.size):
			if self.boxes[i].count == 1:
				count += 1
				again = True
				self.solveSingle(self.boxes[i])
				self.boxes[i] = Box(i,self.squares,self.size)
		if count > 0:
			self.recount()
			self.show()
		count = 0
		for i in range(self.size):
			if self.rows[i].count == 1:
				count += 1
				again = True
				self.solveSingle(self.rows[i])
				self.rows[i] = Row(i,self.squares,self.size)
		if count > 0:
			self.recount()
			self.show()
		count = 0
		for i in range(self.size):
			if self.cols[i].count == 1:
				count += 1
				again = True
				self.solveSingle(self.cols[i])
				self.cols[i] = Col(i,self.squares,self.size)
		if count > 0:
			self.recount()
			self.show()
		if again == True:
			self.solveSimple()

	def solveSingle(self,unit):
		if self.size == 4:
			sum = 10
		elif self.size == 9:
			sum = 45
		for i in range(self.size):
			sum -= self.squares[unit.values[i]].value
		for i in range(self.size):
			if sum == self.squares[unit.values[i]].value:
				print "ERROR"
		for i in range(self.size):
			if self.squares[unit.values[i]].value == 0:
				self.squares[unit.values[i]].value = sum

	def possible(self):
		again = False
		count = 0
		count1 = 0
		for i in range(len(self.squares)):
			if self.squares[i].value == 0:
				count += 1
				for j in range(len(self.squares[i].rel)):
					if self.squares[self.squares[i].rel[j]].value != 0:
						if self.squares[i].possible.count(self.squares[self.squares[i].rel[j]].value) != 0:
							self.squares[i].possible.remove(self.squares[self.squares[i].rel[j]].value)
				if len(self.squares[i].possible) == 1:
					self.squares[i].value = self.squares[i].possible[0]
				elif len(self.squares[i].possible) == 0:
					print "PROBLEM"
					l = raw_input("Press any key to continue")
				self.show()
		for i in range(len(self.squares)):
			if self.squares[i].value == 0:
				count1 += 1
				again = True
		if again == True and count != count1:
			self.possible()
	
	def recount(self):
		for i in range(self.size):
			self.boxes[i].recount(self.squares)
			self.rows[i].recount(self.squares)
			self.cols[i].recount(self.squares)
			#also recheck self.com

	def tough(self):
		#repeat for numbers 1-9
		for i in range(self.size):
			#Look at each box
			for j in range(self.size):
				box = self.boxes[j]
				#look at each 0 in the box
				for x in range(self.size):
					if self.squares[box.values[x]].value == 0:
						#if i is in it's list of possibles
						if self.squares[box.values[x]].possible.count(i) != 0:
							count = self.checkRelForI(box.values,i,box.values[x])
							if count == 0:
								#first zero with i is i
								self.squares[box.values[x]].value == i
							else:
								#look at the zero's row
								count = self.checkRelForI(self.squares[box.values[x]].row,i,box.values[x])
								if count == 0:
									#first zero is i
									self.squares[box.values[x]].value = i
								else:
									#look at the zero's col
									#repeat process
									count = self.checkRelForI(self.squares[box.values[x]].col,i,box.values[x])
									if count == 0:
										#first zero is i
										self.squares[box.values[x]].value = i

	def checkRelForI(self,unit,i,x):
		count = 0
		for a in range(len(unit)):
			if self.squares[unit[a]].value == 0 and self.squares[unit[a]].pos != self.squares[x].pos:
				if self.squares[unit[a]].possible.count(i) != 0:
					count += 1
		return count		

class Square:
    def __init__(self,pos,value,size):
	if size == 4:
		self.value = value
		self.pos = pos
        	if self.value == 0:
        	    self.com = False
        	else:
        	    self.com = True
        	self.possible = [1,2,3,4]
		if self.pos == 0 or self.pos == 1 or self.pos == 4 or self.pos == 5:
			self.box = [0,1,4,5]
		elif self.pos == 2 or self.pos == 3 or self.pos == 6 or self.pos == 7:
			self.box = [2,3,6,7]
		elif self.pos == 8 or self.pos == 9 or self.pos == 12 or self.pos == 13:
			self.box = [8,9,12,13]
		elif self.pos == 10 or self.pos == 11 or self.pos == 14 or self.pos == 15:
			self.box = [10,11,14,15]
		row = math.floor(self.pos / 4)
		row = int(row)
		if row == 0:
			self.row = [0,1,2,3]
		elif row == 1:
			self.row = [4,5,6,7]
		elif row == 2:
			self.row = [8,9,10,11]
		elif row == 3:
			self.row = [12,13,14,15]
		col = self.pos % 4
		if col == 0:
			self.col = [0,4,8,12]
		elif col == 1:
			self.col = [1,5,9,13]
		elif col == 2:
			self.col = [2,6,10,14]
		elif col == 3:
			self.col = [3,7,11,15]
	elif size == 9:
		self.value = value
		self.pos = pos
        	if self.value == 0:
        	    self.com = False
        	else:
        	    self.com = True
        	self.possible = [1,2,3,4,5,6,7,8,9]
		if self.pos == 0 or self.pos == 1 or self.pos == 2 or self.pos == 9 or self.pos == 10 or self.pos == 11 or self.pos == 18 or self.pos == 19 or self.pos == 20:
			self.box = [0,1,2,9,10,11,18,19,20]
		elif self.pos == 3 or self.pos == 4 or self.pos == 5 or self.pos == 12 or self.pos == 13 or self.pos == 14 or self.pos == 21 or self.pos == 22 or self.pos == 23:
			self.box = [3,4,5,12,13,14,21,22,23]
		elif self.pos == 6 or self.pos == 7 or self.pos == 8 or self.pos == 15 or self.pos == 16 or self.pos == 17 or self.pos == 24 or self.pos == 25 or self.pos == 26:
			self.box = [6,7,8,15,16,17,24,25,26]
		elif self.pos == 27 or self.pos == 28 or self.pos == 29 or self.pos == 36 or self.pos == 37 or self.pos == 38 or self.pos == 45 or self.pos == 46 or self.pos == 47:
			self.box = [27,28,29,36,37,38,45,46,47]
		elif self.pos == 30 or self.pos == 31 or self.pos == 32 or self.pos == 39 or self.pos == 40 or self.pos == 41 or self.pos == 48 or self.pos == 49 or self.pos == 50:
			self.box = [30,31,32,39,40,41,48,49,50]
		elif self.pos == 33 or self.pos == 34 or self.pos == 35 or self.pos == 42 or self.pos == 43 or self.pos == 44 or self.pos == 51 or self.pos == 52 or self.pos == 53:
			self.box = [33,34,35,42,43,44,51,52,53]
		elif self.pos == 54 or self.pos == 55 or self.pos == 56 or self.pos == 63 or self.pos == 64 or self.pos == 65 or self.pos == 72 or self.pos == 73 or self.pos == 74:
			self.box = [54,55,56,63,64,65,72,73,74]
		elif self.pos == 57 or self.pos == 58 or self.pos == 59 or self.pos == 66 or self.pos == 67 or self.pos == 68 or self.pos == 75 or self.pos == 76 or self.pos == 77:
			self.box = [57,58,59,66,67,68,75,76,77]
		elif self.pos == 60 or self.pos == 61 or self.pos == 62 or self.pos == 69 or self.pos == 70 or self.pos == 71 or self.pos == 78 or self.pos == 79 or self.pos == 80:
			self.box = [60,61,62,69,70,71,78,79,80]
		row = math.floor(self.pos / 9)
		row = int(row)
		if row == 0:
			self.row = [0,1,2,3,4,5,6,7,8]
		elif row == 1:
			self.row = [9,10,11,12,13,14,15,16,17]
		elif row == 2:
			self.row = [18,19,20,21,22,23,24,25,26]
		elif row == 3:
			self.row = [27,28,29,30,31,32,33,34,35]
		elif row == 4:
			self.row = [36,37,38,39,40,41,42,43,44]
		elif row == 5:
			self.row = [45,46,47,48,49,50,51,52,53]
		elif row == 6:
			self.row = [54,55,56,57,58,59,60,61,62]
		elif row == 7:
			self.row = [63,64,65,66,67,68,69,70,71]
		elif row == 8:
			self.row = [72,73,74,75,76,77,78,79,80]
		col = self.pos % 9
		if col == 0:
			self.col = [0,9,18,27,36,45,54,63,72]
		elif col == 1:
			self.col = [1,10,19,28,37,46,55,64,73]
		elif col == 2:
			self.col = [2,11,20,29,38,47,56,65,74]
		elif col == 3:
			self.col = [3,12,21,30,39,48,57,66,75]
		elif col == 4:
			self.col = [4,13,22,31,40,49,58,67,76]
		elif col == 5:
			self.col = [5,14,23,32,41,50,59,68,77]
		elif col == 6:
			self.col = [6,15,24,33,42,51,60,69,78]
		elif col == 7:
			self.col = [7,16,25,34,43,52,61,70,79]
		elif col == 8:
			self.col = [8,17,26,35,44,53,62,71,80]
	self.rel = []
	for i in range(size):
		if self.row[i] != self.pos and self.rel.count(self.row[i]) == 0:
			self.rel.append(self.row[i])
		if self.col[i] != self.pos and self.rel.count(self.col[i]) == 0:
			self.rel.append(self.col[i])
		if self.box[i] != self.pos and self.rel.count(self.box[i]) == 0:
			self.rel.append(self.box[i])

class Box:
    def __init__(self,num,squares,size):
	if size == 4:
		if num == 0:
			self.values = [0,1,4,5]
		elif num == 1:
			self.values = [2,3,6,7]
		elif num == 2:
    	        	self.values = [8,9,12,13]
		elif num == 3:
			self.values = [10,11,14,15]
        	sum = 0
        	for i in range(len(self.values)):
        	    sum += squares[self.values[i]].value
        	self.sum = sum
        	if sum == 10:
        	    self.com = True
        	else:
        	    self.com = False
        elif size == 9:
		if num == 0:
			self.values = [0,1,2,9,10,11,18,19,20]
	        elif num == 1:
			self.values = [3,4,5,12,13,14,21,22,23]
    	    	elif num == 2:
    	        	self.values = [6,7,8,15,16,17,24,25,26]
        	elif num == 3:
        	    self.values = [27,28,29,36,37,38,45,46,47]
		elif num == 4:
			self.values = [30,31,32,39,40,41,48,49,50]
		elif num == 5:
			self.values = [33,34,35,42,43,44,51,52,53]
		elif num == 6:
			self.values = [54,55,56,63,64,65,72,73,74]
		elif num == 7:
			self.values = [57,58,59,66,67,68,75,76,77]
		elif num == 8:
			self.values = [60,61,62,69,70,71,78,79,80]
        	sum = 0
        	for i in range(len(self.values)):
			sum += squares[self.values[i]].value
        	self.sum = sum
        	if sum == 45:
			self.com = True
        	else:
			self.com = False
	self.nums = []
	for i in range(size):
		self.nums.append(squares[self.values[i]].value)
	self.count = 0
        for i in range(len(self.values)):
		if squares[self.values[i]].value == 0:
                	self.count += 1

    def recount(self,squares):
		count = 0
		for i in range(len(self.values)):
			if squares[self.values[i]].value == 0:
				count += 1
		self.count = count

class Col:
    def __init__(self,num,squares,size):
        self.values = []
	self.nums = []
        for i in range(size * size):
		if i % size == num:
                	self.values.append(i)
			self.nums.append(squares[i].value)
        sum = 0
       	for i in range(len(self.values)):
		sum += squares[self.values[i]].value
       	self.sum = sum
	if size == 4:
        	if sum == 10:
			self.com = True
        	else:
			self.com = False
	elif size == 9:
		if sum == 45:
			self.com = True
		else:
			self.com = False
        count = 0
        for i in range(len(self.values)):
            if squares[self.values[i]].value == 0:
                count += 1
        self.count = count

    def recount(self,squares):
	count = 0
	for i in range(len(self.values)):
		if squares[self.values[i]].value == 0:
			count += 1
	self.count = count

class Row:
    def __init__(self,num,squares,size):
        self.values = []
	self.nums = []
	for i in range(size):
		self.values.append(size*num+i)
		self.nums.append(squares[size*num+i].value)
        sum = 0
        for i in range(len(self.values)):
            sum += squares[self.values[i]].value
        self.sum = sum
	if size == 4:
		if sum == 10:
			self.com = True
		else:
			self.com = False
	elif size == 9:
		if sum == 45:
			self.com = True
		else:
			self.com = False
        count = 0
        for i in range(len(self.values)):
            if squares[self.values[i]].value == 0:
                count += 1
        self.count = count

    def recount(self,squares):
	count = 0
	for i in range(len(self.values)):
		if squares[self.values[i]].value == 0:
			count += 1
	self.count = count

main()