#ifndef CHAINED_SERVO_BOARD_H
#define CHAINED_SERVO_BOARD_H

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

class ChainedServoBoard {
private:
    Adafruit_PWMServoDriver _driver;
    uint8_t _address;
    uint16_t _freq;
    uint16_t _min_us;
    uint16_t _max_us;
    uint16_t _max_degrees;

    bool i2c_write_verify(uint8_t reg, uint8_t val);

public:
    ChainedServoBoard(uint8_t address, uint16_t freq, uint16_t min_us, uint16_t max_us, uint16_t max_degrees);
    void begin();
    void writeAngle(uint8_t channel, float degrees);

    bool wake();
    bool isAsleep();
};

#endif