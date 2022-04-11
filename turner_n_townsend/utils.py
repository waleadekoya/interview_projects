import logging

FORMAT = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger('Turner & Townsend')
