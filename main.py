import random
import socket
import threading
import time
import json
import math

import body as bd
import utils
from body import Body, BodyType
import utils as ut
import mathutils
import terrain
import matplotlib.pyplot as plt

BODIES = bd.initBodies()

# list of existing phases:
# exploring
# lf_target
# shooting
# back_to_base
# reload

ROBOTS = {"bertha": {"id": 71, "phase": "exploring", "shots_per_reload": 1, "remaining_bullets": 1, "next_phase": "exploring"}}


def get_body_infos(id: int):
    for body in BODIES:
        if body.getID() == id:
            return body

    return None


def deduce_bot_position(data, cam_offset=[0, 0, 0], cam_rot=[0, 0]):
    """cam_rot = [pitch, roll]"""
    for marker in data["markers"]:

        if 21 <= marker["id"] <= 36:  # find fixed markers
            # info = [marker["x"], marker["y"], marker["z"], marker["pitch"], marker["yaw"], marker["roll"]]

            for elm in BODIES:
                if elm.getID() == marker["id"]:
                    ## coords corection
                    marker["x"] *= -1
                    marker["y"] *= -1
                    marker["pitch"] *= -1

                    dist3D = mathutils.distance3D(marker["x"], marker["y"], marker["z"])
                    dist2D = dist3D * math.cos(math.radians(cam_rot[1]))

                    pos_offset = [elm.getPos(), 0]

                    pos_offset[1] = utils.angle_bound(marker["pitch"] - 180 + elm.getRot())

                    pos_offset[0][0] += dist2D * math.sin(math.radians(pos_offset[1] - 180))
                    pos_offset[0][2] += dist2D * math.cos(math.radians(pos_offset[1] - 180))

                    return pos_offset

        return None

def deduce_marker_position(data, self_body):
    return [[0, 0, 0], 0]




def update_bodies(data, self_body, cam_offset=[0, 0, 0], cam_rot=[0, 0]):
    for marker in data["markers"]:
        if 1 <= marker["id"] <= 15:  # find targets
            temp = deduce_marker_position(data, self_body)
            found = False
            for elm in BODIES:
                if elm.getID() == marker["id"]:
                    elm.update([temp[0][0], temp[0][1], temp[0][2]], temp[1])
                    break
            if not found:
                BODIES.append(Body(marker["id"], [temp[0][0], temp[0][1], temp[0][2]], temp[1], BodyType.TARGET))





def bertha_ai(data):
    # change phase if needed
    if (ROBOTS["bertha"]["next_phase"] != ROBOTS["bertha"]["phase"]):
        ROBOTS["bertha"]["phase"] = ROBOTS["bertha"]["next_phase"]

        print("Phase changed to", ROBOTS["bertha"]["phase"])


    # future request to the client
    request = json.loads("{'req':[]}")
    req = []

    # determine pos if possible
    new_pos = deduce_bot_position(data, cam_rot=[0, 0])
    if new_pos is not None:
        print("New coords!", new_pos)
        found = False
        for body in BODIES:
            if body.id == 71:
                body.update(new_pos[0], new_pos[1])
                found = True
                break

        if not found:
            BODIES.append(Body(71, new_pos[0], new_pos[1], BodyType.CONNECTED_BODY))


    # update bodies (auto exploration)
    self = get_body_infos(71)
    update_bodies(data, self)


    # --- AI ---


    if ROBOTS["bertha"]["phase"] == "exploring":
        pass
    elif ROBOTS["bertha"]["phase"] == "lf_target":
        # find the closest target
        closest_target = None
        for body in BODIES:
            if body.getType() == BodyType.TARGET:
                if closest_target is None:
                    closest_target = body
                else:
                    if mathutils.distance2D(body.get2DPos()[0], body.get2DPos()[1]) < mathutils.distance2D(
                            body.get2DPos()[0], body.get2DPos()[1]):
                        closest_target = body

        # find the right rotation to face the target (in degrees), 10 degrees of freedom
        if closest_target is not None:
            req.append({"type": "rotate", "value": 0.3})

    elif ROBOTS["bertha"]["phase"] == "shooting":
        req.append({"type": "shoot", "value": 1})
    elif ROBOTS["bertha"]["phase"] == "back_to_base":
        pass


    request["req"] = req
    return json.dumps(request)


class ClientConn(threading.Thread):
    def __init__(self, conn, connAddr):
        threading.Thread.__init__(self)
        self.client_socket = conn
        self.client_address = connAddr

    def run(self):
        data = self.client_socket.recv(1024)  # Receive data from the client
        data = data.decode("utf-8")

        print('[{}]'.format(ut.get_time_str()), '{}'.format(data))

        # --- Process data ---

        # --- Send data back to the client ---
        self.client_socket.sendall(self.process_data(data).encode('utf-8'))

        self.client_socket.close()

    def process_data(self, data) -> str:  # will send back the request to send to the client
        data = json.loads(data)

        if data["sender"] == "esieabot-bcc6b4":
            return bertha_ai(data)

        return ""


# --- Server waiting for connection ---

def server_loop():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '0.0.0.0'
    server_port = 8808

    server_socket.bind((server_host, server_port))
    server_socket.listen(5)  # Maximum number of queued connections

    print('Server listening on {}:{}'.format(server_host, server_port))

    # --- Server waiting for connection ---
    while True:
        client_socket, client_address = server_socket.accept()

        print('[{}] New connection from {}:{}'.format(ut.get_time_str(), client_address[0], client_address[1]))

        new_thread = ClientConn(client_socket, client_address)
        new_thread.start()


# --- Init server listening loop ---

server_thread = threading.Thread(target=server_loop)
server_thread.start()

# # --- Plotter ---
#
# plt.ion()
#
# plotter = terrain.TerrainWindow(335, 125)
# plotter.update_map(BODIES, opacity=0.2)
#
# plotter.show()
#
# # --- Main loop ---
# while True:
#     plotter.update_map(get_bodies())
#     plotter.show()
