import time 

class DummyDevice:
    ### @param name - str
    ### @param door - dict with keys 'plane' (one of ['North', 'South', 'East', 'West', 'Top', 'Bottom']), 'state' ('open'|'closed') and 'move_time' (number)
    def __init__(self, name, door):
        self._name = name
        self._door = door
        print(f"Initialized {name}.")

    @property
    def name(self):
        return self._name

    @property
    def door(self):
        return self._door
    
    @property
    def door_state(self):
        return self._door['state']

    ### Setters
    @name.setter
    def set_name(self, new_name):
        self._name = new_name

    @door.setter
    def door(self, plane, state, delay):
        self._door = {
            'plane': plane, 
            'state': state,
            'move_time': delay,
        }
    
    ### @brief if door exists, set its state
    def set_door(self, attr, val):
        if type(self._door) is dict:
            self._door[attr] = val
            # if attr == "state":
            #     time.sleep(self.get_door()['delay'])
        else:
            print("Cannot change attribute: create a door first.")


class SimulatedSmartDevice(DummyDevice):
    ### @param action - str
    def __init__(self, name, door, action):
        super().__init__(name, door)
        self._action = action
        self._active = False

    ### @brief returns whether action ran successfully after opening the door
    def run_action(self, delay, **kwargs) -> bool: 
        if self._active is False:
            print(f"Running action {self._action}...")
            self._active = True
            time.sleep(delay)
        else:
            print(f"Error: cannot run action {self._action}, action already running.")
            return False

    ### @brief returns whether action stopped successfully after closing the door
    def stop_action(self, delay):
        if self._active is True:
            print(f"Stopping action {self._action}.")
            self._active = False
            time.sleep(delay)
            return True
        else:
            print(f"Error: cannot stop action {self._action}, action is not running.")
            return False

    @property
    def action(self):
        return self._action
    
    @property
    def active(self):
        return self._active

    ### Setters
    @action.setter
    def set_action(self, new_action):
        self._action = new_action


class Vial():
    ### @param volume - number (mL)
    ### @param temp - number (Celsius)
    ### @attr cap - bool
    # TODO: should we add attributes safe_vol, curr_vol, curr_substance, clean, etc.?
    def __init__(self, max_vol, temp):
        self._max_vol = max_vol
        self._temp = temp
        self._cap = False

    def cap_vial(self):
        self._cap = True

    def decap_vial(self):
        self._cap = False

    # TODO: should max_vol have a setter?
    @property
    def max_vol(self):
        return self._max_vol

    @property
    def temp(self):
        return self._temp
    
    @property
    def cap(self):
        return self._cap

    ### Setters
    @temp.setter
    def change_temp(self, temp):
        self._temp = temp

    @cap.setter
    def cap(self, cap):
        self._cap = cap


class SimulatedTowerOfHanoi(DummyDevice):
    def __init__(self, name, door, max_rings):
        super(SimulatedTowerOfHanoi, self).__init__(name, door)
        self.max_rings = max_rings
        self.num_rings = 0
        self.rings = None

    def get_ring(self, key):
        if self.rings is not None:
            if key in self.rings.keys():
                return (key, self.rings[key])
        print(f"Ring with key {key} does not exist in Rings.")
    
    def move_ring(self, robot, from_tower, to_tower):
        # Move to the start position and pick up ring
        robot.arm.set_joint_positions(joint_positions=from_tower.get('approach'), moving_time=3, accel_time=None, blocking=True)
        time.sleep(1)
        robot.arm.set_joint_positions(joint_positions=from_tower.get('pickup'), moving_time=3, accel_time=None, blocking=True)
        time.sleep(1)
        robot.gripper.close(delay=2)
        robot.arm.set_joint_positions(joint_positions=from_tower.get('pickup_safe_height'), moving_time=1, accel_time=None, blocking=True)
        time.sleep(1)
        
        # Move to the end position and place ring
        robot.arm.set_joint_positions(joint_positions=to_tower.get('pickup_safe_height'), moving_time=3, accel_time=None, blocking=True)
        time.sleep(1)
        robot.arm.set_joint_positions(joint_positions=to_tower.get('pickup'), moving_time=1, accel_time=None, blocking=True)
        time.sleep(1)
        robot.gripper.open(delay=2)
        robot.arm.set_joint_positions(joint_positions=to_tower.get('approach'), moving_time=3, accel_time=None, blocking=True)


    # TODO: stack??
    def add_ring(self, key, val):
        if self.num_rings < self.max_rings:
            if self.rings is None:
                self.rings = {}
            if key not in self.rings.keys():
                self.rings[key] = val
                self.update_rings()
                print(f"Ring added to {self.get_name()} successfully.")

            else:
                "Error: existing key found."
        else:
            print("Maximum number of rings already added.")

    def remove_ring(self, key):
        if self.rings is not None:
            print(f"Removing a ring from {self.get_name()}...")
            self.rings.pop(key)
            self.update_rings()
        else:
            print("Cannot remove a ring from an empty ring set.")

    def update_rings(self):
        self.num_rings = len(self.rings)

    ### Setters

    def set_max_rings(self, num):
        self.max_rings = num

    # Replaces Rings with entirely new set of Rings
    def set_rings(self, rings):
        if len(rings) > self.max_rings:
            print("Error: max number of rings reached.")
            return False
        else:
            self.rings = rings
            self.num_rings = len(self.rings)
            print(f"Rings added to {self.get_name()} successfully.")
            return True
 
    ### Getters

    def get_max_rings(self):
        return self.max_rings

    def get_num_rings(self):
        if self.rings is None:
            return 0
        return len(self.rings)
    
    def get_rings(self):
        return self.rings
