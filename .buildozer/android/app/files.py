from android.storage import primary_external_storage_path
global primary_ext_storage
primary_ext_storage = primary_external_storage_path()

from jnius import autoclass

#########################################################################################################

FileOutputStream = autoclass('java.io.FileOutputStream')
FileInputStream = autoclass('java.io.FileInputStream')
String = autoclass('java.lang.String')

def writeString(fileName, str):     #Функция для записи строки в файл (функция сама создаёт файл, если он ещё не был создан)
    out = FileOutputStream(fileName + '.txt')
    out.write(String(str + '\n').getBytes())
    out.close()

def readString(fileName):           #Функция для чтения строки из файла
    input = FileInputStream(fileName + '.txt')
    receivedString = ""
    get = input.read()
    while (get != 10):
        receivedString += chr(get)
        get = input.read()
    input.close()
    return(receivedString)
