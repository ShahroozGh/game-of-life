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

		self.canvas.bind("<Button-1>", self.canvasClicked)
		

		self.gameLoop(self.cellList)

	def gameLoop(self, cellList):
		self.paint(cellList)
		self.root.after(100, self.gameLoop, cellList)

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

	def addOrKillCell(self,live,x,y , cellList):
		cellList[x][y].live = live




class Cell:
	def __init__(self, live = True, x = 0, y = 0):
		self.live = live
		self.x = x
		self.y = y



app = game()
