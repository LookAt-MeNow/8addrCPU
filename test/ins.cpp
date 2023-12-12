#include <iostream>
#include <fstream>
#include <vector>

#define WE_A (1 << 0)
#define CS_A (1 << 1)

#define WE_B (1 << 2)
#define CS_B (1 << 3)

#define WE_C (1 << 4)
#define CS_C (1 << 5)

#define ALU_ADD 0
#define ALU_SUB (1 << 6)
#define ALU_OUT (1 << 7)

#define WE_M (1 << 8)
#define CS_M (1 << 9)

#define WE_PC (1 << 10)
#define EN_PC (1 << 11)
#define CS_PC (1 << 12)

#define HLT (1 << 15)

int main() {
    std::string filename = "ins.bin";
    std::ofstream file(filename, std::ios::binary);

    std::vector<unsigned short> micro = {
        CS_M | CS_A | WE_A | WE_PC | EN_PC | CS_PC,
        CS_M | CS_B | WE_B | WE_PC | EN_PC | CS_PC,
        ALU_ADD | ALU_OUT | CS_C | WE_C,
        CS_C | WE_M | CS_M | WE_PC | EN_PC | CS_PC,
        HLT
    };

    for (unsigned short value : micro) {
        file.write(reinterpret_cast<const char*>(&value), sizeof(value));
        std::cout << value << " ";
    }

    file.close();
    std::cout << "\nFinish compile!!!" << std::endl;

    return 0;
}