from jnius import autoclass

class Bluetooth:

    def __init__(self):
        self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')  #импортируемые классы
        self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
        self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
        self.UUID = autoclass('java.util.UUID')
        self.String = autoclass('java.lang.String')
        self.socket = None
        self.res_pd = None

    def checkEnableBluetooth(self):  #возвращает True, если блютуз включён
        return self.BluetoothAdapter.isEnabled()

    def getBoundedDevices(self): #получить массив названий всех сопряжённых устройств
        pd = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        self.res_pd = []
        for device in pd:
            self.res_pd.append(device.getName())
        return(self.res_pd)

    def connectDevice(self, deviceName): #подключение к устройтву (в функцию передаётся название нужного устройства: тип данных str)
        try:
            pd = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
            for device in pd:
                if (device.getName() == deviceName):
                    self.socket = device.createRfcommSocketToServiceRecord(self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
                    self.BluetoothAdapter.cancelDiscovery()
                    self.socket.connect()
            return "connected"
        except:
            return "error_connect"

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

#########################################################################################################

import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from kivy.uix.gridlayout import GridLayout

class MyApp(App):

    def build(self):

        self.Bl = Bluetooth()
        arr = self.Bl.getBoundedDevices()

        layout=GridLayout(cols=1)
        lb=TextInput(text=str(arr))
        layout.add_widget(lb)


        self.lb=TextInput()
        layout.add_widget(self.lb)

        btn=Button(text="Отослать",
        on_press=self.Conekts
        )

        layout.add_widget(btn)

        self.comand=TextInput()
        layout.add_widget(self.comand)
        btn=Button(text="Отослать", on_press=self.Comands)
        layout.add_widget(btn)

        return layout

    def Conekts(self, *args):
        self.lb.text=str(self.Bl.connectDevice(str(self.lb.text)))

    def Comands(self, *args):
        self.Bl.sendCommand(str(self.comand.text))
        self.comand.text = self.Bl.getAnswer()

if __name__ == '__main__':
    MyApp().run()
