import json

from gym_donkeycar.core.sim_client import SDClient


class PrivateAPIClient(SDClient):
    def __init__(self, address, private_key: int, socket_sleep_time: float = 0.01):
        super().__init__(*address, poll_socket_sleep_time=socket_sleep_time)

        self.private_key = private_key
        self.is_verified = False

    def on_msg_recv(self, json_packet):
        msg_type = json_packet.get("msg_type")

        if msg_type == "verified":
            self.is_verified = True

    def send_verify(self):
        msg = {"msg_type": "verify", "private_key": str(self.private_key)}
        self.send_now(json.dumps(msg))

    def send_seed(self, seed=42):
        # Note: send_verify must be sent before
        msg = {"msg_type": "set_random_seed", "seed": str(seed)}
        self.send_now(json.dumps(msg))
