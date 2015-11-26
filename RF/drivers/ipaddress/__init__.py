import socket

def getIpAddress():
    try:
        return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    except:
        return None
                                                                                                                                         
if __name__ == '__main__':
    print("IP Address: "+getIpAddress())