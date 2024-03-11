import numpy as np
import matplotlib.pyplot as plt
import socket

host = "84.237.21.36"
port = 5152


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data


def position(B):
    bmax = []
    for ny in range(B.shape[0]):
        for nx in range(B.shape[1]):
            if B[ny, nx] != 0:
                if (
                    B[ny - 1, nx] < B[ny, nx]
                    and B[ny, nx - 1] < B[ny, nx]
                    and B[ny + 1, nx] < B[ny, nx]
                    and B[ny, nx + 1] < B[ny, nx]
                ):
                    bmax.append([ny, nx])
    return bmax


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    while beat == b"nope":
        sock.send(b"get")
        bts = recvall(sock, 40002)
        im = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        pos = position(im)
        pos1 = pos[0]
        pos2 = pos[1]

        res = np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
        res = round(res, 1)

        sock.send(f"{res}".encode())

        sock.send(b"beat")
        beat = sock.recv(20)

    print(beat)
    print(res)
    plt.title(f"{pos1} {pos2}")
    plt.imshow(im,cmap = 'hot')
    plt.show()