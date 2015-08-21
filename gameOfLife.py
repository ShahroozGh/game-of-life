import tkinter as tk

class game:
	def __init__(self):
		self.root = tk.Tk()

		self.RUNNING = False
		self.PAUSED = False

		self.SHOW_GRID = tk.BooleanVar()

		self.generationDuration = 100
		self.generation = 0

		self.frame = tk.Frame(bg="white")
		self.frame.pack()

		self.canvas = tk.Canvas(self.frame, bg="black", width = 700, height = 700)
		self.canvas.pack()

		self.startB = tk.Button(self.frame, bg="grey", fg="white", text="Start", command=self.start)
		self.startB.pack(side = tk.LEFT)

		self.pauseB = tk.Button(self.frame, bg="grey", fg="white", text = "Pause", command = self.pause)
		self.pauseB.pack(side = tk.LEFT)

		self.genDurS = tk.Spinbox(self.frame, from_ = 1, to = 1000, repeatdelay = 10, repeatinterval = 10, command = self.genLengthChanged)
		self.genDurS.pack(side = tk.LEFT)

		self.gridCB = tk.Checkbutton(self.frame, text = "Show Grid", variable = self.SHOW_GRID, onvalue = True, offvalue = False, command = self.gridCheckClicked)
		self.gridCB.pack(side = tk.LEFT)

		self.generationL = tk.Label(self.frame, text = "0", font = ("Helvetica", 16))
		self.generationL.pack(side = tk.LEFT)

		#Bind button listners to respond to clicks on canvas
		self.canvas.bind("<Button-1>", self.canvasClicked)
		self.canvas.bind("<B1-Motion>", self.canvasClicked)

		self.root.mainloop()

		#Function called when start button is clicked, will start or reset
	def start(self):
		
		if self.RUNNING is False:

			print("start")
			self.RUNNING = True
			self.PAUSED = False

			#Initalize 2d list with dead cells
			self.cellList = [[Cell(False,x,y) for y in range(70)] for x in range(70)]

			self.cellList[4][1].live = True
			self.cellList[0][0].live = True

			self.cellList[20][20].live = True
			self.cellList[20][21].live = True
			self.cellList[20][22].live = True
			
			#Get generation duration from spinbox (in ms)
			self.generationDuration = int(self.genDurS.get())

			#Change button text
			self.startB.config(text = "Reset")

			#Start game loop
			self.gameLoop(self.cellList)

		else:

			print("Reset")
			self.RUNNING = False
			self.PAUSED = False

			#cancel queued after loop call (Stop gameLoop)
			self.root.after_cancel(self.job)

			#Initalize 2d list with dead cells
			self.cellList = [[Cell(False,x,y) for y in range(70)] for x in range(70)]

			#Paint empty board
			self.paint(self.cellList)

			#Reset generation count
			self.generation = 0

			#Update counter label
			self.generationL.config(text = str(self.generation))

			#Change button text
			self.startB.config(text = "Start")


	def pause(self):

		if self.RUNNING is True:

			print("Pause")

			self.PAUSED = not self.PAUSED

			if self.PAUSED is True:
				self.root.after_cancel(self.job)
			else:
				self.generationDuration = int(self.genDurS.get())
				self.gameLoop(self.cellList)

	def genLengthChanged(self):
		print("speedChanged")
		#self.root.after_cancel(self.job)
		self.generationDuration = int(self.genDurS.get())
		#self.gameLoop(self.cellList)

	def gridCheckClicked(self):
		print(self.SHOW_GRID.get())




	def gameLoop(self, cellList):
		self.generation += 1
		self.generationL.config(text = str(self.generation))
		self.checkLivingConditions(cellList)
		self.nextGeneration(cellList)
		self.paint(cellList)
		self.job = self.root.after(self.generationDuration, self.gameLoop, cellList)

	def paint(self,cellList):
		self.canvas.delete(tk.ALL)
		
		for x in range(70):
			for y in range(70):
				if cellList[x][y].live is True:
					self.canvas.create_rectangle(x * 10, y * 10, x * 10 + 10, y * 10 + 10, fill = "red")
		
		if self.SHOW_GRID.get() == 1:
			#Paint gridlines
			for x in range(70):
				self.canvas.create_line(x*10,0,x*10,700, width = 1, fill = "grey")
			for y in range(70):
				self.canvas.create_line(0,y*10,700,y*10, width = 1, fill = "grey")
		

	#canvas clicked with left mouse btn event
	def canvasClicked(self,event): 
		print("CLick: " + str(event.x) + ", " + str(event.y))
		xTile = (event.x - (event.x % 10)) / 10
		yTile = (event.y - (event.y % 10)) / 10

		#bring cell to life where canvas is clicked
		self.addOrKillCell(True,int(xTile), int(yTile),self.cellList)
		self.paint(self.cellList)

	#Function to add or kill cell
	def addOrKillCell(self,live,x,y , cellList):
		cellList[x][y].live = live

	#Iterates through all tiles and determines which should live or die 
	def checkLivingConditions(self, cellList):
		for x in range(70):
			for y in range(70):
				liveNeighbours = self.checkNeighbours(x,y,cellList) ##Problem here hebause of order, dont kill or spawn until complete check is over, just flag
				if cellList[x][y].live is True:
					
					if liveNeighbours < 2:
						#Kill Cell
						#self.addOrKillCell(False,x,y,cellList) #Dont do this yet, just flag
						cellList[x][y].flaggedForKill = True
					elif liveNeighbours > 3:
						#Kill Cell
						#self.addOrKillCell(False,x,y,cellList)
						cellList[x][y].flaggedForKill = True
					else:
						#Keep Cell 
						#self.addOrKillCell(True,x,y,cellList)
						cellList[x][y].flaggedForKill = False


				elif cellList[x][y].live is False:

					if liveNeighbours == 3:
						#Live Cell
						#self.addOrKillCell(True,x,y,cellList)
						cellList[x][y].flaggedForKill = False
					else:
						cellList[x][y].flaggedForKill = True

	#Kill cells flagged to be killed, ressuruect cells not flagged to be killed
	def nextGeneration(self, cellList):
		#gen++
		for x in range(70):
			for y in range(70):
				if cellList[x][y].flaggedForKill is True:
					self.addOrKillCell(False,x,y,cellList)
				elif cellList[x][y].flaggedForKill is False:
					self.addOrKillCell(True,x,y,cellList)

		for x in range(70):
			for y in range(70):
				cellList[x][y].flaggedForKill = False



	#Returns the number of live neighbours surrounding tile at (x,y)
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



#Class to represent one cell
class Cell:
	def __init__(self, live = False, x = 0, y = 0):
		self.live = live
		self.x = x
		self.y = y
		self.flaggedForKill = True



app = game()
