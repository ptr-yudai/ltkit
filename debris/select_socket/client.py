# coding: utf-8
import socket
 
#----------------------------------------------------------------------
def sendmsg(message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 8001))
        client.send(message)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
    except:
        pass
 
if __name__ == "__main__":
    sendmsg("Hello.")
    sendmsg("こんにちは。")
    sendmsg("你好。")
