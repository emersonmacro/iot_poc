from datetime import datetime
from random import randint
from typing import Any, List, Tuple, Union

from datastore import Datastores
from models import (
  DeviceType,
  Dimmer,
  Dwelling,
  Hub,
  Lock,
  Switch,
  Thermostat,
)

# Dwelling Operations
def create_dwelling(datastores: Datastores, address: str, is_occupied: bool) -> Tuple[Datastores, Dwelling]:
  dwelling = Dwelling(address=address, is_occupied=is_occupied)
  datastores['dwelling_by_id'][dwelling.id] = dwelling
  datastores['dwellings'].append(dwelling)
  return datastores, dwelling

def dwelling_occupied(datastores: Datastores, dwelling_id: str) -> Datastores:
  dwelling = datastores['dwelling_by_id'][dwelling_id]
  dwelling.is_occupied = True
  return datastores

def dwelling_vacant(datastores: Datastores, dwelling_id: str) -> Datastores:
  dwelling = datastores['dwelling_by_id'][dwelling_id]
  dwelling.is_occupied = False
  return datastores

def install_hub(datastores: Datastores, dwelling_id: str, hub_id: str) -> Datastores:
  hub = datastores['hub_by_id'][hub_id]
  hub.dwelling_id = dwelling_id
  return datastores

def list_dwellings(datastores: Datastores) -> Tuple[Datastores, List[Dwelling]]:
  return datastores, datastores['dwellings']

# Hub Operations
def create_hub(datastores: Datastores) -> Tuple[Datastores, Hub]:
  hub = Hub()
  datastores['hub_by_id'][hub.id] = hub
  datastores['hubs'].append(hub)
  return datastores, hub

def pair_device(datastores: Datastores, hub_id: str, device_id: str) -> Datastores:
  device = datastores['device_by_id'][device_id]
  # TODO: handle device-not-found case
  device.hub_id = hub_id
  return datastores

def get_device_state(datastores: Datastores, hub_id: str, device_id: str) -> Tuple[Datastores, Any]:
  device = datastores['device_by_id'][device_id]
  # TODO: handle device-not-found case
  if device.hub_id != hub_id:
    raise Exception(f'ERROR: device {device_id} does not belong to hub {hub_id}')
  if device.device_type == DeviceType.SWITCH:
    return datastores, {'device_id': device.id, 'is_on': device.is_on}
  elif device.device_type == DeviceType.DIMMER:
    return datastores, {'device_id': device.id, 'light_level': device.light_level}
  elif device.device_type == DeviceType.LOCK:
    return datastores, {'device_id': device.id, 'is_locked': device.is_locked}
  elif device.device_type == DeviceType.THERMOSTAT:
    return datastores, {'device_id': device.id, 'temp': device.temp}
  else:
    raise Exception(f'ERROR: unrecognized device type {device.device_type}')

def list_devices(datastores: Datastores, hub_id: str) -> Tuple[Datastores, List[Union[Switch, Dimmer, Lock, Thermostat]]]:
  hub_devices = [device for device in datastores['devices'] if device.hub_id == hub_id and device.del_stamp is None]
  return datastores, hub_devices

def remove_device(datastores: Datastores, hub_id: str, device_id: str) -> Datastores:
  device = datastores['device_by_id'][device_id]
  # TODO: handle device-not-found case
  if device.hub_id != hub_id:
    raise Exception(f'ERROR: device {device_id} does not belong to hub {hub_id}')
  device.hub_id = None
  return datastores

# Device Operations
def create_device(datastores: Datastores, device_type: DeviceType) -> Tuple[Datastores, Union[Switch, Dimmer, Lock, Thermostat]]:
  if device_type == DeviceType.SWITCH:
    device = Switch(is_on=False)
  elif device_type == DeviceType.DIMMER:
    device = Dimmer(light_level=0)
  elif device_type == DeviceType.LOCK:
    # TODO: remove pin from response for security purposes
    device = Lock(is_locked=False, pin=randint(1000,9999))
  elif device_type == DeviceType.THERMOSTAT:
    device = Thermostat(temp=70)
  else:
    raise Exception(f'ERROR: unrecognized device type {device_type}')
  datastores['device_by_id'][device.id] = device
  datastores['devices'].append(device)
  return datastores, device

def delete_device(datastores: Datastores, device_id: str) -> Datastores:
  device = datastores['device_by_id'][device_id]
  if device.hub_id is not None:
    raise Exception(f'ERROR: device {device_id} is currently paired')
  device.del_stamp = datetime.now()
  return datastores

def device_info(datastores: Datastores, device_id: str) -> Tuple[Datastores, Union[Switch, Dimmer, Lock, Thermostat]]:
  device = datastores['device_by_id'][device_id]
  return datastores, device

def modify_device(datastores: Datastores, device_id: str, **kwargs) -> Datastores:
  device = datastores['device_by_id'][device_id]
  if device.device_type == DeviceType.SWITCH:
    val = kwargs.get('is_on', False)
    device.is_on = val
  elif device.device_type == DeviceType.DIMMER:
    val = kwargs.get('light_level', 0)
    device.light_level = val
  elif device.device_type == DeviceType.LOCK:
    val = kwargs.get('is_locked', False)
    device.is_locked = val
  elif device.device_type == DeviceType.THERMOSTAT:
    val = kwargs.get('temp', 70)
    device.temp = val
  else:
    raise Exception(f'ERROR: unrecognized device type {device.device_type}')
  return datastores

def list_all_devices(datastores: Datastores) -> Tuple[Datastores, List[Union[Switch, Dimmer, Lock, Thermostat]]]:
  return datastores, datastores['devices']
