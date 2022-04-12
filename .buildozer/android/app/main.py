#qpy:kivy
from jnius import autoclass

fox = 'fox_3_05c0d1405613c'

BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
UUID = autoclass('java.util.UUID')
String = autoclass('java.lang.String')

global test
pd = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
socket = None
for device in pd:
    if (device.getName() == fox):
        socket = device.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
        BluetoothAdapter.cancelDiscovery()
        socket.connect()
        get = socket.getInputStream()
        send = socket.getOutputStream()

        if (socket.isConnected()):
            s = String("test" + "\n")
            b = s.getBytes()
            send.write(b)
            send.flush()

            test = 'ok'
        else:
            test = 'no'

# def get_socket_stream(name):
#     paired_devices = BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
#     socket = None
#     for device in paired_devices:
#         if device.getName() == name:
#             socket = device.createRfcommSocketToServiceRecord(
#                 UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
#             recv_stream = socket.getInputStream()
#             send_stream = socket.getOutputStream()
#             break
#     socket.connect()
#     return recv_stream, send_stream

#########################################################################################################

import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MyApp(App):

    def build(self):
        global test
        # recv_stream, send_stream = get_socket_stream(fox)
        # send_stream.write('test')
        # send_stream.flush()
        return TextInput(text=str(test))


if __name__ == '__main__':
    MyApp().run()
