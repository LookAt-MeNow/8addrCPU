import os

dirname = os.path.dirname(os.path.abspath(__file__))

for var in range(256):
    byte = var.to_bytes(2,byteorder="little")
    print(byte)
    break