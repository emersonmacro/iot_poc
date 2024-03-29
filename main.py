from datetime import datetime
from random import randint
from typing import Any, List, Union

from models import (
  DeviceType,
  Dimmer,
  Dwelling,
  Hub,
  Lock,
  Switch,
  Thermostat,
)
from datastore import (
  device_by_id,
  devices,
  dwelling_by_id,
  dwellings,
  hub_by_id,
  hubs,
)

# Dwelling Operations
def create_dwelling(address: str, is_occupied: bool) -> Dwelling:
  dwelling = Dwelling(address=address, is_occupied=is_occupied)
  dwelling_by_id[dwelling.id] = dwelling
  dwellings.append(dwelling)
  return dwelling

def dwelling_occupied(dwelling_id: str):
  dwelling = dwelling_by_id[dwelling_id]
  dwelling.is_occupied = True

def dwelling_vacant(dwelling_id: str):
  dwelling = dwelling_by_id[dwelling_id]
  dwelling.is_occupied = False

def install_hub(dwelling_id: str, hub_id: str):
  hub = hub_by_id[hub_id]
  hub.dwelling_id = dwelling_id

def list_dwellings() -> List[Dwelling]:
  return dwellings

# Hub Operations
def create_hub() -> Hub:
  hub = Hub()
  hub_by_id[hub.id] = hub
  hubs.append(hub)
  return hub

def pair_device(hub_id: str, device_id: str):
  device = device_by_id[device_id]
  device.hub_id = hub_id

def get_device_state(hub_id: str, device_id: str) -> Any:
  device = device_by_id[device_id]
  if device.hub_id != hub_id:
    raise Exception(f'ERROR: device {device_id} does not belong to hub {hub_id}')
  if device.device_type == DeviceType.SWITCH:
    return {'device_id': device.id, 'is_on': device.is_on}
  elif device.device_type == DeviceType.DIMMER:
    return {'device_id': device.id, 'light_level': device.light_level}
  elif device.device_type == DeviceType.LOCK:
    return {'device_id': device.id, 'is_locked': device.is_locked}
  elif device.device_type == DeviceType.THERMOSTAT:
    return {'device_id': device.id, 'temp': device.temp}
  else:
    raise Exception(f'ERROR: unrecognized device type {device.device_type}')

def list_devices(hub_id: str) -> List[Union[Switch, Dimmer, Lock, Thermostat]]:
  return [device for device in devices if device.hub_id == hub_id and device.del_stamp is None]

def remove_device(hub_id: str, device_id: str):
  device = device_by_id[device_id]
  if device.hub_id != hub_id:
    raise Exception(f'ERROR: device {device_id} does not belong to hub {hub_id}')
  device.hub_id = None

# Device Operations
def create_device(device_type: DeviceType) -> Union[Switch, Dimmer, Lock, Thermostat]:
  if device_type == DeviceType.SWITCH:
    device = Switch(is_on=False)
  elif device_type == DeviceType.DIMMER:
    device = Dimmer(light_level=0)
  elif device_type == DeviceType.LOCK:
    device = Lock(is_locked=False, pin=randint(1000,9999))
  elif device_type == DeviceType.THERMOSTAT:
    device = Thermostat(temp=70)
  else:
    raise Exception(f'ERROR: unrecognized device type {device_type}')
  device_by_id[device.id] = device
  devices.append(device)
  return device

def delete_device(device_id: str):
  device = device_by_id[device_id]
  if device.hub_id is not None:
    raise Exception(f'ERROR: device {device_id} is currently paired')
  device.del_stamp = datetime.now(datetime.timezone.utc)

def device_info(device_id: str) -> Union[Switch, Dimmer, Lock, Thermostat]:
  device = device_by_id[device_id]
  return device

def modify_device(device_id: str, **kwargs):
  device = device_by_id[device_id]
  if device.device_type == DeviceType.SWITCH:
    val = kwargs.get('is_on', False)
    device.is_on = val
  elif device.device_type == DeviceType.DIMMER:
    val = kwargs.get('light_level', 0)
    device.light_level = val
  elif device.device_type == DeviceType.LOCK:
    val = kwargs.get('is_locked', False)
    device.is_locked == DeviceType
  elif device.device_type == DeviceType.THERMOSTAT:
    val = kwargs.get('temp', 70)
    device.temp = val
  else:
    raise Exception(f'ERROR: unrecognized device type {device.device_type}')

def list_devices() -> List[Union[Switch, Dimmer, Lock, Thermostat]]:
  return devices





# TEST
def print_data():
  print('dwelling_by_id:')
  print(dwelling_by_id)
  print('dwellings:')
  print(dwellings)
d = create_dwelling('test', False)
print_data()
dwelling_occupied(d.id)
print_data()
