import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(message)s'
)

logger = logging.getLogger(__name__)
