# coding=utf-8

import os
import pin
import assembly as ASM

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'micro.bin')

micro = [pin.HLT for _ in range(0x10000)] # 在ROM里写满HLT指令

for addr in range(0x10000):
    ir = addr >> 8            # 从地址中取出IR即指令信息
    psw = (addr >> 4) & 0xf   # 从地址中取出PSW即状态字信息
    cyc = addr & 0xf          # 从地址中取出系统时钟周期信息

    if cyc < len(ASM.FETCH):  # 如果将指令一个个填充进去
        micro[addr] = ASM.FETCH[cyc]

with open(filename, 'wb') as file: # 转换成二进制
    for var in micro:
        value = var.to_bytes(4, byteorder='little')
        file.write(value)

print('Compile micro instruction finish!!!')