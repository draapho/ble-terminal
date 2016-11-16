import pygatt
import logging


class BleDevice(pygatt.BGAPIBackend):

    def __init__(self):
        self.device = None
        self.adapter = pygatt.BGAPIBackend()
        self.adapter.start()

    def stop(self):
        self.adapter.stop()

    def scan(self, timeout=5):
        self.devices = self.adapter.scan(timeout)
        return self.devices

    def connect_name(self, name, devices=None):
        if devices is None:
            devices = self.devices
        for dev in self.devices:
            if name == dev['name']:
                return self.connect(dev['address'])
        return None

    def connect(self, address):
        self.device = self.adapter.connect(address)
        return self.device

    def discover_characteristics(self, device=None):
        if device is None:
            device = self.device
        characteristics = []
        for uuid in device.discover_characteristics().keys():
            try:
                device.char_read(uuid)
                characteristics.append(
                    {'uuid': uuid, 'handle': device.get_handle(uuid), 'readable': True})
            except Exception as e:
                if "unable to read" in str(e).lower():
                    characteristics.append(
                        {'uuid': uuid, 'handle': device.get_handle(uuid), 'readable': False})
                else:
                    raise e
        return characteristics

    def set_indication(self, uuid, device=None, callback=None, indication=True):
        if device is None:
            device = self.device
        device.subscribe(uuid, callback, indication)

    def read_characteristics(self, uuid, device=None):
        if device is None:
            device = self.device
        return device.char_read(uuid)

    def read_characteristics_handle(self, handle, device=None):
        if device is None:
            device = self.device
        return device.char_read_handle(handle)

    def write_characteristics(self, str, uuid, device=None):
        if device is None:
            device = self.device
        data = map(ord, str)
        for i in range(0, len(data), 20):
            device.char_write(uuid, data[i:i + 20])

    def write_characteristics_handle(self, str, handle, device=None):
        if device is None:
            device = self.device
        data = map(ord, str)
        for i in range(0, len(data), 20):
            device.char_write_handle(handle, data[i:i + 20])

if __name__ == "__main__":
    # logging.basicConfig()
    # logging.getLogger('pygatt').setLevel(logging.DEBUG)
    ble = BleDevice()
    print ble.scan()
    device = ble.connect_name("MC000000006")
    print device._address
    chars = ble.discover_characteristics(device)
    print chars
    # print chars[0]['uuid']
    print ble.read_characteristics(chars[1]['uuid'])
    ble.write_characteristics("<debug>STATUS</debug>", chars[0]['uuid'])
