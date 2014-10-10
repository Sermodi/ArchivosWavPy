#!/usr/bin/python2
#coding=utf-8
#
#   Autor: Sergio Modino Catalán
#
#   Descripción:
#       Dado un fichero .wav, recoge sus datos, tanto la información de su cabecera
#        como la información de sus muestras y las almacena.
#       Si se quiere a estas muestras se les puede aplicar un filtro de reverberación y
#        el resultado se guarda en un nuevo archivo de audio llamado "audio_reverberado.wav"
#
#
#   Estructura del archivo wav.
#
#   ffset    Description
#   ------    -----------
#   0x00     chunk id 'RIFF'
#   0x04     chunk size (32-bits)
#   0x08     wave chunk id 'WAVE'
#   0x0C     format chunk id 'fmt '
#   0x10     format chunk size (32-bits)
#   0x14     format tag (currently pcm)
#   0x16     number of channels 1=mono, 2=stereo
#   0x18     sample rate in hz
#   0x1C     average bytes per second
#   0x20     number of bytes per sample
#       1 =  8-bit mono
#       2 =  8-bit stereo or
#           16-bit mono
#       4 = 16-bit stereo
#   0x22     number of bits in a sample
#   0x24     data chunk id 'data'
#   0x28     length of data chunk (32-bits)
#   0x2C     Sample data

import struct
import sys


class Wav:
    """
    Clase que accede a los datos de un archivo .wav proporciona su cabecera
        y permite aplicar distintos filtros a los datos de muestra
    """

    #diccionario vacio donde se almacenarán todos los metadatos.
    #   dic{"cID": ,
    #       "cSize":        ,
    #       "waveID":       ,
    #       "formatID":     ,
    #       "formatSize":   ,
    #       "formatTag":    ,
    #       "channels":     ,
    #       "sRate":        ,
    #       "averageBps":   ,
    #       "BpSample":     ,
    #       "binSample":    ,
    #       "dataID":       ,
    #       "lengthData":    ,
    #       }
    __metadatos = {}  #Las dos barras bajas indican que es un elemento privado
    __datos = []
    #Constantes informativas:
    #FMTS indica que tipo de formateo ha de usarse para escribir o leer la muestra en el archivo binario.
    # "=B" será un unsigned char correspondiente a 1Byte de tamaño de muestra. 255 valores.
    # "=h" indica un short int para 2Bytes de tamaño de muestra.
    __FMTS = (None, "=B", "=h")
    #Si el archivo tiene un tamaño de muestra de 1 Byte se debe restar a cada muestra 128 al leerla,
    # y sumarselo al escribirla.
    __DCS = (None, 128, 0)

    #El valor máximo que puede alcanzar el tipo de datos del archivo.
    __MAX_tipoDatos = (None , 128, 32767)

    __fmt = 0
    __dc = 0

    def __init__(self, fichero):
        '''
        Metodo de inicialización de la clase wav
        '''
        assert isinstance(fichero, str)
        self.__nombre = fichero
        arch = open(fichero, 'rb')
        self.nFich = fichero
        self.__metadatos, self.__datos = self.obtener_datos(arch)


    def get_nombre(self):
        """
        Nombre del archivo
        """
        return self.__nombre

    def obtener_datos(self, f):
        """
        Dado un fichero .wav se lee su cabecera y los datos de muestreo.
            --return :  * diccionario con los metadatos del archivo wav.
                        * array con los datos de muestreo del archivo wav.
        """
        metadatos = {}
        datos = []
        #Se inicia la lectura del fichero, con la estructura comentada en la cabecera de este archivo.
        #   El primer dato a leer son 4Bytes que deben mostrar la cadena de caracteres "RIFF"
        chunk = f.read(4)
        dato = struct.unpack("4s", chunk)[
            0]  #struct.unpack genera una tupla de un elemento, se selecciona ese elemento (el 0).
        dato = dato.decode("utf-8")
        #Se comprueba que el valor leido es RIFF. Valor inicial de la cabecera de cualquier .wav
        if str(dato) != "RIFF":
            print("El archivo indicado no es un archivo .wav\n El programa se reiniciará")
            exit(1)
        #Se almacena el valor leido en el diccionario.
        metadatos["cID"] = dato

        #   El siguiente dato a leer es el tamaño "chunk size" un entero de 32 bits (4 Bytes)
        chunk = f.read(4)
        dato = struct.unpack("<L", chunk)[0]  #"L" indica que los digitos a leer son enteros, de 4bytes por defecto.
        dato = str(dato).decode("utf-8")
        metadatos["cSize"] = dato

        #   "Wave chunk id" una palabra de 4Bytes que debe ser "WAVE" si se trata de un archivo ,wav estandar
        chunk = f.read(4)
        dato = struct.unpack("4s", chunk)[
            0]  #"4s" indica que se va a leer una palabra de 4 bytes, 4 carácteres de un byte
        dato = dato.decode("utf-8")
        if (str(dato) != "WAVE"):
            print(
                "El archivo indicado no es un archivo .wav o está comprimido.\nSe requiere que el archivo sea un .wav sin comprimir.\n El programa se reiniciará")
            exit(1)
        metadatos["waveID"] = dato

        #   "format chunk id" una palabra de 4Bytes que suele ser 'fmt '
        chunk = f.read(4)
        dato = struct.unpack("4s", chunk)[
            0]  #"4s" indica que se va a leer una palabra de 4 bytes, 4 carácteres de un byte
        dato = dato.decode("utf-8")
        metadatos["formatID"] = dato

        #   "format chunk size" tamaño del
        chunk = f.read(4)
        dato = struct.unpack("<L", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["formatSize"] = dato

        #   "format tag" un entero, si es 1 su valor es pcm.
        chunk = f.read(2)
        dato = struct.unpack("<H", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["formatTag"] = dato

        #   "number of channels" numero de canales en uso 1=mono, 2= estereo.
        chunk = f.read(2)
        dato = struct.unpack("<H", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["channels"] = dato

        #   "sample rate" ratio de muestreo en herzios.
        chunk = f.read(4)
        dato = struct.unpack("<L", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["sRate"] = dato

        #   "average bytes per second" Tasa media de bytes por segundo (entero de 4Bytes.)
        chunk = f.read(4)
        dato = struct.unpack("<L", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["averageBps"] = dato

        #   "Bytes per samble" 1= 8bits mono ; 2 = 8bits stereo ó 16bits mono; 4 = 16bits stereo.
        chunk = f.read(2)
        dato = struct.unpack("<H", chunk)[0]
        dato = str(dato).decode("utf-8")

        metadatos["BpSample"] = int(dato)

        #   "bits in sample" Numero de bits por muestra.
        chunk = f.read(2)
        dato = struct.unpack("<H", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["bInSample"] = dato

        #   "data chunk ID" Identificador de datos, suele ser "data".
        chunk = f.read(4)
        dato = struct.unpack("<4s", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["dataID"] = dato

        #   "length of data chunck" longitud de los datos.
        chunk = f.read(4)
        dato = struct.unpack("<L", chunk)[0]
        dato = str(dato).decode("utf-8")
        metadatos["lengthData"] = dato
        #Todas las operaciones anteriores se podrían realizar en una misma consulta struct.unpack
        # pero se ha hecho así para que sea más legible, aunque se pierda tiempo de ejecución.

        bps = self.get_BpS(metadatos["BpSample"])
        #Se recoge el tipo del formato de las muestras de __FMTS y si es necesario cambiar los valores de __DCS
        self.__fmt = self.__FMTS[bps]
        self.__dc = self.__DCS[bps]

        self.__maxT = self.__MAX_tipoDatos[bps]

        numDatos = int(metadatos["lengthData"]) / bps
        if metadatos["channels"] != "1":
            #Se divide a la mitad porque las muestras en estereo son la mitad.
            numDatos = numDatos / 2
            datos.append([])
            datos.append([])

        #Ahora se leen los datos de cada muestra con el tamaño indicado en metadatos["BpSample"]
        for i in range(numDatos):
            if (metadatos["channels"] != "1"):
                chunk = f.read(bps)
                dato = struct.unpack(self.__fmt, chunk)[0]
                dato -= self.__dc
                datos[0].append(dato)
                chunk = f.read(bps)
                dato = struct.unpack(self.__fmt, chunk)[0]
                dato -= self.__dc
                datos[1].append(dato)
            else:
                chunk = f.read(bps)
                dato = struct.unpack(self.__fmt, chunk)[0]
                dato -= self.__dc
                datos.append(dato)

        return metadatos, datos

    def get_fMuestreo(self):
        """
        Devuelve la frecuencia de muestreo del archivo.
        """
        return self.__metadatos["sRate"]

    def get_numCanales(self):
        """
        Devuelve el número de canales en los que se ha guardado el audio.
        """
        return self.__metadatos["channels"]

    def get_duracion(self):
        """
        Devuelve la duración en segundos del fichero de audio.
        """
        BytesSeg = self.__metadatos["averageBps"]
        longDatos = self.__metadatos["lengthData"]
        #Segundos = longitud de datos en Bytes / Bytes por segundo
        return float(longDatos) / float(BytesSeg)

    def calcula_duracion(self, longDatos, BytesSeg):
        """
        Dada la longitud de los Datos en Bytes y los Bytes por segundo del audio se devuelve
          la duración del audio.
        :rtype : float
        :param longDatos: longitud de los datos de muestra.
        :param BytesSeg:  Numero de Bytes por segundo del audio.
        """
        assert isinstance(longDatos, float)
        assert isinstance(BytesSeg, float)

        return longDatos / BytesSeg

    def imprimir_metadatos(self):
        """
            Muestra todos los metadatos del archivo .wav indicado.
        """
        print("chunk id                          \t : \t" + self.__metadatos["cID"])
        print("chunk size                        \t : \t" + self.__metadatos["cSize"])
        print("wave chunk id                     \t : \t" + self.__metadatos["waveID"])
        print("format chunk id                   \t : \t" + self.__metadatos["formatID"])
        print("format size                       \t : \t" + self.__metadatos["formatSize"])
        print("format tag                        \t : \t" + self.__metadatos["formatTag"])
        #Se comprueba el tipo de canal 1 para "mono" y 2 para "stereo"
        if (self.__metadatos["channels"] == "2"):
            aux = "stereo"
        else:
            aux = "mono"
        print("number of channels                \t : \t" + aux)
        print("samble rate in Hz                 \t : \t" + self.__metadatos["sRate"] + " Hz")
        print("average bytes per second          \t : \t" + self.__metadatos["averageBps"] + " Bytes por segundo." )
        #Determinamos cuantos bytes por muestra se utilizan.
        bpS = self.__metadatos["BpSample"]
        aux = self.get_BpS(bpS)
        print("number of bytes per sample        \t : \t" + str(aux) + " Bytes por muestra.")
        print("number of bits in a sample        \t : \t" + self.__metadatos["bInSample"] + " bits en una muestra.")
        print("data chunk id                     \t : \t" + self.__metadatos["dataID"])
        print("length of data chunk              \t : \t" + self.__metadatos["lengthData"])

    def get_BpS(self, bps):
        """
        Los Bytes por muestra están guardados con un número del uno al 4, pero ese valor no corresponde
            a los bytes, sino que:
                + El valor 1 corresponde a 1Byte en mono.
                + El valor 2 corresponde a 2Bytes en mono ó 1 Byte en stereo.
                + El valor 4 corresponde a 2Bytes en stereo.
        --return : un entero de 1 a 2 con el tamaño en bytes de cada muestra.
        :rtype : integer
        :type bpS: string : "1", "2" , "4"
        """
        aux = 0
        if bps == 1:
            aux = 1
        elif bps == 2 and not self.is_stereo():
            aux = 2
        elif bps == 2 and self.is_stereo():
            aux = 1
        elif bps == 4:
            aux = 2

        return aux

    def add_reverberacion(self, retardo, coefs):
        """
        Para todos los datos de muestreo se añade un filtro de reverberación.
        """
        i = 0
        y = 0.0
        fy = []

        numCoef = len(coefs)  #numero de coeficientes con delay
        for dato in self.__datos:
            #Se recorre cada dato en el array de datos para ap
            # licarle la función
            if self.is_stereo():
                i = 0
                fy1 = []
                for i in range(len(dato)):
                    if i < (numCoef * int(retardo)):  #Si la medida es menor q el m
                        fy1.append(dato[i])
                    else:
                        y = self.calcula_reverberacion(i, int(retardo), coefs)
                        fy1.append(y)
                fy.append(fy1)
            else:
                if i < (numCoef * int(retardo)):  #Si la medida es menor q el m
                    fy.append(dato)
                    i += 1
                else:
                    y = self.calcula_reverberacion(self.__datos.index(dato), int(retardo), coefs)
                    fy.append(y)
        return fy

    def calcula_reverberacion(self, posicion, retardo, coefs, opt=0):
        """
        y(n) = x(n) + coef[0]*x(n - retardo) + coef[1]*x(n - 2 * retardo) ...
        """
        if self.is_stereo():
            y = self.__datos[opt][posicion]
        else:
            y = self.__datos[posicion]
        for i in range(len(coefs)):
            if self.is_stereo():
                y += coefs[i] * self.__datos[opt][posicion - ((i + 1) * retardo)]
            else:
                y += coefs[i] * self.__datos[posicion - ((i + 1) * retardo)]
        return y


    def is_stereo(self):
        """
        Indica si el archivo .wav al que pertenece esta entidad tiene un sonido mono o estereo.
        """
        if self.__metadatos["channels"] == "1":
            return False
        else:
            return True

    def generar_reverberacion(self, retardo, coef, duracion=0.0):
        fy = self.add_reverberacion(retardo, coef)

        if self.is_stereo():
            datoMayor = max((max(fy[0]), max(fy[1]), abs(min(fy[0])), abs(min(fy[1]))))
        else:
            datoMayor = max((max(fy), abs(min(fy))))

        fich = open("audio_reverberado.wav", "wb")  #Abrimos el archivo en modo de escritura binaria.

        if duracion == 0.0 or duracion >= self.get_duracion():
            #La duración de los datos será la duración del archivo.
            lengthData = int(self.__metadatos["lengthData"])
        else:
            #La longitud de los datos se calcula como la Duración en segundos por Los Bytes por segundo.
            lengthData = duracion * float(self.__metadatos["averageBps"])

        #Se compone la cabecera.
        cabecera = struct.pack('<4sL4s4sLHHLLHH4sL'
                               , str(self.__metadatos["cID"])
                               , int(lengthData) + 36
                               , str(self.__metadatos["waveID"])
                               , str(self.__metadatos["formatID"])
                               , int(self.__metadatos["formatSize"])
                               , int(self.__metadatos["formatTag"])
                               , int(self.__metadatos["channels"])
                               , int(self.__metadatos["sRate"])
                               , int(self.__metadatos["averageBps"])
                               , int(self.__metadatos["BpSample"])
                               , int(self.__metadatos["bInSample"])
                               , str(self.__metadatos["dataID"])
                               , int(lengthData)  #Añadimos las muestras q genere el eco a mayores
        )
        fich.write(cabecera)

        if self.is_stereo():
            completo = []  #unión de la lista con las muestras izquierdas y derechas
            for i in range(len(fy[0])):
                for j in range(len(fy)):
                    #Para cada uno de los canales de la muestra se añaden a la lista
                    # pero escalandolos para que el resultado esté dentro del intervalo máximo del tipo de datos.

                    completo.append(fy[j][i])

            for y1 in completo:

                #Se divide por el valor máximo de la secuencia.
                aux = y1/datoMayor
                #Se multiplica por el valor máximo del tipo de datos utilizado
                aux = aux * self.__maxT

                aux = int(aux) + self.__dc
                muestra = struct.pack(self.__fmt, int(aux))
                fich.write(muestra)
        else:
            for y in fy:
                #Se divide por el valor máximo de la secuencia.
                aux = y/datoMayor
                #Se multiplica por el valor máximo del tipo de datos utilizado
                aux = aux * self.__maxT

                aux = int(aux) + self.__dc
                muestra = struct.pack(self.__fmt, int(aux))
                fich.write(muestra)
                #formatTag, channels, sRate, averageBps, BpSample, bInSample, dataID, lengthData


