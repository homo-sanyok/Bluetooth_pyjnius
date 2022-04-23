#Первым делом вызывается функция getBoundedDevices, которая выдаёт списко всех сопряжённых устройств.
#Далее, после выбора названия нужного устройства, вызывается connectDevice, в которую передаётся название нужного устройства.
#После можно использовать функцию sendCommand для отправки команды на устройство (как пример, sendCommand(str(test))).
#И в последнюю очередь можно использовать getAnswer, чтобы получить ответ устройства
from jnius import autoclass

class Bluetooth:

    def __init__(self):
        self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')  #импортируемые классы
        self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
        self.UUID = autoclass('java.util.UUID')
        self.String = autoclass('java.lang.String')
        self.socket = None

    def getBoundedDevices(self): #получить массив названий всех сопряжённых устройств
        pd = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        res = []
        for device in pd:
            res.append(device.getName())
        return(res)

    def connectDevice(self, deviceName): #подключение к устройтву (в функцию передаётся название нужного устройства: тип данных str)
        pd = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        for device in pd:
            if (device.getName() == deviceName):
                self.socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                self.BluetoothAdapter.cancelDiscovery()
                self.socket.connect()

    def sendCommand(self, command): #принимает команду в виде строки (возвращает True, если команда была доставлена)
            if (self.socket.isConnected()):
                try:
                    send = self.socket.getOutputStream()
                    s = self.String(str(command) + "\n")
                    b = s.getBytes()
                    send.write(b)
                    send.flush()
                    return(True)
                except:
                    return(False)
            else:
                return(False)

    def getAnswer(self): #возвращает ответ от устройства в виде строки (если что-то пошло не так, возвращает False)
            if (self.socket.isConnected()):
                try:
                    get = self.socket.getInputStream()
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
