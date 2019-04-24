import tkinter as tk
import numpy as np
from PIL import Image, ImageTk, ImageOps, ImageFilter
from tkinter.filedialog import askopenfilename, asksaveasfilename

#開檔
def clickOpen() :
		global filename, arr, cur, bpFirst
		#取得開啟資訊
		filename = askopenfilename(filetypes=(("tif files", "*.tif"),("tiff files", "*.tiff"),("all files","*.*")))

		#開檔成功
		if (filename) :
			#Label 顯示圖片
			imgO = Image.open(filename).resize((300, 300), Image.BILINEAR).convert('L')
			chgO = Image.open(filename).resize((300, 300), Image.BILINEAR).convert('L')
			img = ImageTk.PhotoImage(imgO)
			imgL.configure(image=img)
			imgL.image = img
			arr = np.array(imgO)
			cur = np.array(chgO)
			showImage()
			#初始化變數
			bpFirst = True
			
#存檔
def clickSave() :
		global filename, savename
		#如果已開檔
		if (filename) :
			#取得存取資訊
			savename = asksaveasfilename(filetypes=(("tif files", "*.tif"),("tiff files", "*.tiff"),("all files","*.*")))
			
			#取得成功
			if (savename) : 
				tmp = Image.fromarray(cur).convert('L').save(savename)
				return
		#失敗
		print("file save failed")
		
#show image
def showImage() :
	global chgL
	chgO = Image.fromarray(cur)
	chg = ImageTk.PhotoImage(chgO)
	chgL.configure(image=chg)
	chgL.image = chg
	
#gray level slicing
def GLS() :
	#如果開過檔
	if (filename) :
		global cur, btnIndex
		btnIndex = 1
		reset(btnIndex)			
		size = np.shape(arr)
		a = int(sa.get())
		b = int(sb.get())
		if (a > b) :
			a, b = b, a
		#off
		if (glsIndex == 0) :
			cur = np.copy(arr)
		#mode a : 維持原本
		elif (glsIndex == 1) :
			cur = np.uint8([[255 if arr[i][j] >= a and arr[i][j] <= b else arr[i][j] for j in range(size[1])] for i in range(size[0])])
		#mode b : 變黑
		elif (glsIndex == 2) :
			cur = np.uint8([[255 if arr[i][j] >= a and arr[i][j] <= b else 0 for j in range(size[1])] for i in range(size[0])])
		showImage()

#gray level slicing button
def clickGLS() :
	#如果開過檔
	if (filename) :
		global glsIndex
		glsIndex = (glsIndex+1)%3
		gls["text"]=glsText[glsIndex]	
		GLS()

#scale of gray level slicing	
def val_a(val) :
	GLS()

#scale of gray level slicing
def val_b(val) :
	GLS()
	
#bit plane
def clickBP() :
	#如果開過檔
	if (filename) :
		global bpIndex, bpFirst, bp_arr, cur, btnIndex
		btnIndex = 2
		reset(btnIndex)			
		bpIndex = (bpIndex+1)%9
		bp["text"]=bpText[bpIndex]
		#計算每一個bit plane
		if (bpFirst) : 
			size = np.shape(arr)
			bpFirst = False
			for k in range(8) :
				bp_arr[k] = [[255 if str(bin(arr[i][j])[2:]).zfill(8)[k] == '1' else 0 for j in range(size[1])] for i in range(size[0])]
		if (bpIndex != 0) :
			cur = np.copy(bp_arr[8-bpIndex])
		else :
			cur = np.copy(arr)
		showImage()

#smooth, sharp
def clickS() :
	if (filename) :
		global sText, sIndex, s, btnIndex, ss, cur
		btnIndex = 3
		reset(btnIndex)
		cur = np.copy(arr)
		showImage()
		ss.set(1)
		sIndex = (sIndex+1)%3
		s["text"]=sText[sIndex]

#scale of smooth/sharp
def val_s(val) :
	if (filename) : 
		global cur
		size = np.shape(arr)
		cur = np.copy(arr)

		#smooth
		if (sIndex == 1) :
			v = int(val)*2 - 1
			for i in range(size[0]) :
				for j in range(size[1]) :
					s = 0
					cnt = 0
					for a in range(-(v//2), (v+1)//2) :
						for b in range(-(v//2), (v+1)//2) : 
							if (i + a >= 0 and i + a < size[0]) :
								if (j + b >= 0 and j + b < size[1]) :
									s += arr[i + a][j + b]
									cnt += 1
					cur[i][j] = int(s/cnt)
		#sharp
		elif (sIndex == 2) :
			for i in range(int(val)-1) :
				cur = np.array(Image.fromarray(cur).filter(ImageFilter.SHARPEN))
		showImage()
		
#log F
def clickLog_f() :
	if (filename) :
		global log_fIndex, log_f, cur, btnIndex
		btnIndex = 4
		reset(btnIndex)
		log_fIndex = (log_fIndex+1)%2
		log_f["text"] = log_fText[log_fIndex]
		if (log_fIndex == 0) :
			cur = np.copy(arr)
		else :
			cur = np.log(1+np.absolute(np.fft.fft2(arr)))
			size = np.shape(cur)
			higest = np.nanmax(cur)
			lowest = np.nanmin(cur)
			gap = higest - lowest
			cur = np.uint8([[(cur[i][j]-lowest)/gap*255 for j in range(size[1])] for i in range(size[0])])
		showImage()
		
#2d fft
def clickTwo_f() :
	if (filename) :
		global two_fIndex, two_f, cur, btnIndex
		btnIndex = 5
		reset(btnIndex)
		two_fIndex = (two_fIndex+1)%3
		two_f["text"] = two_fText[two_fIndex]
		if (two_fIndex == 0) :
			cur = np.copy(arr)
		else :
			mag_fshift = np.fft.fftshift(np.fft.fft2(arr))
			#amp
			if (two_fIndex == 1) :
				cur = np.abs(np.fft.ifft2(np.fft.ifftshift(mag_fshift)))
			#phase
			elif (two_fIndex == 2) :
				cur = np.abs(np.fft.ifft2(np.exp(1j * np.angle(mag_fshift))))
			size = np.shape(cur)
			higest = np.nanmax(cur)
			lowest = np.nanmin(cur)
			gap = higest - lowest
			cur = np.uint8([[(cur[i][j]-lowest)/gap*255 for j in range(size[1])] for i in range(size[0])])		
		showImage()

#重設工作狀態(只有一個狀態開啟)
def reset(index) :
	global gls, glsIndex, sa, sb, bp, bpIndex, s, sIndex, ss, log_f, log_fIndex, two_f, two_fIndex
	if (index != 1) :
		glsIndex = 0
		gls["text"] = glsText[0]
		sa.set(0)
		sb.set(255)
	if (index != 2) : 
		bpIndex = 0
		bp["text"] = bpText[0]
	if (index != 3) :
		sIndex = 0
		s["text"] = sText[0]
		ss.set(1)
	if (index != 4) :
		log_fIndex = 0
		log_f["text"] = log_fText[0]
	if (index != 5) :
		two_fIndex = 0
		two_f["text"] = two_fText[0]

#視窗資訊
win = tk.Tk()
win.title("dip hw2")
win.resizable(False, False)
win.geometry("810x570+300+300")

#button
Open = tk.Button(win, text="open", width=10, height=2, command=clickOpen)
save = tk.Button(win, text="save", width=10, height=2, command=clickSave)
gls = tk.Button(win, text="(1) off", width=10, height=2, command=clickGLS)
bp = tk.Button(win, text="(2) off", width=10, height=2, command=clickBP)
s = tk.Button(win, text="(3) off", width=10, height=2, command=clickS)
log_f = tk.Button(win, text="(4) off", width=10, height=2, command=clickLog_f)
two_f = tk.Button(win, text="(5) off", width=10, height=2, command=clickTwo_f)

#label
imgL = tk.Label(win, width=300, height=300)
chgL = tk.Label(win, width=300, height=300)

#scale
sa = tk.Scale(win, from_=0, to=255, orient=tk.HORIZONTAL, length=630, showvalue=1, tickinterval=255, resolution=1, command=val_a)
sb = tk.Scale(win, from_=0, to=255, orient=tk.HORIZONTAL, length=630, showvalue=1, tickinterval=255, resolution=1, command=val_b)
ss = tk.Scale(win, from_=1, to=5, orient=tk.HORIZONTAL, length=630, showvalue=1, tickinterval=1, resolution=1, command=val_s)

#pack/place
Open.pack(side="top", anchor="nw", padx=20, pady=20)
save.pack(side="top", anchor="nw", padx=20, pady=0)
imgL.place(x=150, y=20)
chgL.place(x=480, y=20)
gls.pack(side="top", anchor="nw", padx=20, pady=20)
sa.place(x=150, y=340)
sb.place(x=150, y=410)
bp.pack(side="top", anchor="nw", padx=20, pady=0)
s.pack(side="top", anchor="nw", padx=20, pady=20)
ss.place(x=150, y=480)
log_f.pack(side="top", anchor="nw", padx=20, pady=0)
two_f.pack(side="top", anchor="nw", padx=20, pady=20)

#set
sb.set(255)

#一些變數
btnIndex = 1
arr = np.zeros(shape=(1,1))
cur = np.zeros(shape=(1,1))
bp_arr = np.zeros(shape=(8,300,300))
filename = None
savename = None
glsText = ["(1) off", "mode a", "mode b"]
glsIndex = 0
bpText = ["(2) off", "1", "2", "3", "4", "5", "6", "7", "8"]
bpIndex = 0
bpFirst = True
sText = ["(3) off", "smooth", "sharp"]
sIndex = 0
log_fIndex = 0
log_fText = ["(4) off", "log F"]
two_fIndex = 0
two_fText = ["(5) off", "amplitude", "phase"]

#主程式
win.mainloop()
