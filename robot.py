import PIL.ImageGrab
from PIL import Image
import time
import win32api
import win32con
time.sleep(3)
zero_count = 0
f = open('p.txt',"a")
while True:
	time.sleep(0.4)
	im = PIL.ImageGrab.grab()
	#im.show()
	#im.save('example.bmp')
	#im = Image.open('example.bmp')
	#nim = im.crop((929,72,1338,481))
	def getGrid(im,x,y):
		startx = 930
		starty = 72
		r = 51
		g = 0
		b = 0
		#nim = im.crop((startx+x*r,starty+y*r,startx+x*r+r,starty+y*r+r))
		for i in range(startx+x*r+5,startx+x*r+15):
			for j in range(starty+y*r+20,starty+y*r+30):
				p = im.getpixel((i,j))
				g = g + p[1] - p[0]
				b = b + p[2] - p[0]
		return (g,b)
				
	startx = 930
	starty = 72
	r = 51
	m = [['u' for col in range(8)] for row in range(8)]  
	for x in range(8):
		for y in range(8):
			g = getGrid(im,x,y)
			print(g,file=f)
			#print(g)
			if g[0] < -3000 and g[1] < -2000:   # red
				#print('r')
				m[y][x] = 'r'
			elif g[0] < 0 and g[0] >=-2000 and g[1] < 0 and g[1] >=-2000: # dark
				#print('d')
				m[y][x] = 'd'
			elif g[0] > 0 and g[1] < 0:   # green
				#print('g')
				m[y][x] = 'g'
			elif g[0] < 0 and g[1] > 0:   # p
				#print('p',x,y)
				m[y][x] = 'p'
			elif g[0] > 0 and g[1] > 0:   # blue
				#print('b')
				m[y][x] = 'b'
			elif g[0] < 0 and g[0] > -5000 and g[1] < -5000: # yellow
				#print('y')
				m[y][x] = 'y'
				#im.crop((startx+x*r+5,starty+y*r+20,startx+x*r+15,starty+y*r+30)).show()
			else:
				print('unknow color')

	def test_click(l,m,c,x,y,px,py):
		startx = 930
		starty = 72
		r = 51
		if c=='u' or x<0 or y<0 or px<0 or py<0:
			return
		if m[x][y] == c:
			l.append((x,y,px,py))
			print("(%d,%d)->(%d,%d)"%(x,y,px,py))
	l = []
	for x in range(8):
		for y in range(7,-1,-1):
			c = m[x][y]
			try:
				if m[x+1][y] == c:
					test_click(l,m,c,x+3,y,x+2,y)
					test_click(l,m,c,x+2,y-1,x+2,y)
					test_click(l,m,c,x+2,y+1,x+2,y)
				if m[x][y-1] == c:
					test_click(l,m,c,x,y-3,x,y-2)
					test_click(l,m,c,x-1,y-2,x,y-2)
					test_click(l,m,c,x+1,y-2,x,y-2)
				if m[x+2][y] == c:
					test_click(l,m,c,x+1,y+1,x+1,y)
					test_click(l,m,c,x+1,y-1,x+1,y)
				if m[x][y-2] == c:
					test_click(l,m,c,x-1,y-1,x,y-1)
					test_click(l,m,c,x+1,y-1,x,y-1)
			except IndexError:
				pass
	print(l)
	if not len(l):
		zero_count = zero_count + 1
		if zero_count == 3:
			win32api.keybd_event(90,0,0,0) #z键位码是90  
			win32api.keybd_event(90,0,win32con.KEYEVENTF_KEYUP,0)  
			print('z')
		continue
	else:
		zero_count = 0
	import random
	t = random.choice(l)
	print(t)
	win32api.SetCursorPos([startx+t[1]*r+25,starty+t[0]*r+25])    #为鼠标焦点设定一个位置
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
	time.sleep(0.1)
	win32api.SetCursorPos([startx+t[3]*r+25,starty+t[2]*r+25])    #为鼠标焦点设定一个位置
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0) 
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
	win32api.SetCursorPos([300,300])	
		  
	  

