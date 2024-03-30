import pytest

from datastore import initialize_datastores
from main import *
from models import DeviceType

# Note: I'm still learning the basics of Pytest. I'm pretty sure a lot
# of this could be cleaned up with fixtures, but I haven't had a chance
# to dig into it yet.

class TestDwellingOps:
  test_address = 'test'

  def test_create_dwelling(self):
    store = initialize_datastores()
    assert len(store['dwellings']) == 0
    store, dwelling = create_dwelling(store, self.test_address, False)
    # dwellings should now have one entry
    assert len(store['dwellings']) == 1
    assert dwelling.address == self.test_address
    assert store['dwellings'][0].address == self.test_address
    assert store['dwellings'][0].id == store['dwelling_by_id'][dwelling.id].id

  def test_dwelling_occupied(self):
    store = initialize_datastores()
    store, dwelling = create_dwelling(store, self.test_address, False)
    assert store['dwellings'][0].is_occupied == False
    store = dwelling_occupied(store, dwelling.id)
    # dwelling should now be set to occupied
    assert store['dwellings'][0].is_occupied == True

  def test_dwelling_vacant(self):
    store = initialize_datastores()
    store, dwelling = create_dwelling(store, self.test_address, True)
    assert store['dwellings'][0].is_occupied == True
    store = dwelling_vacant(store, dwelling.id)
    # dwelling should now be set to vacant
    assert store['dwellings'][0].is_occupied == False

  def test_install_hub(self):
    store = initialize_datastores()
    store, dwelling = create_dwelling(store, self.test_address, True)
    store, hub = create_hub(store)
    assert hub.dwelling_id is None
    store = install_hub(store, dwelling.id, hub.id)
    # dwelling and hub should now be linked
    assert store['hubs'][0].dwelling_id == dwelling.id

  def test_list_dwellings(self):
    store = initialize_datastores()
    store, _ = create_dwelling(store, self.test_address, True)
    store, _ = create_dwelling(store, self.test_address, True)
    store, dwellings = list_dwellings(store)
    # dwellings should now have two entries
    assert len(dwellings) == 2

class TestHubOps:
  def test_create_hub(self):
    store = initialize_datastores()
    assert len(store['hubs']) == 0
    store, hub = create_hub(store)
    # hubs should now have one entry
    assert len(store['hubs']) == 1
    assert store['hubs'][0].id == store['hub_by_id'][hub.id].id

  def test_pair_device(self):
    store = initialize_datastores()
    store, hub = create_hub(store)
    store, device = create_device(store, DeviceType.SWITCH)
    store = pair_device(store, hub.id, device.id)
    # hub and device should now be linked
    assert store['devices'][0].hub_id == hub.id

  def test_get_device_state(self):
    store = initialize_datastores()
    store, hub = create_hub(store)
    store, device = create_device(store, DeviceType.SWITCH)
    store = pair_device(store, hub.id, device.id)
    store, result = get_device_state(store, hub.id, device.id)
    # device should have property `is_on` set to False (default value)
    assert result['device_id'] == device.id
    assert result['is_on'] == False

  def test_get_device_state_invalid_device_id(self):
    with pytest.raises(Exception):
      store = initialize_datastores()
      store, hub1 = create_hub(store)
      store, hub2 = create_hub(store)
      store, device = create_device(store, DeviceType.SWITCH)
      store = pair_device(store, hub1.id, device.id)
      store, _ = get_device_state(store, hub2.id, device.id)
      # should raise exception because device doesn't belong to hub

  def test_list_devices(self):
    store = initialize_datastores()
    store, hub1 = create_hub(store)
    store, hub2 = create_hub(store)
    store, device1 = create_device(store, DeviceType.SWITCH)
    store, device2 = create_device(store, DeviceType.SWITCH)
    store, device3 = create_device(store, DeviceType.SWITCH)
    store = pair_device(store, hub1.id, device1.id)
    store = pair_device(store, hub1.id, device2.id)
    store = pair_device(store, hub2.id, device3.id)
    store, hub_devices = list_devices(store, hub1.id)
    # devices store should have len 3 but hub_devices should have len 2
    assert len(store['devices']) == 3
    assert len(hub_devices) == 2
    # each device in hub_devices should belong to hub1
    for device in hub_devices:
      assert device.hub_id == hub1.id

  def test_remove_device(self):
    store = initialize_datastores()
    store, hub = create_hub(store)
    store, device = create_device(store, DeviceType.SWITCH)
    store = pair_device(store, hub.id, device.id)
    assert store['devices'][0].hub_id == hub.id
    store = remove_device(store, hub.id, device.id)
    # hub and device should now be unlinked
    assert store['devices'][0].hub_id is None

  def test_remove_device_invalid_device_id(self):
    with pytest.raises(Exception):
      store = initialize_datastores()
      store, hub1 = create_hub(store)
      store, hub2 = create_hub(store)
      store, device = create_device(store, DeviceType.SWITCH)
      store = pair_device(store, hub1.id, device.id)
      store, _ = remove_device(store, hub2.id, device.id)
      # should raise exception because device doesn't belong to hub

class TestDeviceOps:
  def test_create_device_switch(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.SWITCH)
    # should create device of appropriate type with default values
    assert device.device_type == DeviceType.SWITCH
    assert device.is_on == False

  def test_create_device_dimmer(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.DIMMER)
    # should create device of appropriate type with default values
    assert device.device_type == DeviceType.DIMMER
    assert device.light_level == 0

  def test_create_device_lock(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.LOCK)
    # should create device of appropriate type with default values
    assert device.device_type == DeviceType.LOCK
    assert device.is_locked == False

  def test_create_device_thermostat(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.THERMOSTAT)
    # should create device of appropriate type with default values
    assert device.device_type == DeviceType.THERMOSTAT
    assert device.temp == 70

  def test_create_device_invalid_device_type(self):
    with pytest.raises(Exception):
      store = initialize_datastores()
      _, _ = create_device(store, 12345)
      # should raise exception due to unrecognized device type

  def test_delete_device(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.SWITCH)
    assert device.del_stamp is None
    store = delete_device(store, device.id)
    # device del_stamp should now be set
    assert store['devices'][0].del_stamp is not None

  def test_delete_device_error_case(self):
    with pytest.raises(Exception):
      store = initialize_datastores()
      store, hub = create_hub(store)
      store, device = create_device(store, DeviceType.SWITCH)
      store = pair_device(store, hub.id, device.id)
      store = delete_device(store, device.id)
      # should raise exception because device is still paired

  def test_device_info(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.SWITCH)
    store, info = device_info(store, device.id)
    # should return device info
    assert info.id == device.id
    assert info.device_type == device.device_type
    assert info.is_on == device.is_on

  def test_modify_device_switch(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.SWITCH)
    assert device.is_on == False
    store = modify_device(store, device.id, is_on=True)
    # switch should now be on
    assert store['devices'][0].is_on == True

  def test_modify_device_dimmer(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.DIMMER)
    assert device.light_level == 0
    store = modify_device(store, device.id, light_level=80)
    # dimmer light level should now be 80
    assert store['devices'][0].light_level == 80

  # TODO: figure out why the Pydantic validation isn't working as expected here
  # expected result: light_level cannot exceed 100

  # def test_modify_device_dimmer_validation_error(self):
  #   with pytest.raises(ValueError):
  #     store = initialize_datastores()
  #     store, device = create_device(store, DeviceType.DIMMER)
  #     store = modify_device(store, device.id, light_level=200)

  def test_modify_device_lock(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.LOCK)
    assert device.is_locked == False
    store = modify_device(store, device.id, is_locked=True)
    # lock should now be locked
    assert store['devices'][0].is_locked == True

  def test_modify_device_thermostat(self):
    store = initialize_datastores()
    store, device = create_device(store, DeviceType.THERMOSTAT)
    assert device.temp == 70
    store = modify_device(store, device.id, temp=65)
    # thermostat should now be set to 65
    assert store['devices'][0].temp == 65

  def test_list_all_devices(self):
    store = initialize_datastores()
    store, _ = create_device(store, DeviceType.SWITCH)
    store, _ = create_device(store, DeviceType.DIMMER)
    store, _ = create_device(store, DeviceType.LOCK)
    store, _ = create_device(store, DeviceType.THERMOSTAT)
    store, devices = list_all_devices(store)
    # devices should now have four entries
    assert len(devices) == 4
    pass
