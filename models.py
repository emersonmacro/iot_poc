from datetime import datetime
from enum import Enum
from typing import Union
from uuid import uuid4

from pydantic import BaseModel, Field

# Assumptions:
# - A Hub can belong to one and only one Dwelling
# - A Device can belong to one and only one Hub
# - Lock pin will be a random 4-digit number

class Dwelling(BaseModel):
  id: str = Field(default_factory=lambda: str(uuid4()))
  address: str
  is_occupied: bool

class Hub(BaseModel):
  id: str = Field(default_factory=lambda: str(uuid4()))
  dwelling_id: Union[str, None] = None

class DeviceType(Enum):
  SWITCH = 1
  DIMMER = 2
  LOCK = 3
  THERMOSTAT = 4

class Device(BaseModel):
  id: str = Field(default_factory=lambda: str(uuid4()))
  hub_id: Union[str, None] = None
  device_type: DeviceType
  del_stamp: Union[datetime, None] = None

class Switch(Device):
  device_type: DeviceType = DeviceType.SWITCH
  is_on: bool

class Dimmer(Device):
  device_type: DeviceType = DeviceType.DIMMER
  light_level: int = Field(ge=0, le=100)

class Lock(Device):
  device_type: DeviceType = DeviceType.LOCK
  is_locked: bool
  pin: int

class Thermostat(Device):
  device_type: DeviceType = DeviceType.THERMOSTAT
  temp: int = Field(ge=50, le=90)
