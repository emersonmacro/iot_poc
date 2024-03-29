from typing import Dict, List, Union

from models import Dwelling, Hub, Switch, Dimmer, Lock, Thermostat

dwelling_by_id: Dict[str, Dwelling] = dict()
dwellings: List[Dwelling] = list()

hub_by_id: Dict[str, Hub] = dict()
hubs = List[Hub] = list()

device_by_id: Dict[str, Union[Switch, Dimmer, Lock, Thermostat]] = dict()
devices = List[Union[Switch, Dimmer, Lock, Thermostat]] = list()
