#!python3
import api_manager
import logging
import time
import sys
from drone_manager import DroneManager

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

api_manager.run()

try:
    drone_manager = DroneManager()
except Exception as exception:
    logger.error(exception)

# drone_manager.takeoff()
# time.sleep(5)

# drone_manager.up()
# time.sleep(5)

# drone_manager.right()
# time.sleep(5)

# drone_manager.left()
# time.sleep(5)

# drone_manager.land()
# drone_manager.stop()
