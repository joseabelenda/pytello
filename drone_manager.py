#!python3
import logging
import socket
import sys
import threading
import time

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

DEFAULT_DISTANCE = 30
DEFAULT_SPEED = 10
DEFAULT_DEGREE = 10


class DroneManager(object):
    def __init__(self, drone_ip='192.168.10.1', drone_port=8889,
                 host_ip='192.168.10.2', host_port=8889, speed=DEFAULT_SPEED):
        self.drone_ip = drone_ip
        self.drone_port = drone_port

        self.drone_address = (drone_ip, drone_port)

        self.host_ip = host_ip
        self.host_port = host_port

        self.speed = speed

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            self.socket.bind((self.host_ip, self.host_port))
        except:
            raise Exception('Was not possible to connect to drone')

        self.response = None
        self.stop_event = threading.Event()
        self._response_thread = threading.Thread(
            target=self.receive_response, args=(self.stop_event, ))
        self._response_thread.start()

        self.send_command('command')
        self.send_command('streamon')
        self.set_speed(self.speed)

    def receive_response(self, stop_event):
        while not stop_event.is_set():
            try:
                self.response, ip = self.socket.recvfrom(3000)
                logger.info({'action': 'receive_response',
                            'response': self.response})
            except socket.error as ex:
                logger.error({'action': 'receive_response',
                              'ex': ex})
                break

    def __dell__(self):
        self.stop()

    def back(self, distance=DEFAULT_DISTANCE):
        return self.move('back', distance)

    def clockwise(self, degree=DEFAULT_DEGREE):
        return self.send_command(f'cw {degree}')

    def counter_clockwise(self, degree=DEFAULT_DEGREE):
        return self.send_command(f'ccw {degree}')

    def down(self, distance=DEFAULT_DISTANCE):
        return self.move('down', distance)

    def flip_front(self):
        return self.send_command('flip f')

    def flip_back(self):
        return self.send_command('flip b')

    def flip_left(self):
        return self.send_command('flip l')

    def flip_right(self):
        return self.send_command('flip r')

    def forward(self, distance=DEFAULT_DISTANCE):
        return self.move('forward', distance)

    def land(self):
        self.send_command('land')

    def left(self, distance=DEFAULT_DISTANCE):
        return self.move('left', distance)

    def move(self, direction, distance):
        distance = float(distance)
        return self.send_command(f'{direction} {distance}')

    def right(self, distance=DEFAULT_DISTANCE):
        return self.move('right', distance)

    def send_command(self, command):
        logger.info({'action': 'send_command', 'command': command})
        self.socket.sendto(command.encode('utf-8'), self.drone_address)

        retry = 0
        while self.response is None:
            time.sleep(0.3)
            if retry > 3:
                break
            retry += 1

        if self.response is None:
            response = None
        else:
            response = self.response.decode('utf-8')
        self.response = None
        return response

    def set_speed(self, speed):
        return self.send_command(f'speed {speed}')

    def stop(self):
        self.stop_event.set()
        retry = 0

        while self._response_thread.is_alive():
            time.sleep(0.3)
            if retry > 30:
                break
            retry += 1

        self.socket.close()

    def takeoff(self):
        self.send_command('takeoff')

    def up(self, distance=DEFAULT_DISTANCE):
        return self.move('up', distance)


drone_manager = DroneManager()

drone_manager.takeoff()
time.sleep(5)

drone_manager.up()
time.sleep(5)

drone_manager.right()
time.sleep(5)

drone_manager.left()
time.sleep(5)

drone_manager.land()
drone_manager.stop()
