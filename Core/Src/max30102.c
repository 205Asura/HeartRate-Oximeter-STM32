#include "max30102.h"
#include "main.h"

// Hàm kiểm tra kết nối
uint8_t MAX30102_CheckConnection(void) {
    uint8_t part_id = 0;
    MAX30102_ReadRegister(REG_PART_ID, &part_id);
    return (part_id == 0x15) ? 1 : 0;
}

// Hàm khởi tạo
uint8_t MAX30102_Init(void) {
    uint8_t part_id = 0;

    // Kiểm tra kết nối
    MAX30102_ReadRegister(REG_PART_ID, &part_id);
    if (part_id != 0x15) {
        return 0;
    }

    // Reset chip
    MAX30102_WriteRegister(REG_MODE_CONFIG, 0x40);
    HAL_Delay(10);

    // Cấu hình FIFO
    MAX30102_WriteRegister(REG_FIFO_CONFIG, 0x4F);
    MAX30102_WriteRegister(REG_MODE_CONFIG, 0x03);
    MAX30102_WriteRegister(REG_SPO2_CONFIG, 0x27);
    MAX30102_WriteRegister(REG_LED1_PA, 0x24);
    MAX30102_WriteRegister(REG_LED2_PA, 0x24);

    // Clear FIFO
    MAX30102_WriteRegister(REG_FIFO_WR_PTR, 0x00);
    MAX30102_WriteRegister(REG_OVF_COUNTER, 0x00);
    MAX30102_WriteRegister(REG_FIFO_RD_PTR, 0x00);

    return 1;
}

// Hàm ghi thanh ghi
void MAX30102_WriteRegister(uint8_t reg, uint8_t value) {
    uint8_t data[2] = {reg, value};
    HAL_I2C_Master_Transmit(&hi2c1, MAX30102_I2C_ADDR, data, 2, HAL_MAX_DELAY);
}

// Hàm đọc thanh ghi
void MAX30102_ReadRegister(uint8_t reg, uint8_t *value) {
    HAL_I2C_Master_Transmit(&hi2c1, MAX30102_I2C_ADDR, &reg, 1, HAL_MAX_DELAY);
    HAL_I2C_Master_Receive(&hi2c1, MAX30102_I2C_ADDR, value, 1, HAL_MAX_DELAY);
}

// Hàm đọc dữ liệu từ FIFO
void MAX30102_ReadFIFO(uint32_t *red_value, uint32_t *ir_value) {
    uint8_t data[6];

    // Đọc 6 byte từ FIFO
    HAL_I2C_Mem_Read(&hi2c1, MAX30102_I2C_ADDR, REG_FIFO_DATA, 1, data, 6, HAL_MAX_DELAY);

    // Xử lý dữ liệu
    *red_value = ((data[0] << 16) | (data[1] << 8) | data[2]) >> 2;
    *ir_value = ((data[3] << 16) | (data[4] << 8) | data[5]) >> 2;
}
