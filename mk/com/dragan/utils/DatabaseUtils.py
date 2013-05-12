'''
Created on Jul 15, 2012

@author: dzaharie
'''
import logging
import redis
log = logging.getLogger('Redis Utils')
database = redis.Redis('localhost')


def dbget(keyPrefix, description):
    key = keyPrefix + ':' + str(sorted(description.values()))
    result = database.get(key)
    log.info('reading key:' + key + ' from database')
    if result == None:
        log.info('value not found')
    else:
        log.info('value found: ' + str(result))
    return result
    
def dbset(keyPrefix, description, value):
    key = keyPrefix + ':' + str(sorted(description.values()))
    log.info('setting key:' + key + ' with value:' + str(value) + ' in database')
    return database.set(key, value)

def dbgetlist(keyPrefix, description):
    key = keyPrefix + ':' + str(sorted(description.values()))
    return dbgetlistSimple(key)

def dbgetlistSimple(key):
    result = database.lrange(key, 0, -1)
    log.info('reading key:' + key + ' from database')
    if not result:
        log.info('value not found')
        return result
    else:
        parsed = []
        for r in result:
            try:
                parsed.append(float(r))
            except:
                parsed.append(r)
        log.info('value found: ' + str(parsed))
        return parsed
    
def dbsetlist(keyPrefix, description, lista):
    key = keyPrefix + ':' + str(sorted(description.values()))
    dbsetlistSimple(key, lista)
        
def dbsetlistSimple(key, lista):
    log.info('setting key:' + key + ' with value:' + str(lista) + ' in database')
    
    for item in lista:
        database.rpush(key, item)
