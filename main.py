# EU LoRaWAN device example
#
# This example node will increase a counter every 30 seconds and send the
# latest counter status as a LoRaWAN payload. We only use one byte in this
# example, so we need to reset the counter after it reaches 255.

from time import sleep
from lorawan.node import LoRaWANNode


# Change the example AppEUI and AppKey with lorawan.utils.generate_keys
_APP_EUI = "522d4954777f8e25"
_APP_KEY = "7526981c04eaca6a7267eecef4903277"


def main():
    # Enable debug
    LoRaWANNode.DEBUG = True

    print("Setup node...")
    node = LoRaWANNode(_APP_EUI, _APP_KEY)

    try:
        counter = 0
        while True:
            # Send the current counter as bytes
            node.send(bytes([counter]))

            # Increase counter, or reset if counter is 255
            if counter < 255:
                counter += 1
            else:
                counter = 0

            print("Sleep for 30 seconds...")
            sleep(30)
    finally:
        node.shutdown()


if __name__ == "__main__":
    main()
