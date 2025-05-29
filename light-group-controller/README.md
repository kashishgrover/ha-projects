# Light Group Controller for Home Assistant

A modular MicroPython project for controlling Home Assistant light groups via a physical rotary encoder interface. This project runs on a Raspberry Pi Pico W and provides a simple way to control light brightness/temperature and toggle state.

## Hardware Components

1. Raspberry Pi Pico 2W
2. Rotary Encoder (EC11H)
3. TP4056 Type-C Charging Module
4. 800mAH LiPo Battery
5. Slide Switch
6. Jumper Cables

## Features

- Physical control of Home Assistant light groups
- Wi-Fi connectivity with auto-reconnect
- MQTT communication with Home Assistant
- Rotary encoder interface:
  - Turn to adjust color temperature
  - Press to toggle lights on/off
- Status indication via onboard LED
- Battery powered for portable use

## Setup Instructions

1. Copy `secrets.py.example` to `secrets.py` and fill in your Wi-Fi and MQTT credentials
2. Adjust settings in `config.py` if needed
