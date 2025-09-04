# HeartRate Oximeter STM32

A project to monitor heart rate (in BPM) and blood oxygen levels (SpO2) using an STM32F411CEU6 microcontroller and MAX30102 sensor.

## Description
This project implements a heart rate and blood oxygen (SpO2) monitoring system using the STM32 microcontroller and the MAX30102 pulse oximetry sensor. The system reads infrared (IR) and red light data from the sensor, processes it, and controls an LED to indicate finger presence. Data is also sent via UART to a connected terminal for real-time monitoring.

## 🚀 Features
- Measures heart rate and blood oxygen levels.
- Uses STM32 with I2C communication to MAX30102.
- UART output for real-time data logging.
- Graph monitoring real time heart rate.
<img width="500" height="333" alt="image" src="https://github.com/user-attachments/assets/9339562b-95f7-4706-87e5-4aedf56c876b" />

## 🛠️ Hardware Requirements
- STM32 Board, ST-Link for programming.
- MAX30102 Sensor.
- USB-to-UART Module (e.g., CP2102, CH340).
- Jumper wires

<img width="500" height="350" alt="image" src="https://github.com/user-attachments/assets/26c8f20e-f59d-4725-986e-e198d25d0759" />

<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/90827b86-7aa6-44af-9b29-ddf2697b25e4" />

## 💻 Software Requirements
- STM32CubeIDE or similar IDE for STM32 development.
- Terminal software (e.g., Tera Term, PuTTY) for UART data viewing.

## 🔌Connectivity

| MAX30102 | STM32     |     Note     |
|----------|-----------|--------------|
| VIN      | 3.3V      | Power source |
| GND      | GND       | Ground       |
| SDA      | PA7       | I2C1 SDA     |
| SCL      | PA6       | I2C1 SCL     |

| UART      | STM32     |     Note     |
|-----------|-----------|--------------|
| TX        | PA2       | USART2_TX    |
| RX        | PA3       | USART2_RX    |
| GND       | GND       | Ground       |

- Baudrate: **115200**  

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/205Asura/HeartRate-Oximeter-STM32.git
   ```
2. Open the project in STM32CubeIDE.
3. Build and flash the code to your STM32 board using ST-Link.
4. Connect the USB-to-UART module to your STM32 and a PC.
5. Open a terminal (baud rate: 115200) to view the output.

## Usage
- Place your finger on the MAX30102 sensor.
- The LED will light up when a finger is detected.
- Monitor real-time BPM and SpO2 values on the terminal.

## Future Improvements:
- Measure blood oxygen
- Optimize algorithm to calculate heart rate and SpO2 to be more sensitive.
