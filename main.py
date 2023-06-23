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


def get_bodies():
    return BODIES


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


def bertha_ai(data):
    new_pos = deduce_bot_position(data, cam_rot=[0, 0])


    if new_pos is not None:
        print("New coords!", new_pos)
        found = False
        for body in BODIES:
            if body.id == 71:
                print("updating body")
                body.update(new_pos[0], new_pos[1])
                found = True
                break

        if not found:
            BODIES.append(Body(71, new_pos[0], new_pos[1], BodyType.CONNECTED_BODY))


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
        self.process_data(data)

        # --- Send data back to the client ---
        self.client_socket.sendall("got your message".encode('utf-8'))

        self.client_socket.close()

    def process_data(self, data) -> str:  # will send back the request to send to the client
        data = json.loads(data)

        if data["sender"] == "esieabot-bcc6b4":
            bertha_ai(data)

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
