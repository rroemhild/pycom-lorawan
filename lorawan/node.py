import usocket
import ubinascii

from network import LoRa


class LoRaWANNode:
    """LoRaWAN node for LoRa capable Pycom modules"""

    DEBUG = False

    def __init__(
        self,
        app_eui,
        app_key,
        dev_eui=None,
        region=LoRa.EU868,
        sf=7,
        adr=True,
        dr=5,
        timeout=10,
    ):
        """Initialize the LoRaWAN node and setup the connection

        Pycom LoRa docs: https://docs.pycom.io/firmwareapi/pycom/network/lora/

        Parameters
        ----------
        app_eui : string
            The Application EUI.
        app_key : string
            The Join-Key, also known as Application Key.
        dev_eui : string
            The Device EUI, default is the LoRa MAC of the device.
        region : integer
            The LoRaWAN region to operate in.
        sf : integer
            Sets the desired spreading factor. Accepts values between 7 and 12.
        adr : boolean
            Enables Adaptive Data Rate
        dr : integer
            Specify the initial data rate for the Join Request.
        timeout : integer
            The maximum time in seconds to wait for the Join Accept message and socket.
        """

        self._timeout = timeout
        self._app_eui = ubinascii.unhexlify(app_eui)
        self._app_key = ubinascii.unhexlify(app_key)
        self._dev_eui = dev_eui
        self._socket = None
        self._dr = dr
        self.lora = LoRa(mode=LoRa.LORAWAN, region=region, sf=sf, adr=adr)

        self.setup()

    def setup(self):
        """Setup LoRaWAN node

        Re-use saved LoRaWAN session from nvram or join the network with OTAA.
        """

        self.lora.nvram_restore()

        if not self.lora.has_joined():
            self.join()
        else:
            self._open_socket()

    def join(self):
        """Join the network"""

        try:
            timeout = self._timeout * 1000

            self.dprint("Send join request")
            if self._dev_eui:
                self.lora.join(
                    activation=LoRa.OTAA,
                    auth=(self._dev_eui, self._app_eui, self._app_key),
                    timeout=timeout,
                    dr=self._dr,
                )
            else:
                self.lora.join(
                    activation=LoRa.OTAA,
                    auth=(self._app_eui, self._app_key),
                    timeout=timeout,
                    dr=self._dr,
                )

            if self.lora.has_joined():
                self.lora.nvram_save()
                self._open_socket()
                self.dprint("Joined network")
        except LoRa.timeout:
            self.dprint("Timeout error")
            raise

    def _open_socket(self, timeout=6):
        """Open the LoRa socket"""

        self._socket = usocket.socket(usocket.AF_LORA, usocket.SOCK_RAW)
        self._socket.setsockopt(usocket.SOL_LORA, usocket.SO_DR, self._dr)
        self._socket.settimeout(timeout)

    def reset(self):
        """Reset LoRaWAN socket

        Clear on device stored LoRaWAN session and re-join the network.
        """

        self._socket.close()
        self.lora.lora_erase()
        self.join()

    def send(self, payload, port=1):
        """Send uplink data as bytes



        Parameters
        ----------
        payload : bytes, string, integers, float
            The uplink payload. If the payload is not bytes, the module tries
            to convert the playload to bytes.
        port : integer
            The LoRaWAN port used for the uplink.
        """

        self._socket.bind(port)
        if self.lora.has_joined():
            if isinstance(payload, (float, str, int)):
                payload = bytes([payload])
            self.dprint("Send payload: {}".format(payload))
            self._socket.setblocking(True)
            self._socket.send(payload)
            self._socket.setblocking(False)
            self.lora.nvram_save()

    def recv(self, rbytes=1):
        """Receive ammount of bytes from a downlink payload

        Paramaters
        ----------
        rbytes : integer
            The amount of bytes to receive from the latest downlink.
        """

        retval = self._socket.recvfrom(rbytes)
        self.dprint("Recv payload: {}, port: {}".format(retval[0], retval[1]))
        return retval

    def shutdown(self):
        """Close socket and shutdown the LoRa modem"""

        self._socket.close()
        self.lora.power_mode(LoRa.SLEEP)

    def dprint(self, message):
        """Simple debug console messages

        Parameters
        ----------
        message : string
            The debug message to print out to the terminal.
        """

        if self.DEBUG:
            print("LoRaWANNode: {}".format(message))
