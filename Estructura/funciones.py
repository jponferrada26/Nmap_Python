# -*- coding: utf-8 -*-

import socket
import sys
import os
import re
import nmap
import time
import MySQLdb

PATRON_IP = re.compile("^([0-9]\.|[1-9][0-9]\.|[1][0-9][0-9]\.|[2][0-5][0-5]\.){3}([0-9]|[1-9][0-9]|[1][0-9][0-9]|[2][0-5][0-5])$")
#Obtener la ip local del equipo actual
def obtenerIpEquipo():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    cadena = str(s.getsockname()).split('(')
    cadena = str(cadena[1]).split(',')
    return str(cadena[0]).replace("'","")


#Obtener plataforma del Sistema Operativo
def obtenerOS():
    nombre = sys.platform
    if nombre == 'linux2':
        return "Linux"
    elif nombre == 'win32' or nombre == 'win64':
        return "Windows"
    else:
        return "OSX"

def obtenerDatosNmapScan(resultadoNmap):
    fichero = open("resultadoAux.txt",'w')
    fichero.write(resultadoNmap)
    fichero.close()

    fechaYHora = ""
    host = ""
    puerto = ""
    protocolo = ""
    servicio = ""
    fichero = open("resultadoAux.txt",'r')

    lectura = str(fichero.readline()).split(";")

    conn = MySQLdb.connect("127.0.0.1","root","","BBDD_LOGS_RED")
    cursor = conn.cursor()

    print '\nHOST\t\tPUERTO\t\tPROTOCOLO\t\tSERVICIO'

    while True:
        lectura = str(fichero.readline()).split(";")
        if lectura == ['']:
            break
        host = lectura[0]
        puerto = int(lectura[4])
        protocolo = lectura[5]
        servicio = lectura[7]
        fechaYHora = str(time.strftime("%d/%m/%y ") + " - " + str(time.strftime("%H:%M")))

        print host, "\t" + str(puerto), "\t\t" + protocolo, "\t\t\t" + servicio
        cursor.execute(("INSERT INTO REGISTROS(IP,PUERTO,PROTOCOLO,SERVICIO,FECHA) VALUES('%s','%d','%s','%s','%s')") % (host,puerto,protocolo,servicio,fechaYHora))
        conn.commit()
    conn.close()
    fichero.close()

def scanTotal():
    ip = str(obtenerIpEquipo())
    ipTrozos = ip.split(".")
    ipFinal = ""
    if ipTrozos[0] >= '0' and ipTrozos[0] <= '127':
        ipFinal = ipTrozos[0]+"." + ipTrozos[1] + "." + ipTrozos[2]+ "." + "0/8"
    elif ipTrozos[0] >= '128' and ipTrozos[0] <= '191':
        ipFinal = ipTrozos[0]+"." + ipTrozos[1] + "." + ipTrozos[2]+ "." + "0/16"
    elif ipTrozos[0] >= '192' and ipTrozos[0] <= '223':
        ipFinal = ipTrozos[0] + "." + ipTrozos[1] + "." + ipTrozos[2]+ "." + "0/24"
    else:
        return "Rango de ip no válido."

    nmapScan = nmap.PortScanner()
    print "\nEscaneando red: " + ipFinal + " ..."

    nmapScan.scan(ipFinal, '0')

    print 'Los hosts a escanear son: ',
    print nmapScan.all_hosts()

    for host in nmapScan.all_hosts():
        print scanIpConcreta(host)

def scanIpConcreta(ip):
    try:
        if PATRON_IP.match(ip):
            print "\nEscaneando IP: " + ip + " ..."
            nmapScan = nmap.PortScanner()
            nmapScan.scan(ip, '1-60000')
            resultado = str(nmapScan.csv())
            obtenerDatosNmapScan(resultado)
        else:
            return "IP incorrecta."
    except Exception as e:
        return 'Debe tener instalado NMAP'
