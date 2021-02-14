# Pycom LoRaWAN

This is a LoRaWAN node module for LoRa capable Pycom modules. I use this module for my projects, may it help you with your projects too. Tested on EU TTN (v2/v3).


## Features

* OTAA (only)
* Auto store/restore keys from nvram
* Support uplink and downlink
* Uplink port on send

## ToDO

* More LoRaWAN options
* Network re-join
* Class-C device support


# Example

See the `main.py` for a simple test device.


# Utils

## LoRa Erase

Erase all LoRa settings from nvram:

```python
from lorawan.utils import lora_erase
lora_erase()
```

## Device EUI

Get the Device EUI from your Pycom module:

```python
from lorawan.utils import get_device_eui
get_device_eui()
```

## Generate App Keys

Generate Application EUI and Application Key:

```python
from lorawan.utils import generate_keys
generate_keys()
```
