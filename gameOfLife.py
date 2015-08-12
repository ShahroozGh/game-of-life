import tkinter as tk

class game:
	def __init__(self):
		self.root = tk.Tk()

		self.frame = tk.Frame(bg="white")
		self.frame.pack()

		self.canvas = tk.Canvas(self.frame, bg="black", width = 800, height = 800)
		self.canvas.pack()

		self.startB = tk.Button(self.frame, bg="grey", fg="white", text="Start", command=self.start)
		self.startB.pack()

		self.root.mainloop()

	def start(self):
		print("start")

	def paint(self):

class cell:
	def __inti__(self, live = True, x = 0, y = 0):
		self.life = life
		self.x = x
		self.y = y



app = game()
