from typing import Dict, List, TypedDict, Union

from models import Dwelling, Hub, Switch, Dimmer, Lock, Thermostat

class Datastores(TypedDict):
  dwelling_by_id: Dict[str, Dwelling]
  dwellings: List[Dwelling]
  hub_by_id: Dict[str, Hub]
  hubs = List[Hub]
  device_by_id: Dict[str, Union[Switch, Dimmer, Lock, Thermostat]]
  devices = List[Union[Switch, Dimmer, Lock, Thermostat]]

def initialize_datastores() -> Datastores:
  dwelling_by_id: Dict[str, Dwelling] = dict()
  dwellings: List[Dwelling] = list()

  hub_by_id: Dict[str, Hub] = dict()
  hubs = List[Hub] = list()

  device_by_id: Dict[str, Union[Switch, Dimmer, Lock, Thermostat]] = dict()
  devices = List[Union[Switch, Dimmer, Lock, Thermostat]] = list()

  datastores: Datastores = Datastores(
    dwelling_by_id=dwelling_by_id,
    dwellings=dwellings,
    hub_by_id=hub_by_id,
    hubs=hubs,
    device_by_id=device_by_id,
    devices=devices,
  )

  return datastores
