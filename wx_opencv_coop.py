#!/bin/env python
# -*- coding: utf-8 -*-

import wx
import cv2
import time
import numpy as np

class Myform(wx.Frame):
		
	def __init__(self,parent,id):
		wx.Frame.__init__(self , parent , id , 'Camera image from opencv 2.4 on wx panels version 2.0' , size=(1295,520) , pos=(25,25))			# zaszyty na stałe rozmiar okna - do poprawki !!!
		self.Centre()
		self.SetFocus()
		#self.prev = np.zeros(10)
		# to powyżej zostawić w spokoju
		
		##############################################################################################
		################################### INICJALIZACJA WŁAŚCIWA ###################################
		
		self.initializeParameters()							# podstawowe parametry pracy
		
		self.cap = cv2.VideoCapture(self.deviceNr)			# inicjalizacja strumienia z kamery
		#self.cap2 = cv2.VideoCapture(1)			# inicjalizacja strumienia z kamery
		self.cap.set(3,640)#1280)							# ustawienie parametrów strumienia
		self.cap.set(4,480)#720)

		#self.cap2.set(3,640)#1280)							# ustawienie parametrów strumienia
		#self.cap2.set(4,480)#720)																												# ustawiona na stałe rozdzielczość - można lepiej !!!
		#self.cap.set(5,30)									# ustawienie fps kamery na 30 Hz
		
		self.createGui()								# w tym miejscu tworzony jest interfejs graficzny
		
		self.initializeTimer()							# inicjalizacja stopera
		
		self.createCloseBinding()						# utworzenie dowiązań do zdarzenia zamknięcia okna
		
		##############################################################################################
		##############################################################################################
    
	def initializeTimer(self):
		print("INITIALIZE TIMER")
		self.stoper = wx.Timer(self)									# tworzę stoper
		self.Bind(wx.EVT_TIMER , self.timerUpdate , self.stoper)		# dowiązuję zdarzenie do tick'ów stopera
																		# nie uruchamiam stopera od razu, dopiero po wciśnięciu przycisku start
	
	def getNewFrame(self,parity):								# pobranie nowej klatki z kamery
		ret,frame = self.cap.read()
		
		#if self.prev.all() == frame.all():
		#	print("AAAAAAAAAAAAAAAAAAAAAA")
		#self.prev = frame
		
		#print frame
		#print("/")
		#print ret
		#print("//")
		print(time.time())
		
		
		# łapię surową klatkę z kamery
		if parity == 0:
			#ret,frame = self.cap.read()
			self.img_tmp_P.SetData( frame.tostring())					# i ustawiam w nim klatkę
			pic = self.img_tmp_P.ConvertToBitmap() 					# oraz konwertuję go na bitmap'ę
		elif parity == 1:
			#ret,frame = self.cap2.read()
			self.img_tmp_L.SetData( frame.tostring())					# i ustawiam w nim klatkę
			pic = self.img_tmp_L.ConvertToBitmap() 					# oraz konwertuję go na bitmap'ę				
		print("########################")
		
		return pic											# zwracam skonwertowaną klatkę w postaci bitmapy
	
	def createGui(self):
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)     		# tworzę główną tabelę
		
		self.pictureSizer = wx.GridSizer(1, 2, 1, 15)		# tworzę tabelę na obrazy
		
		self.pic = self.getNewFrame(self.parity)							# łapię pierwszą klatkę z kamery, żeby poznać jej rozmiary i ustawić cokolwiek w polach obrazu
		
		self.pictureLeft = wx.StaticBitmap(self, -1, self.pic)						# teraz tworzę dwa widgety do umieszczenia na gui
		self.pictureRight = wx.StaticBitmap(self, -1, self.pic)						# ...
		
		self.pictureSizer.Add(self.pictureLeft, 0 , wx.LEFT| wx.LEFT, 0)					# i dodaję je do tabeli obrazów
		self.pictureSizer.Add(self.pictureRight, 0 , wx.LEFT| wx.RIGHT, 0)					# ...
		
		self.mainSizer.Add(self.pictureSizer, 0 , wx.LEFT| wx.RIGHT, 0)		# dodaję tabelę obrazów do tabeli głównej
		
		self.ss_button = wx.Button(self,-1,'Start')						# tworzę przycisk start/stop
		self.ss_button.SetDefault()										# ustawiam go jako domyślny
		self.ss_button.Bind(wx.EVT_BUTTON, self.onKeyPress)				# dowiązuję do niego zdarzenie wciśnięcia
		self.mainSizer.Add(self.ss_button, 0, wx.CENTER| wx.BOTTOM)		# dodaję go do tabeli głównej
		
		self.SetSizer(self.mainSizer)									# ustawiam tabelę główną jako podstawową
    
		
	def createCloseBinding(self):
		self.Bind(wx.EVT_CLOSE , self.OnCloseWindow)
	
	def initializeParameters(self):
		self.timeGap = 66						# odstęp pomiędzy sygnałem ze stopera w [ms] (czyli 0.001 częstości próbkowania)
		self.parity = 0       	        		# przechowuje parzystość aktualnej klatki (0-parzysta, 1-nieparzysta)
		self.deviceNr = 0						# numer urządzenia w dev, pod którym jest żądana kamera
		self.img_tmp_L = wx.EmptyImage(640,480)#1280,720)			# tworzę pusty obraz																	# tutaj wraca jeszcze szycie na stałe rozmiaru !!!
		self.img_tmp_P = wx.EmptyImage(640,480)#1280,720)			# tworzę pusty obraz																	# tutaj wraca jeszcze szycie na stałe rozmiaru !!!

      
	def OnCloseWindow(self , event):    		# zamykanie programu
		self.stoper.Stop()
		self.Destroy()
    
	def onKeyPress(self , event):       				# zdarzenie kliknięcia przycisku
		label = event.GetEventObject().GetLabel()
	
		if label == 'Start':							# jeśli przycisk miał uruchomić system, to:
			self.ss_button.SetLabel('Stop')					# zmiana etykiety przycisku
			self.stoper.Start(self.timeGap)					# uruchomienie zainicjalizowanego wcześniej stopera
			
		elif label == 'Stop':							# jeśli przycisk miał system zatrzymać, to:
			self.ss_button.SetLabel('Start')				# zmiana etykiety przycisku
			self.stoper.Stop()								# zatrzymanie stopera
  

	def timerUpdate(self , event):				# zdarzenie wykonywane przy każdym tyknięciu stopera
		#print("TIMER: "+str(time.time()))
		#while True:
		#	time.sleep(0.33)
		#pic = self.getNewFrame(self.parity)		# łapię nową klatkę z kamery
		
		if self.parity == 0:					# jeśli klatka jest parzysta:
			pic = self.getNewFrame(self.parity)		# łapię nową klatkę z kamery
			self.parity = 1							# zmieniam flagę parzystości
			self.pictureRight.SetBitmap(pic)		# ustawiam ją na prawym polu obrazu
		elif self.parity == 1:					# jeśli klatka jest nieparzysta:
			pic = self.getNewFrame(self.parity)		# łapię nową klatkę z kamery
			self.parity = 0							# zmieniam flagę parzystości
			self.pictureLeft.SetBitmap(pic)			# ustawiam ją na lewym polu obrazu


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = Myform(parent=None,id=-1)
	frame.Show()
	app.MainLoop()
