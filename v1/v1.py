import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageOps
from tkinter.filedialog import askopenfilename, asksaveasfilename

#視窗化的class
class window :
	#視窗初始化
	def __init__(self) :
		#一些變數
		self.method = ["Linearly", "Exponentially", "Logarithmically"]
		self.index = 0	#紀錄method的index
		self.chgMethod = False	#紀錄是否有換method
		self.filename = None
		
		#視窗基本資訊
		self.win = tk.Tk()
		self.win.title("dip hw1")
		self.win.resizable(False, False)		#不可調整視窗長寬
		self.win.geometry("810x600+200+200")	#視窗大小
		self.arr = np.zeros(shape=(1,1))
		self.tmparr = np.copy(self.arr)
		
		#視窗button, label等
		self.win.open = tk.Button(self.win, text="open", width=10, height=2, command=self.clickOpen)
		self.win.save = tk.Button(self.win, text="save", width=10, height=2, command=self.clickSave)
		self.imgL = tk.Label(self.win, width=300, height=300)
		self.chgL = tk.Label(self.win, width=300, height=300)
		self.mth = tk.Button(self.win, text=self.method[self.index], command=self.clickMth, width=12, height=2)
		self.a = tk.Label(self.win, text="a")
		self.b = tk.Label(self.win, text="b")
		self.sa = tk.Scale(self.win, from_=-1, to=3, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=1, resolution=0.1, command=self.val_a)
		self.sb = tk.Scale(self.win, from_=-100, to=100, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=20, resolution=0.1, command=self.val_b)
		self.sa.set(1)
		self.z = tk.Label(self.win, text="zoom")
		self.sz = tk.Scale(self.win, from_=0.5, to=1.5, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=0.1, resolution=0.01, command=self.zoom)
		self.sz.set(1)
		self.his = tk.Button(self.win, text="histogram", command=self.clickHis, width=10, height=2)
		
		#pack / place
		self.win.open.pack(side="top", anchor="nw", padx=20, pady=20)
		self.win.save.pack(side="top", anchor="nw", padx=20, pady=0)
		self.imgL.place(x=150, y=20)
		self.chgL.place(x=480, y=20)
		self.mth.place(x=12, y=390)
		self.a.place(x=150, y=365)
		self.b.place(x=150, y=444)
		self.sa.place(x=171, y=342)
		self.sb.place(x=171, y=421)
		self.z.place(x=50, y=523)
		self.sz.place(x=171, y=500)
		self.his.pack(side="top", anchor="nw", padx=20, pady=20)
		
	#開檔	
	def clickOpen(self) :
		#取得開啟資訊
		self.filename = askopenfilename(filetypes=(("jpg files","*.jpg"),("tif files", "*.tif"),("all files","*.*")))

		#開檔成功
		if (self.filename) :
			#Label 顯示圖片
			self.imgO = Image.open(self.filename).convert('L').resize((300, 300), Image.BILINEAR)
			self.chgO = Image.open(self.filename).convert('L').resize((300, 300), Image.BILINEAR)
			self.img = ImageTk.PhotoImage(self.imgO)
			self.chg = ImageTk.PhotoImage(self.chgO)
			self.imgL.configure(image=self.img)
			self.imgL.image = self.img
			self.chgL.configure(image=self.chg)
			self.chgL.image = self.chg
			
			#將圖片轉成array
			self.arr = np.array(self.imgO)
			self.tmparr = np.copy(self.arr)
						
		#開檔失敗
		else :
			print("file open failed")
			
	#存檔
	def clickSave(self) :
		#如果已開檔
		if (self.filename) :
			#取得存取資訊
			self.savename = asksaveasfilename(filetypes=(("jpg files","*.jpg"),("tif files", "*.tif"),("all files","*.*")))
			
			#取得成功
			if (self.savename) :
				#大小不變
				if (float(self.sz.get()) == 1) :
					tmp = Image.fromarray(self.arr)
				#縮小
				elif (float(self.sz.get()) < 1) :
					tmp = Image.fromarray(self.arr).resize((int(300*float(self.sz.get())), int(300*float(self.sz.get()))), Image.BILINEAR)
				#放大
				else :
					tmp = Image.fromarray(self.arr).resize((int(300*float(self.sz.get())),int(300*float(self.sz.get()))), Image.BILINEAR)
					tmp = tmp.crop((0, 0, 300, 300))
				tmp = tmp.convert('RGB')
				tmp.save(self.savename)
				return
		#失敗
		print("file save failed")
			
	#根據方法更改slider
	def clickMth(self) :
		self.index = (self.index+1) % 3
		self.mth["text"] = self.method[self.index]
		self.chgMethod = True
		
		#Linearly
		if (self.index == 0) :
			self.sa = tk.Scale(self.win, from_=-1, to=3, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=1, resolution=0.1, command=self.val_a)
			self.sb =tk.Scale(self.win, from_=-100, to=100, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=20, resolution=0.1, command=self.val_b)
			self.sa.set(1)
			
		#Exponentially
		elif (self.index == 1) :
			self.sa = tk.Scale(self.win, from_=0.009, to=0.01, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=0.0001, resolution=0.0001, command=self.val_a)
			self.sb = tk.Scale(self.win, from_=-1, to=1, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=0.2, resolution=0.1, command=self.val_b)
			self.sa.set(0.0095)
			
		#Logarithmically
		elif (self.index == 2) :
			self.sa = tk.Scale(self.win, from_=-3, to=5, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=1, resolution=0.1, command=self.val_a)
			self.sb =tk.Scale(self.win, from_=-100, to=100, orient=tk.HORIZONTAL, length=610, showvalue=1, tickinterval=20, resolution=0.1, command=self.val_b)
			self.sa.set(1)
			
		self.sa.place(x=171, y=342)
		self.sb.place(x=171, y=421)
	
	#A的slider
	def val_a(self, val) :
		#如果已開檔
		if (self.filename) :
			#如果有換方法
			if (self.chgMethod) :
				self.tmparr = np.copy(self.arr)
				self.chgMethod = False
			
			#Linearly : y = ax + b
			if (self.index == 0) :
				self.arr = self.tmparr * float(val) + float(self.sb.get())
				
			#Exponentially : y = exp(ax + b)
			elif (self.index == 1) :
				self.arr = np.exp(self.tmparr * float(val) + float(self.sb.get()))
				
			#Logarithmically : y = a * log(1 + x) + b
			elif (self.index == 2) :
				self.arr = float(val) * (np.log(np.absolute(self.tmparr) + 1) + float(self.sb.get()))
				
			#更新圖片
			tmp = Image.fromarray(self.arr).resize((int(300*float(self.sz.get())), int(300*float(self.sz.get()))), Image.BILINEAR)
			tmpp= ImageTk.PhotoImage(tmp)
			self.chgL.configure(image=tmpp)
			self.chgL.image = tmpp
	
	#B的slider
	def val_b(self, val) :
		#如果已開檔
		if (self.filename) :
			#如果有換方法
			if (self.chgMethod) :
				self.tmparr = np.copy(self.arr)
				self.chgMethod = False

			#Linearly : y = ax + b
			if (self.index == 0) :
				self.arr = self.tmparr * float(self.sa.get()) + float(val)
				
			#Exponentially : y = exp(ax + b)
			elif (self.index == 1) :
				self.arr = np.exp(self.tmparr * float(self.sa.get()) + float(val))
				
			#Logarithmically : y = a * log(1 + x) + b
			elif (self.index == 2) :
				self.arr = float(self.sa.get()) * np.log(np.absolute(self.tmparr) + 1) + float(val)
				
			#更新圖片
			tmp = Image.fromarray(self.arr).resize((int(300*float(self.sz.get())), int(300*float(self.sz.get()))), Image.BILINEAR)
			tmpp= ImageTk.PhotoImage(tmp)
			self.chgL.configure(image=tmpp)
			self.chgL.image = tmpp
	
	#zoom
	def zoom(self, val) :
		if (self.filename) :
			tmp = Image.fromarray(self.arr).resize((int(300*float(val)), int(300*float(val))), Image.BILINEAR)
			tmpp = ImageTk.PhotoImage(tmp)
			self.chgL.configure(image=tmpp)
			self.chgL.image = tmpp
	
	#histogram
	def clickHis(self) :
		tmp = Image.fromarray(self.arr).resize((int(300*float(self.sz.get())),int(300*float(self.sz.get()))), Image.BILINEAR)
		tmp = tmp.convert('RGB')
		tmp = ImageOps.equalize(tmp)
		self.chgMethod = True
		
		#更新圖片
		tmpp = ImageTk.PhotoImage(tmp)
		self.chgL.configure(image=tmpp)
		self.chgL.Image = tmpp
		self.arr = np.array(tmp.convert('F'))


#主程式	
myWindow = window()
myWindow.win.mainloop()
