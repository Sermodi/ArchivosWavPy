#!/usr/bin/python2
#coding=utf-8
#
#   Autor: Sergio Modino Catalán
#
#   Descripción:
#       Clase lanzadora de la clase Wav.
#       Recibirá mínimo 3 argumentos, <fichero de audio> <retardo> <coeficiente1 coeficiente2 ...>
#
#
#   Referencias:
#       Riff WAVE file format:
#           http://sox.sourceforge.net/AudioFormats-11.html#ss11.6
#
#       WAVE PCM soundfile format, Standford
#           https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
#
#       struct — Interpret strings as packed binary data
#           https://docs.python.org/2.7/library/struct.html
#
from Wav import Wav
import sys

if sys.version_info[0] != 2:
    print("ERROR: Este programa está escrito en Python versión 2, si está ejecutandolo en python3 este programa se cerrará.\n"
          "\tEscriba en consola 'python2 <nombre del programa>'")
    exit(1)
audio = ""
retardo = 0
coef = []

if (len(sys.argv) <= 3):
    print("ERROR: número de argumentos erroneo.\nEl formato de insercción de argumentos debe ser así:\n"
          "\tprograma ficheroWavOriginal retardo coef1 coef2 coef3...")
    exit(1)
else:
    #De los argumentos introducidos es necesario que minimo haya 4 argumentos
    #   el argv[0] es el self del programa.
    for i in range(len(sys.argv)):
        aux = sys.argv[i]
        if i == 1:
            audio = aux
        elif i == 2:
            retardo = int(aux)
        elif i > 2:
            coef.append(float(aux))

archivo = Wav(audio)

#Si se descomenta la linea siguiente se verá por pantalla los metadatos del archivo.
#archivo.imprimir_metadatos()

#Se muestra la frecuencia de muestreo, numero de canales y la duración en segundos.
print("Archivo de audio " + str(archivo.get_nombre())
      + "\n\tFrecuencia de muestreo: " + str(archivo.get_fMuestreo())
      + "\n\tNumero de canales :     " + str(archivo.get_numCanales())
      + "\nDuración de " + str(archivo.get_duracion()) + " segundos.\n")

duracionFinal = input("\t¿Cuantos segundos ha de durar el archivo final?\n")
if duracionFinal > archivo.get_duracion():
    print("Los segundos indicados exceden la longitud del fichero, por lo tanto se usará la duración máxima del fichero.")
    duracionFinal = archivo.get_duracion()
archivo.generar_reverberacion(retardo, coef, duracionFinal)