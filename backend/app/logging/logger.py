import logging
import os

os.makedirs("logs", exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("nexus")

logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setFormatter(formatter)

file = logging.FileHandler(
    "logs/nexus.log"
)
file.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(file)