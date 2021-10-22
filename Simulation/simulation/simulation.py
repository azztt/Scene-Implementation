# This is the main simulation file, having a separate mqqt client
# to manage the simulation via the interface provided. This has direct
# connection to the golang server for managing (adding, deleting, etc)
# rooms, devices, and controllers.

# importing types
from typing import Any, Dict, Tuple

# importing os utilities
# import 

# importing all devices
from devices import AirConditioner
from devices import ColorLight
from devices import DoorLock
from devices import Fan
from devices import Light

# importing all controllers
from controllers import ACController
from controllers import ColorLightController
from controllers import DoorLockController
from controllers import FanController
from controllers import LightController

# importing room
from base_classes import Controller, Device, Room

# importing utilities
import utilities as utils

# simulation utilities
from sim_utils import *
from sim_constants import *

# importing mqtt client
import paho.mqtt.client as mqtt

# importing pickle to load and write latest configuration
import pickle

# list of all entities
rooms: Dict[str, Room] = {}
devices: Dict[str, Device] = {}
controllers: Dict[str, Controller] = {}

# initializing id generator for this simulation
id_gen = utils.IDClass()

"""
MQTT COMMUNICATION SPEC FOR SIMULATION

SUBSCRIBED COMMUNICATIONS:
1)
    topic: `simulation/new_room`
    message: `room_name`
    Description: Create a new room object with given name

2)
    topic: `simulation/rem_room`
    message: `room_id`
    Description: Remove the room object with given id

3)
    topic: `simulation/new_device`
    message: `device_type/device_name/other_keyword_parameters`
    Description: Create a new device object of given type with given parameters

4)
    topic: `simulation/rem_device`
    message: `device_id`
    Description: Removes the device object of given id

PUBLISHING COMMUNICATIONS:
1)
    topic: `simulation/device_status`
    message: `device_id/status_string`
    Description: Cron job publishing device status
"""

# simulation meta data
SIM_ID = id_gen.new_id()

# methods to load and write latest configuration files
def load_configuration() -> str:
    global rooms, devices, controllers
    simulation = None

    try:
        with open(CONFIG, 'rb') as config_file:
            simulation = pickle.load(config_file)
    except OSError:
        return "No previous configuration"
    if simulation:
        rooms = simulation["rooms"]
        devices = simulation["devices"]
        controllers = simulation["controllers"]
    return None

def save_configuration() -> str:
    global rooms, devices, controllers
    simulation = {}
    simulation["rooms"] = rooms
    simulation["devices"] = devices
    simulation["controllers"] = controllers
    try:
        with open(CONFIG, 'wb') as config_file:
            simulation = pickle.dump(simulation, config_file)
    except OSError:
        return "Unknown error"
    else:
        return None

# callbacks for the mqtt client
def on_connect(
    client: mqtt.Client,
    userdata: Any,
    flags: Any,
    rc: Any) -> None:
    print("Simulation connected to network with result code {}".format(rc))

    # publishing for presence
    client.publish(
        topic=PRES_TOPIC,
        payload="{}".format(SIM_ID),
        qos=2   
    )

def on_subscribe(
    client: mqtt.Client,
    userdata: Any,
    mid: Any,
    granted_qos: int) -> None:
    print("Simulation subscribed to topic successfully")

# callback for new room
def new_room(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    new_room_id = id_gen.new_id()
    msg = str(message.payload.decode('utf-8'))
    room_name = msg

    new_room = Room(
        name=room_name,
        id=new_room_id
    )

    rooms[new_room_id] = new_room
    sim_acknowledge(
        client=client,
        topic=NEW_ROOM,
        status=utils.OPStatus.SUCCESS.value
    )

# callback for removing room
def rem_room(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    room_id = str(message.payload.decode('utf-8'))

    room = rooms.get(room_id)
    err = room.empty_room()
    if err:
        sim_acknowledge(
            client=client,
            topic=REM_ROOM,
            status=utils.OPStatus.FAILED.value
        )
    else:
        sim_acknowledge(
            client=client,
            topic=REM_ROOM,
            status=utils.OPStatus.SUCCESS.value
        )
    rooms.pop(room_id, None)

# callback for new device
def new_device(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    new_dev_id = id_gen.new_id()
    msg = str(message.payload.decode('utf-8'))
    msg = json.loads(msg)
    # msg = msg.split("/")
    room_id = msg["room_id"]
    room = rooms.get(room_id)
    if not room:
        sim_acknowledge(
            client=client,
            topic=NEW_DEVICE,
            status=utils.OPStatus.FAILED.value
        )
        return
    device_type = msg["type"]
    device_name = msg["name"]

    if device_type == utils.DeviceType.AC.value:
        temp_range: str = msg["temp_range"]
        temp_range = temp_range[1:-1]
        temp_lim = temp_range.split(",")
        temp_range = tuple(list(map(int, temp_lim)))
        new_ac = AirConditioner(
            name=device_name,
            id=new_dev_id,
            temp_range=temp_range
        )
        err = room.add_device(new_ac)
        if err == utils.Error.NO_CONT.value:
            new_cont_id = id_gen.new_id()
            ac_cont = ACController(
                name="Controller {}".format(len(controllers)+1),
                id=new_cont_id
            )
            controllers[new_cont_id] = ac_cont
            err = room.add_controller(ac_cont)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
            err = room.add_device(new_ac)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
        elif err:
            sim_acknowledge(
                client=client,
                topic=NEW_DEVICE,
                status=utils.OPStatus.FAILED.value
            )
            return
        
        devices[new_dev_id] = new_ac
    
    elif device_type == utils.DeviceType.COL_LIGHT.value:
        color: str = msg["color"]
        if color:
            color = color[1:-1]
            color = color.split(",")
            color = tuple(list(map(int, color)))
        
        b_levels = int(msg["b_levels"])
        new_clight = ColorLight(
            name=device_name,
            id=new_dev_id,
            color=color,
            brightness_levels=b_levels
        )
        err = room.add_device(new_clight)
        if err == utils.Error.NO_CONT.value:
            new_cont_id = id_gen.new_id()
            clight_cont = ColorLightController(
                name="Controller {}".format(len(controllers)+1),
                id=new_cont_id
            )
            controllers[new_cont_id] = clight_cont
            err = room.add_controller(clight_cont)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
            err = room.add_device(new_clight)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
        elif err:
            sim_acknowledge(
                client=client,
                topic=NEW_DEVICE,
                status=utils.OPStatus.FAILED.value
            )
            return
        
        devices[new_dev_id] = new_clight
    
    elif device_type == utils.DeviceType.DOOR_LOCK.value:
        new_dlock = DoorLock(
            name=device_name,
            id=new_dev_id,
        )
        err = room.add_device(new_dlock)
        if err == utils.Error.NO_CONT.value:
            new_cont_id = id_gen.new_id()
            dlock_cont = DoorLockController(
                name="Controller {}".format(len(controllers)+1),
                id=new_cont_id
            )
            controllers[new_cont_id] = dlock_cont
            err = room.add_controller(dlock_cont)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
            err = room.add_device(new_dlock)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
        elif err:
            sim_acknowledge(
                client=client,
                topic=NEW_DEVICE,
                status=utils.OPStatus.FAILED.value
            )
            return
        
        devices[new_dev_id] = new_dlock
    
    elif device_type == utils.DeviceType.FAN.value:
        speed_levels = int(msg["speed_levels"])
        new_fan = Fan(
            name=device_name,
            id=new_dev_id,
            speed_levels=speed_levels
        )
        err = room.add_device(new_fan)
        if err == utils.Error.NO_CONT.value:
            new_cont_id = id_gen.new_id()
            fan_cont = FanController(
                name="Controller {}".format(len(controllers)+1),
                id=new_cont_id
            )
            controllers[new_cont_id] = fan_cont
            err = room.add_controller(fan_cont)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
            err = room.add_device(new_fan)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
        elif err:
            sim_acknowledge(
                client=client,
                topic=NEW_DEVICE,
                status=utils.OPStatus.FAILED.value
            )
            return
        
        devices[new_dev_id] = new_fan

    elif device_type == utils.DeviceType.LIGHT.value:
        b_levels = int(msg["b_levels"])
        new_light = Light(
            name=device_name,
            id=new_dev_id,
            brightness_levels=b_levels
        )
        err = room.add_device(new_light)
        if err == utils.Error.NO_CONT.value:
            new_cont_id = id_gen.new_id()
            light_cont = LightController(
                name="Controller {}".format(len(controllers)+1),
                id=new_cont_id
            )
            controllers[new_cont_id] = light_cont
            err = room.add_controller(light_cont)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
            err = room.add_device(new_light)
            if err:
                sim_acknowledge(
                    client=client,
                    topic=NEW_DEVICE,
                    status=utils.OPStatus.FAILED.value
                )
                return
        elif err:
            sim_acknowledge(
                client=client,
                topic=NEW_DEVICE,
                status=utils.OPStatus.FAILED.value
            )
            return
        
        devices[new_dev_id] = new_light

    sim_acknowledge(
        client=client,
        topic=NEW_DEVICE,
        status=utils.OPStatus.SUCCESS.value
    )

# callback for removing device
def rem_device(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    dev_id = str(message.payload.decode('utf-8'))
    device = devices.get(dev_id, None)
    if not device:
        sim_acknowledge(
            client=client,
            topic=NEW_DEVICE,
            status=utils.OPStatus.FAILED.value
        )
        return
    
    room = device.get_room()
    err = room.remove_device_by_id_type(
        device_id=dev_id,
        type=device.get_device_type()
    )
    if err:
        sim_acknowledge(
            client=client,
            topic=NEW_DEVICE,
            status=utils.OPStatus.FAILED.value
        )
        return
    else:
        sim_acknowledge(
            client=client,
            topic=NEW_DEVICE,
            status=utils.OPStatus.SUCCESS.value
        )

start_success = False
# callback for starting the simulation
def start_sim(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    global start_success
    if message.topic == START_SIM:
        client.unsubscribe(topic=START_SIM)
        # loading latest configuration if available
        config = load_configuration()
        if not config:
            # if loaded, start all the controllers
            for (_, controller) in controllers.items():
                err = controller.start()
                if err:
                    start_success = False
                    return
                
        # if all controllers started successfully
        start_success = True

        client.subscribe(topic=STOP_SIM)

stop_success = False
# callback for stopping the simulation
def stop_sim(client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
    global stop_success
    if message.topic == STOP_SIM:
        client.unsubscribe(topic=STOP_SIM)

        # stop all controllers first
        for (_, controller) in controllers.items():
            err = controller.stop()
            if err:
                stop_success = False
                return

        # writing latest configuration to file
        config = save_configuration()
        if not config:
            # if saved
            stop_success = True

        client.subscribe(topic=START_SIM)


# setting up and running mqtt simulation client
sim_client = mqtt.Client(
    client_id=SIM_ID,
    clean_session=False
)

try:
    sim_client.on_connect = on_connect
    sim_client.on_subscribe = on_subscribe
    sim_client.message_callback_add(NEW_ROOM, new_room)
    sim_client.message_callback_add(REM_ROOM, rem_room)
    sim_client.message_callback_add(NEW_DEVICE, new_device)
    sim_client.message_callback_add(REM_DEVICE, rem_device)
    sim_client.message_callback_add(START_SIM, start_sim)
    sim_client.message_callback_add(STOP_SIM, stop_sim)

    # getting the simulation connected to network
    sim_client.connect(
        host=utils.MQTT_SERVER,
        port=utils.MQTT_PORT
    )

    # waiting for start command for the simulation to get running
    sim_client.subscribe(
        topic=START_SIM,
        qos=2
    )

    # subscribe to all topics
    sim_client.subscribe(NEW_ROOM, 1)
    sim_client.subscribe(REM_ROOM, 1)
    sim_client.subscribe(NEW_DEVICE, 1)
    sim_client.subscribe(REM_DEVICE, 1)


    # start the loop of listening
    sim_client.loop_start()

except KeyboardInterrupt:
    # stop and disconnect the client from listening
    sim_client.unsubscribe(NEW_ROOM)
    sim_client.unsubscribe(REM_ROOM)
    sim_client.unsubscribe(NEW_DEVICE)
    sim_client.unsubscribe(REM_DEVICE)
    sim_client.loop_stop()
    sim_client.disconnect()

    # stop the controllers
    for (_, controller) in controllers.items():
        err = controller.stop()
    
    # save configuration
    config = save_configuration()
    print("Simulation stopped after saving configuration")
