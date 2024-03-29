from typing import Any, Union

from models import (
  DeviceType,
  Dimmer,
  Lock,
  Switch,
  Thermostat,
)

def current_device_state(device: Union[Switch, Dimmer, Lock, Thermostat]) -> Any:
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
