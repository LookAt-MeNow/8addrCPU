# coding=utf-8

import pin

FETCH = [
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.IR_IN | pin.PC_INC,
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.DST_IN | pin.PC_INC,
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.SRC_IN | pin.PC_INC,
]

MOV = 0 | pin.ADDR2                       # MOV指令定义位1000 xxxx
ADD = (1 << pin.ADDR2_SHIFT) | pin.ADDR2  # ADD指令定义为 1001 xxxx

NOP = 0     # NOP指令定义为 0000 0000
HLT = 0x3f  # HLT指令定义为 0011 1111

""" INSTRUCTIONS = {
    2: { # 二操作数指令列表
        MOV: { # MOV指令寻址方式列表
            (pin.AM_REG, pin.AM_INS): [  # (寄存器寻址，立即寻址) 例如 MOV A,5
                pin.DST_W | pin.SRC_OUT, # 微指令：DST寄存器写，SRC读，SRC->DST，这里DST是控制寄存器写
            ]
        }
    },
    1: {},# 一操作数指令列表
    0: {  # 零操作数指令列表
        NOP: [
            pin.CYC, # 让指令周期清零，跳过这次指令
        ],
        HLT: [
            pin.HLT, # 指令停止
        ]
    }
} """
MOV = (0 << pin.ADDR2_SHIFT) | pin.ADDR2
ADD = (1 << pin.ADDR2_SHIFT) | pin.ADDR2
SUB = (2 << pin.ADDR2_SHIFT) | pin.ADDR2

INC = (0 << pin.ADDR1_SHIFT) | pin.ADDR1
DEC = (1 << pin.ADDR1_SHIFT) | pin.ADDR1

INSTRUCTIONS = {
    2: {
        MOV: {
            (pin.AM_REG, pin.AM_INS): [ # (寄存器寻址，立即寻址) 例如 MOV A,5
                pin.DST_W | pin.SRC_OUT, # 微指令：DST写寄存器，SRC寄存器读，SRC->DST，读取SRC寄存器里数据送入DST指定的寄存器中
            ],
            (pin.AM_REG, pin.AM_REG): [ # (寄存器寻址，寄存器寻址) 例如 MOV A,B
                pin.DST_W | pin.SRC_R,  # 微指令：DST写寄存器，SRC读寄存器，SRC->DST，这里DST，SRC是控制其他寄存器写和读
            ],
            (pin.AM_REG, pin.AM_DIR): [ # (寄存器寻址，直接寻址) 例如 MOV A,[5]
                pin.SRC_OUT | pin.MAR_IN, # 从SRC寄存器读，送到RAM地址线上
                pin.DST_W | pin.RAM_OUT # 从RAM指定地址读，DST写寄存器
            ],
            (pin.AM_REG, pin.AM_RAM): [ # (寄存器寻址，寄存器间接寻址) 例如 MOV A,[B]
                pin.SRC_R | pin.MAR_IN, # SRC读寄存器(数据)，送到RAM地址线上
                pin.DST_W | pin.RAM_OUT # 从RAM指定地址读数据，DST写寄存器
            ],
            (pin.AM_DIR, pin.AM_INS): [ # (直接寻址，立即寻址) 例如 MOV [5],5
                pin.DST_OUT | pin.MAR_IN, # 从DST寄存器读数据，送到RAM地址线上
                pin.RAM_IN | pin.SRC_OUT # 从SRC寄存器读数据，往RAM里写
            ],
            (pin.AM_DIR, pin.AM_REG): [ # (直接寻址，寄存器寻址) 例如 MOV [5],A
                pin.DST_OUT | pin.MAR_IN, # DST寄存器读，送到地址线上
                pin.RAM_IN | pin.SRC_R, # SRC读寄存器，往RAM里写
            ],
            (pin.AM_DIR, pin.AM_DIR): [ # (直接寻址，直接寻址) 例如 MOV [5],[2]
                pin.SRC_OUT | pin.MAR_IN, # SRC寄存器读到地址线上
                pin.RAM_OUT | pin.T1_IN, # 从RAM里读出来，写到T1寄存器里
                pin.DST_OUT | pin.MAR_IN, # 再把DST寄存器读到地址线上
                pin.RAM_IN | pin.T1_OUT, # 把T1寄存器的值写到RAM里
            ],
            (pin.AM_DIR, pin.AM_RAM): [ # (直接寻址，寄存器间接寻址) 例如 MOV [5],[A]
                pin.SRC_R | pin.MAR_IN, # SRC读寄存器到地址线上
                pin.RAM_OUT | pin.T1_IN, # 把RAM数据读到T1上
                pin.DST_OUT | pin.MAR_IN, # DST寄存器读到地址线上
                pin.RAM_IN | pin.T1_OUT, # 把T1写到RAM里
            ],

            (pin.AM_RAM, pin.AM_INS): [ # (寄存器间接寻址，立即数寻址) 例如 MOV [A],5
                pin.DST_R | pin.MAR_IN, # DST读寄存器到地址线上
                pin.RAM_IN | pin.SRC_OUT # SRC寄存器数据写到RAM里
            ],
            (pin.AM_RAM, pin.AM_REG): [ # (寄存器间接寻址，寄存器寻址) 例如 MOV [A],B
                pin.DST_R | pin.MAR_IN, # DST读寄存器到地址线上
                pin.RAM_IN | pin.SRC_R, # SRC读寄存器到RAM里
            ],
            (pin.AM_RAM, pin.AM_DIR): [ # (寄存器间接寻址，直接寻址) 例如 MOV [A],[5]
                pin.SRC_OUT | pin.MAR_IN, # SRC寄存器的数据送到地址线上
                pin.RAM_OUT | pin.T1_IN, # RAM里数据读到T1里
                pin.DST_R | pin.MAR_IN, # DST读寄存器到地址总线上
                pin.RAM_IN | pin.T1_OUT, # 把T1读到RAM里
            ],
            (pin.AM_RAM, pin.AM_RAM): [ # (寄存器间接寻址，寄存器间接寻址) 例如 MOV [A],[B]
                pin.SRC_R | pin.MAR_IN, # SRC读寄存器到地址线上
                pin.RAM_OUT | pin.T1_IN, # RAM输出到T1
                pin.DST_R | pin.MAR_IN, #  DST读寄存器到地址线上
                pin.RAM_IN | pin.T1_OUT, # T1输出到RAM
            ]
        },
        ADD: {
            (pin.AM_REG, pin.AM_INS): [ # (寄存器寻址，直接寻址) 例如ADD A,5
                pin.DST_R | pin.A_IN, # DST读寄存器数据到A寄存器中
                pin.SRC_OUT | pin.B_IN, # SRC寄存器读数据到B寄存器中
                pin.OP_ADD | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW #选择加法 ，ALU输出，DST写寄存器，ALU状态字
            ],
            (pin.AM_REG, pin.AM_REG): [ # (寄存器寻址，寄存器寻址) 例如ADD A,B
                pin.DST_R | pin.A_IN, # DST读寄存器到A寄存器
                pin.SRC_R | pin.B_IN, # SRC读寄存器到B寄存器
                pin.OP_ADD | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW # 加法，ALU输出，DST写寄存器，ALU状态字
            ],
        },
        SUB: {
            (pin.AM_REG, pin.AM_INS): [ # (寄存器寻址，直接寻址) 例如 SUB A,5
                pin.DST_R | pin.A_IN, # DST读寄存器到A寄存器
                pin.SRC_OUT | pin.B_IN, # SRC寄存器读数据到B寄存器
                pin.OP_SUB | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW # 减法，ALU输出，DST写寄存器 ，ALU状态字
            ],
            (pin.AM_REG, pin.AM_REG): [ # (寄存器寻址，寄存器寻址) 例如 SUB A,B
                pin.DST_R | pin.A_IN, # DST读寄存器到A寄存器
                pin.SRC_R | pin.B_IN, # SRC读寄存器到B寄存器
                pin.OP_SUB | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW # 减法，ALU输出，DST写寄存器，ALU状态字
            ],
        },
    },
    1: {
        INC: {
            pin.AM_REG: [
                pin.DST_R | pin.A_IN, # DST读寄存器到A寄存器
                pin.OP_INC | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW # +1，ALU输出，DST写寄存器，ALU状态字
            ],
        },
        DEC: {
            pin.AM_REG: [
                pin.DST_R | pin.A_IN, # DST读寄存器到A寄存器
                pin.OP_DEC | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW # -1，ALU输出，DST写寄存器，ALU状态字
            ],
        },
    },
    0: {
        NOP: [
            pin.CYC,
        ],
        HLT: [
            pin.HLT,
        ]
    }
}
