import crypto
import ubinascii

from network import LoRa


def get_device_eui():
    lora = LoRa(mode=LoRa.LORAWAN)
    print(ubinascii.hexlify(lora.mac()).upper().decode("utf-8"))


def lora_erase():
    lora = LoRa(mode=LoRa.LORAWAN)
    lora.nvram_erase()


def generate_keys(prefix=b"7079636f"):
    app_eui = prefix + ubinascii.hexlify(crypto.getrandbits(32))
    app_key = ubinascii.hexlify(crypto.getrandbits(128))
    print("AppEUI: {}".format(app_eui.decode()))
    print("AppKey: {}".format(app_key.decode()))
