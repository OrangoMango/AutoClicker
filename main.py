from tkinter import *
from tkinter import ttk, messagebox
import pyautogui as pa
import time, threading
from pynput import keyboard

class AutoClicker:
	def __init__(self, h, m, s, ms, pos):
		self.time = ms+s*1000+m*60000+h*60*60*1000
		self.started = True
		self.button = "left"
		self.position = pos
	def start(self):
		while self.started:
			if self.position != None:
				pa.click(button=self.button, x=self.position[0], y=self.position[1])
			else:
				pa.click(button=self.button)
			time.sleep(self.time/1000)
	def stop(self):
		self.started = False

class Window:
	def __init__(self):
		self.tk = Tk()
		self.tk.title("AutoClicker v1.0")
		self.startKey = "c"
		self.started = False
	def draw_gui(self):
		self.interval = LabelFrame(self.tk, text="Click interval")
		self.interval.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky="ew")
		self.h = ttk.Spinbox(self.interval, from_=0, to=24, width=2, state="readonly")
		self.h.set(0)
		self.h.pack(side="left", pady=5, padx=5)
		hL = Label(self.interval, text="hours,")
		hL.pack(side="left")
		self.m = ttk.Spinbox(self.interval, from_=0, to=59, width=2, state="readonly")
		self.m.set(0)
		self.m.pack(side="left")
		mL = Label(self.interval, text="minutes,")
		mL.pack(side="left")
		self.s = ttk.Spinbox(self.interval, from_=0, to=59, width=2, state="readonly")
		self.s.set(0)
		self.s.pack(side="left")
		sL = Label(self.interval, text="seconds,")
		sL.pack(side="left")
		self.ms = ttk.Spinbox(self.interval, from_=0, to=999, width=2, state="readonly")
		self.ms.set(0)
		self.ms.pack(side="left")
		mmL = Label(self.interval, text="milliseconds")
		mmL.pack(side="left")
		
		def check_bind_start():
			def key_pressed(k):
				try:
					self.started = True
					self.startKey = k.char
					self.started = False
					return False
				except ValueError:
					pass
			with keyboard.Listener(on_press=key_pressed) as listener:
				listener.join()
			self.startBindL["text"] = "Start/Stop key: [%s]: " % self.startKey
		
		self.config = LabelFrame(self.tk, text="Key bind")
		self.startBindL = Label(self.config, text="Start/Stop key [%s]: " % self.startKey)
		self.startBindL.pack(side="left", padx=3, pady=5)
		startBindB = Button(self.config, text="Click to bind", command=check_bind_start)
		startBindB.pack(side="left", padx=3, pady=5)
		self.config.grid(row=1, column=0, padx=5, sticky="e")
		
		self.mouseSetting = LabelFrame(self.tk, text="Mouse setting")
		mouseButtonL = Label(self.mouseSetting, text="Mouse button: ")
		mouseButtonL.pack(padx=3, pady=3)
		self.buttonSelect = ttk.Combobox(self.mouseSetting, values=["left", "right"], state="readonly")
		self.buttonSelect.set("left")
		self.buttonSelect.pack(padx=3, pady=3)
		frame = Frame(self.mouseSetting)
		x = Label(frame, text="X:", state="disabled")
		y = Label(frame, text="Y:", state="disabled")
		self.xNum = Entry(frame, width=4, state="disabled")
		self.yNum = Entry(frame, width=4, state="disabled")
		def onclick():
			x["state"] = "normal" if self.var.get() else "disabled"
			y["state"] = "normal" if self.var.get() else "disabled"
			self.xNum["state"] = "normal" if self.var.get() else "disabled"
			self.yNum["state"] = "normal" if self.var.get() else "disabled"
		self.var = BooleanVar()
		coordsBox = Checkbutton(frame, variable=self.var, text="Specific coords", command=onclick)
		x.grid(row=1, column=0)
		y.grid(row=2, column=0)
		self.xNum.grid(row=1, column=1)
		self.yNum.grid(row=2, column=1)
		coordsBox.grid(row=0, column=0, columnspan=2)
		frame.pack(padx=3, pady=3)
		self.mouseSetting.grid(row=1, column=1, padx=5, sticky="w")
		
		self.startB = Button(self.tk, text="Start", command=self.start)
		self.startB.grid(row=2, column=0)
		self.stopB = Button(self.tk, text="Stop", command=self.stop, state="disabled")
		self.stopB.grid(row=2, column=1, pady=10);
		
		Label(self.tk, text="OrangoMango - https://orangomango.github.io").grid(row=3, column=0, pady=2, columnspan=2)
		
		def handleStartClick():
			def key_pressed(k):
				try:
					if k.char == self.startKey.lower():
						if self.started:
							self.stop()
						else:
							self.start()
				except AttributeError:
					pass
			with keyboard.Listener(on_press=key_pressed) as listener:
				listener.join()
		
		clickThread = threading.Thread(target=handleStartClick)
		clickThread.start()
	def start(self):
		self.started = True;
		hours = int(self.h.get())
		minutes = int(self.m.get())
		seconds = int(self.s.get())
		milliseconds = int(self.ms.get())
		if self.var.get():
			try:
				xC = int(self.xNum.get())
				yC = int(self.yNum.get())
				pos = (xC, yC)
			except ValueError:
				messagebox.showerror("Error", "Please check your values!")
				return
		else:
			pos = None
		self.startB.configure(state="disabled")
		self.stopB.configure(state="normal");
		self.autoclicker = AutoClicker(hours, minutes, seconds, milliseconds, pos)
		self.autoclicker.button = self.buttonSelect.get()
		startT = threading.Thread(target=self.autoclicker.start)
		startT.start()
	def stop(self):
		self.started = False
		self.autoclicker.stop()
		self.startB.configure(state="normal")
		self.stopB.configure(state="disabled");
	def mainloop(self):
		self.tk.mainloop()

if __name__ == "__main__":
	window = Window()
	window.draw_gui();
	window.mainloop()
