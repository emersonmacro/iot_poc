from datetime import datetime
from enum import Enum
from typing import Union
from uuid import uuid4

from pydantic import BaseModel

class Dwelling(BaseModel):
  id: uuid4
  address: str
  is_occupied: bool

class Hub(BaseModel):
  id: uuid4
  dwelling_id: str

class DeviceType(Enum):
  SWITCH = 1
  DIMMER = 2
  LOCK = 3
  THERMOSTAT = 4

class Device(BaseModel):
  id: uuid4
  device_type: DeviceType
  del_stamp: Union[datetime, None] = None

class Switch(Device):
  is_on: bool

class Dimmer(Device):
  light_level: int

class Lock(Device):
  is_locked: bool
  pin: int

class Thermostat(Device):
  temp: int
