'''
Created on Oct 11, 2011

@author: Dragan
'''
import logging

ch = logging.StreamHandler()
logger = logging.getLogger()
logger.addHandler(ch)
f = logging.Formatter('%(levelname)s: %(name)s - %(message)s')
ch.setFormatter(f)
logger.setLevel(logging.INFO)