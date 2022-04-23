#qpy:kivy
from jnius import autoclass

fox = 'fox_3_05c0d1405613c' # название устройства

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
            s = String("r" + "\n") # отсылаемое на устройство сообщение
            b = s.getBytes()
            send.write(b)
            send.flush()

            getting_bytes = get.read()
            test = []
            while (len(test) < 25):
                getting_bytes = get.read()
                test.append(getting_bytes)

            # getting_bytes = get.available()
            # test = getting_bytes

        else:
            test = 'no'
