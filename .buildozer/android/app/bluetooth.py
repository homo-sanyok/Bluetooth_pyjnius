#Первым делом вызывается функция getBoundedDevices, которая выдаёт списко всех сопряжённых устройств.
#Далее, после выбора названия нужного устройства, вызывается connectDevice, в которую передаётся название нужного устройства.
#После можно использовать функцию sendCommand для отправки команды на устройство (как пример, sendCommand(str(test))).
#И в последнюю очередь можно использовать getAnswer, чтобы получить ответ устройства
from jnius import autoclass

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')  #импортируемые классы
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')
String = autoclass('java.lang.String')

global socket

def getBoundedDevices(): #получить массив названий всех сопряжённых устройств
    pd = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    res = []
    for device in pd:
        res.append(device.getName())
    return(res)

def connectDevice(deviceName): #подключение к устройтву (в функцию передаётся название нужного устройства: тип данных str)
    global socket
    pd = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
    socket = None
    for device in pd:
        if (device.getName() == deviceName):
            socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
            BluetoothAdapter.cancelDiscovery()
            socket.connect()

def sendCommand(command): #принимает команду в виде строки (возвращает True, если команда была доставлена)
    global socket
        if (socket.isConnected()):
            try:
                send = socket.getOutputStream()
                s = String(str(command) + "\n")
                b = s.getBytes()
                send.write(b)
                send.flush()
                return(True)
            except:
                return(False)
        else:
            return(False)

def getAnswer(): #возвращает ответ от устройства в виде строки (если что-то пошло не так, возвращает False)
    global socket
        if (socket.isConnected()):
            try:
                get = socket.getInputStream()
                getting_byte = get.read()
                res = ""
                while (getting_byte != 13):
                    res += chr(getting_byte)
                    getting_byte = get.read()
                return (res)
            except:
                return (False)
        else:
            return (False)
