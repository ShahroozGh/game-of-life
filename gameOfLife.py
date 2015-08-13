import tkinter as tk

class game:
	def __init__(self):
		self.root = tk.Tk()

		self.PAUSED = False

		self.frame = tk.Frame(bg="white")
		self.frame.pack()

		self.canvas = tk.Canvas(self.frame, bg="black", width = 700, height = 700)
		self.canvas.pack()

		self.startB = tk.Button(self.frame, bg="grey", fg="white", text="Start", command=self.start)
		self.startB.pack()

		self.root.mainloop()

	def start(self):
		print("start")
		self.cellList = [[Cell(False,x,y) for y in range(70)] for x in range(70)]

		self.cellList[4][1].live = True
		self.cellList[0][0].live = True

		self.cellList[20][20].live = True
		self.cellList[20][21].live = True
		self.cellList[20][22].live = True

		self.canvas.bind("<Button-1>", self.canvasClicked)
		

		self.gameLoop(self.cellList)

	def gameLoop(self, cellList):
		self.checkLivingConditions(cellList)
		self.paint(cellList)
		self.root.after(10000, self.gameLoop, cellList)

	def paint(self,cellList):
		self.canvas.delete(tk.ALL)
		
		for x in range(70):
			for y in range(70):
				if cellList[x][y].live is True:
					self.canvas.create_rectangle(x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill = "red")

	def canvasClicked(self,event): 
		print("CLick: " + str(event.x) + ", " + str(event.y))
		xTile = (event.x - (event.x % 10)) / 10
		yTile = (event.y - (event.y % 10)) / 10

		self.addOrKillCell(True,int(xTile), int(yTile),self.cellList)
		self.paint(self.cellList)

	def addOrKillCell(self,live,x,y , cellList):
		cellList[x][y].live = live

	def checkLivingConditions(self, cellList):
		for x in range(70):
			for y in range(70):
				liveNeighbours = self.checkNeighbours(x,y,cellList) ##Problem here hebause of order, dont kill or spawn until complete check is over, just flag
				if cellList[x][y].live is True:
					
					if liveNeighbours < 2:
						#Kill Cell
						self.addOrKillCell(False,x,y,cellList) #Dont do this yet, just flag
					elif liveNeighbours > 3:
						#Kill Cell
						self.addOrKillCell(False,x,y,cellList)
					else:
						#Keep Cell 
						self.addOrKillCell(True,x,y,cellList)


				elif cellList[x][y].live is False:

					if liveNeighbours == 3:
						#Live Cell
						self.addOrKillCell(True,x,y,cellList)


	def checkNeighbours(self,x,y,cellList):
		liveNeighbours = 0

		if x+1 < 70 and y+1 < 70:
			if cellList[x+1][y+1].live == True:
				liveNeighbours += 1
		if x-1 > -1 and y-1 > -1: 
			if cellList[x-1][y-1].live == True:
				liveNeighbours += 1
		if x+1 < 70 and y-1 > -1: 
			if cellList[x+1][y-1].live == True:
				liveNeighbours += 1
		if x-1 > -1 and y+1 < 70: 
			if cellList[x-1][y+1].live == True:
				liveNeighbours += 1
		if y+1 < 70: 
			if cellList[x][y+1].live == True:
				liveNeighbours += 1
		if y-1 > -1: 
			if cellList[x][y-1].live == True:
				liveNeighbours += 1
		if x+1 < 70: 
			if cellList[x+1][y].live == True:
				liveNeighbours += 1
		if x-1 > -1: 
			if cellList[x-1][y].live == True:
				liveNeighbours += 1

		return liveNeighbours




class Cell:
	def __init__(self, live = True, x = 0, y = 0):
		self.live = live
		self.x = x
		self.y = y



app = game()
