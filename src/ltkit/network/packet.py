import json
import zlib

def compress(message):
    try:
        return zlib.compress(
            json.dumps(message,
                       separators=(',', ':')),
            9
        )
    except:
        return ''

def decompress(message):
    try:
        return json.loads(
            zlib.decompress(message)
        )
    except:
        return {}

def create_id(ip_address):
    
    return
