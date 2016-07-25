#!/usr/bin/env python
# -*- coding: utf-8 -*-

########  15-puzzle

# Importamos la librería
import pygame
import sys
import random
import MySQLdb
from pygame.locals import *

class DriverMySQL:
	def __init__(self):
		# Establecemos la conexión
		self.Conexion =MySQLdb.connect(host='localhost', user='conan',passwd='crom', db='DBdeConan')
		# Creamos el cursor, pero especificando que sea de la subclase DictCursor
		self.micursor =self.Conexion.cursor()
		#print "Base de datos conectada"
		self.iniciaBD()

	def creaTablaBD(self):
		#print "Creando la tabla. . ."
		self.micursor.execute("DROP TABLE IF EXISTS 15puzzle;")
		self.micursor.execute("CREATE TABLE 15puzzle(nombre VARCHAR(50),puntos INT);")
		self.Conexion.commit()

	def limpiarBD(self):
		#print "Limpiando la tabla. . ."
		self.micursor.execute("DELETE FROM 15puzzle")
		self.Conexion.commit()

	def iniciaBD(self):
		# Creo la BD vacia
		#print "Crear Tabla 15puzzle"
		self.creaTablaBD()

		#print "Limpiar Tabla"
		self.limpiarBD()
		
		#print "Insertar Datos"
		query= "INSERT INTO 15puzzle (nombre,puntos) VALUES ('Ramon',7),('Antonio',10),('Belen',5);"
		self.micursor.execute(query)
		self.Conexion.commit()

	def obtenerDatos(self):
		#print "Obteniendo puntuaciones. . ."
		sql ="SELECT nombre,puntos FROM 15puzzle WHERE 1 ORDER BY puntos DESC LIMIT 5;"
		self.micursor.execute(sql)
		if self.micursor.rowcount>0:
			return self.micursor.fetchall()
		return None

	def guardarDato(self,nombre,puntos):
		#print "Guardando nueva puntuacion para "+str(nombre)+". . ."
		sql ="INSERT INTO 15puzzle (nombre,puntos) VALUES ('"+nombre+"',"+str(puntos)+");"
		self.micursor.execute(sql)
		self.Conexion.commit()

	def desconectar(self):
		self.Conexion.close()
		#print "Cerrando conexion. . ."

class Handler:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("crud.glade")
		self.handlers = {"onDeleteWindow": self.onDeleteWindow,
						 "onAceptar": self.onAceptar}
		self.builder.connect_signals(self.handlers)
		self.window = self.builder.get_object("window1")
		self.window.show_all()
		self.window.resize(300,200)

		# Campos de texto
		self.txt_nombre = self.builder.get_object("entry1")

	# Botones
	def onDeleteWindow(self, *args):
		self.driver.desconectar()
		Gtk.main_quit(*args)

	def onAceptar(self, button):
		#if (self.txt_nombre.get_text()!=""):
		self.driver.guardarDato(self.txt_nombre.get_text(),self.puntos)

def calcCoordenadasMatriz():
	coordenadas = []
	for i in range(4):
		coordenadas.append([])
		for j in range(4):
			cx = j*100+j*5+30
			cy = i*100+i*5+30
			coordenadas[i].append((cx,cy))
	return coordenadas

def cargaImagenesMatriz():
	# Array de imagenes
	cuadros = []
	for i in range(4):
		cuadros.append([])
		for j in range(4):
			k = i*4+j
			if (k!=15):
				img = "foto/"+str(k+1)+".png"
				cuadros[i].append(pygame.image.load(img))
				cuadros[i][j] = pygame.transform.scale(cuadros[i][j],(100,100))
	return cuadros

def calcCoordenadas():
	coordenadas = []
	for k in range(16):
		i= k/4; j= k%4
		cx = j*100+j*5+30
		cy = i*100+i*5+30
		coordenadas.append((cx,cy))
	return coordenadas

def cargaImagenes():
	# Array de imagenes
	cuadros = []
	for k in range(16):
		img = "foto/"+str(k+1)+".png"
		cuadros.append(pygame.transform.scale(pygame.image.load(img),(100,100)))
	return cuadros

def cargaFlechas():
	# Array de imagenes
	flechas= []
	for k in range(6):
		img = pygame.image.load("flechas.png")
		flechas.append(img.subsurface((k*155+1,1,150,150)))
		flechas[k] = pygame.transform.scale(flechas[k],(100,100))
	return flechas

def calcPosicion():
	posicion= range(16)
	random.shuffle(posicion)
	return posicion

def calcPuntos(posicion):
	pnts = 0
	for k in range(16):
		if (posicion[k]==k):
			pnts+= 1
	return str(pnts)

def buscarPiezaPos(posicion,p):
	for k in range(16):
		if posicion[k] == p:
			return k
	return -1

def main():
	nombre =raw_input("Introduce tu nombre antes de comenzar: ")

	# Creamos un reloj
	Reloj= pygame.time.Clock()

	# Iniciamos Pygame
	pygame.init()

	# Creamos una surface (la ventana de juego), asignándole un alto y un ancho
	Ventana = pygame.display.set_mode((600, 480))

	# Le ponemos un título a la ventana
	pygame.display.set_caption("15-Puzzle")

	# Cargamos las imágenes
	fondo = pygame.image.load("fondo15.png")
	foto = pygame.transform.scale(pygame.image.load("foto/foto.png"),(90,90))

	# Coordenadas para las imagenes
	coordenadas = calcCoordenadas()
	
	# Imagenes para los cuadros y posicion
	imagenes = cargaImagenes()
	posicion = calcPosicion()
	
	flechas = cargaFlechas()
	
	posNueva= posActual= posicion[15]
	
	tiempo = 300.0	# Tiempo inicial

	# Textos
	Fuente= pygame.font.Font(None, 28) # Elegimos la fuente y el tamaño

	# Bucle infinito para mantener el programa en ejecución
	while True:
		mov = False
		# Renderizamos (convertimos a imagen) el mensaje con la fuente definida
		Tiempo = Fuente.render(str(int(tiempo)), 0, (255,0,255))
		Puntos = Fuente.render(calcPuntos(posicion), 0, (255,0,255))

		Ventana.blit(fondo, (0, 0))
		Ventana.blit(foto, (496, 296))
		Ventana.blit(Puntos, (530, 102))
		Ventana.blit(Tiempo, (530, 52))
		for k in range(15):
			Ventana.blit(imagenes[k], coordenadas[posicion[k]])
		# La ultima imagen es la flecha
		flecha = int(tiempo*6)%6
		transparente = flechas[flecha].get_at((0, 0))
		flechas[flecha].set_colorkey(transparente)
		Ventana.blit(flechas[flecha], coordenadas[posicion[15]])

		pygame.display.flip()

		# Manejador de eventos
		for evento in pygame.event.get():
			# Pulsación de la tecla escape
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					sys.exit()
				elif evento.key == pygame.K_RIGHT:
					if posActual%4<3:
						posNueva = posActual+1
						mov = True
				elif evento.key == pygame.K_LEFT:
					if posActual%4>0:
						posNueva= posActual-1
						mov = True
				elif evento.key == pygame.K_DOWN:
					if posActual<12:
						posNueva= posActual+4
						mov = True
				elif evento.key == pygame.K_UP:
					if posActual>3:
						posNueva= posActual-4
						mov = True
			if evento.type == pygame.MOUSEBUTTONDOWN:
				px,py = pygame.mouse.get_pos()
				if (px>496 and px<585):
					if (py>435 and py<465):
						print "Cerrando. . ."
						sys.exit()

		if mov:
			k = buscarPiezaPos(posicion, posNueva)
			posicion[15],posicion[k] = posNueva,posActual
			posActual = posNueva

		# Asignamos un FPS = 4
		fps = 30.0
		Reloj.tick(fps)
		tiempo-= 1/fps
		
		if (tiempo<0) or calcPuntos(posicion)>15:
			break

	print "juego acabado"

	# JUEGO ACABADO
	# Renderizamos (convertimos a imagen) el mensaje con la fuente definida
	Tiempo = Fuente.render(str(int(tiempo)), 0, (255,0,255))
	Puntos = Fuente.render(calcPuntos(posicion), 0, (255,0,255))

	Ventana.blit(fondo, (0, 0))
	Ventana.blit(foto, (496, 296))
	Ventana.blit(Puntos, (530, 102))
	Ventana.blit(Tiempo, (530, 52))
	for k in range(15):
		Ventana.blit(imagenes[k], coordenadas[posicion[k]])
	
	# Textos
	final = Fuente.render("Conseguiste "+calcPuntos(posicion)+" puntos", 0, (0,255,255))
	Ventana.blit(final, (85, 120))
	pygame.display.flip()

	bd= DriverMySQL()		# Conexion
	bd.guardarDato(nombre, calcPuntos(posicion))
	datos= bd.obtenerDatos()

	if datos != None:
		# Renderizamos (convertimos a imagen) el mensaje con la fuente definida
		Tiempo = Fuente.render(str(int(tiempo)), 0, (255,0,255))
		Puntos = Fuente.render(calcPuntos(posicion), 0, (255,0,255))

		Ventana.blit(fondo, (0, 0))
		Ventana.blit(foto, (496, 296))
		Ventana.blit(Puntos, (530, 102))
		Ventana.blit(Tiempo, (530, 52))
		for k in range(15):
			Ventana.blit(imagenes[k], coordenadas[posicion[k]])
		
		# Textos
		Fuente= pygame.font.Font(None, 40) # Elegimos la fuente y el tamaño
		final = Fuente.render("Conseguiste "+calcPuntos(posicion)+" puntos", 0, (0,255,255))
		Ventana.blit(final, (85, 120))

		k = 0
		for nombre,puntos in datos:
			#print (nombre,str(puntos))
			pos = Fuente.render(nombre+"  "+str(puntos)+" puntos", 0, (255,0,0))
			Ventana.blit(pos, (100, 160+k*40))
			k+= 1

		pygame.display.flip()

	while True:
		salir = False
		for evento in pygame.event.get():
			# Pulsación de la tecla escape
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_ESCAPE:
					salir=True
		if salir==True:
			break
	return 0

if __name__ == '__main__':
	main()
