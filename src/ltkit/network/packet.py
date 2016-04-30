import json
import zlib

def compress(message):
    return zlib.compress(
        json.dumps(message,
                   separators=(',', ':')),
        9
    )

def decompress(message):
    return json.loads(
        zlib.decompress(message)
    )

def create_id(ip_address):
    
    return
