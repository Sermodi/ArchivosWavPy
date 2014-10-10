  ##########################################################
 #                                                         #
 # ANALIZADOR DE FICHERO WAV Y FILTRADO POR REVERBERACIÓN #
 #                                                         #
 ########################################################### 

---------------
-  EJECUCIÓN: -
---------------
    Este programa está escrito en Python 2.7.3, y es compatible con versiones python 2.6 y superiores, pero no compatible con python 3+.
    Si se quiere ejecutar el programa en distribuciones GNU/LINUX basadas en Debian se utilizará la siguiente sentencia:
        
       python LectorWav.py <nombre del archivo .wav> <retardo> <coeficiente1 coeficiente2 ...>

    Para realizar la ejecución del programa en otros sistemas sería necesario utilizar el comando python2 en vez de python.

       python2 LectorWav.py <nombre del archivo .wav> <retardo> <coeficiente1 coeficiente2 ...>

    Si los datos introducidos son correctos (el archivo wav existe y hay un mínimo de 3 argumentos de programa) empezará la ejecución del programa,
      · Inicialmente se mostrarán datos del fichero .wav facilitado.
      · Se pedirá cuanto tiempo ha de durar el fichero final (con reverberación)
      · Se harán los cálculos de reverberación
      · Se crea el nuevo archivo de nombre "audio_reverberado.wav", con el filtro de reverberación aplicado y la duración en segundos indicada.

----------------------
- Archivos Adjuntos  -
----------------------

    Junto a este archivo de información se adjuntan los siguientes archivos:
        · LectorWav.py  ----------  Clase lanzadora.
        · Wav.py        ----------  Clase que contiene toda la logica de lectura del fichero wav y la ejecución del filtro.
        · audio1.wav    ----------  Audio utilizado para la prueba.
        · audio_reverberado.wav --  Audio resultado de la ejecución del filtro con 'python2 LectorWav.py audio1.wav 0.7 0.5 0.3 0.1'
        · audio_reverberado2.wav -  Audio resultado de la ejecución del filtro con 'python2 LectorWav.py audio1.wav 5000 0.5 0.3 0.1' indicando un
            mayor retardo para que se denote la reverberación más adecuadamente.

------------------
- OBSERVACIONES  -
------------------

    Se ha presupuesto que el tiempo que debe durar el archivo resultado de la reverberación es menor o igual al tiempo que dura el
    archivo original, debido a que no se especificaba nada sobre este aspecto. Así si un archivo de audio dura 3 segundos el archivo
    reverberado durará 3 segundo o menos, pero nunca se permitirá que un archivo dure 0 segundos.


    Al aplicar el filtro de reverberación si el valor de retardo es muy pequeño el resultado de calcular el filtro puede exceder 
    el valor máximo de representación de ese valor en cada muestra. La primera decisión tomada es que si se excedía el valor máximo
    (32767 para los Short int) ese valor se cambiase al valor máximo, de este modo nunca se excedería ese valor. Pero en este caso
    el audio resultante contenía mucho ruido.
    La solución proporcionada por el profesor ha sido dividir todos los valores de las muestras con reverberación por el valor máximo
    de este modo los valores resultantes eran menores que 1, y con esos valores multiplicarles el valor máximo del tipo de datos en el
    que se almacenará la muestra, de esta forma se evita ese ruido generado sin dañar sustancialmente la muestra. 

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
