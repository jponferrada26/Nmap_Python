# -*- coding: utf-8 -*-

from funciones import *

def mostrarOpciones():
	print '\n-----Menú escaneo de puertos-----\n'
	print '\t1. Escanear todos los puertos de la red'
	print '\t2. Nombre sistema operativo'
	print '\t3. IP local'
	print '\t4. Escanear IP concreta'
	print '\t0. Salir'

def limpiarPantalla():
	if os.name == "nt":
		os.system("cls")
	elif os.name == "posix":
		os.system("clear")

limpiarPantalla()
try:
	mostrarOpciones()
	opcion = int(raw_input(">>>Seleccione opción: "))
except Exception as e:
	opcion=9

while opcion !=0:
	if opcion==1:
		scanTotal()
		print '\nPulse INTRO para continuar...'
		raw_input()
		limpiarPantalla()
	elif opcion==2:
		print '\nSu Sistema Operativo es: ' + obtenerOS()
		print '\nPulse INTRO para continuar...'
		raw_input()
		limpiarPantalla()
	elif opcion==3:
		print '\nSu IP local es: ', obtenerIpEquipo()
		print '\nPulse INTRO para continuar...'
		raw_input()
		limpiarPantalla()
	elif opcion==4:
		print scanIpConcreta(raw_input("\nIP:(xx.xx.xx.xx) ---> "))
		print '\nPulse INTRO para continuar...'
		raw_input()
		limpiarPantalla()
	elif opcion==0:
		print '\nSALIENDO...\n'
	else:
		print '\n¡¡¡Opción erronea!!!'
		limpiarPantalla()

	mostrarOpciones()
	try:
		opcion = int(raw_input(">>>Seleccione opción: "))
	except Exception as e:
		opcion=9
