#include "PCA9685_header.h"

ChainedServoBoard::ChainedServoBoard(uint8_t address, uint16_t freq, uint16_t min_us, uint16_t max_us, uint16_t max_degrees)
    : _driver(address), _address(address), _freq(freq), _min_us(min_us), _max_us(max_us), _max_degrees(max_degrees) {}

void ChainedServoBoard::begin() {
    _driver.begin();
    _driver.setPWMFreq(_freq);
    delay(10);
    wake();
}

void ChainedServoBoard::writeAngle(uint8_t channel, float degrees) {
    degrees = constrain(degrees, 0.0f, (float)_max_degrees);
    float target_us = _min_us + ((degrees / _max_degrees) * (_max_us - _min_us));
    float seconds_per_tick = 1.0f / (_freq * 4096.0f);
    uint16_t target_ticks = (target_us / 1000000.0f) / seconds_per_tick;
    _driver.setPWM(channel, 0, target_ticks);
}

bool ChainedServoBoard::i2c_write_verify(uint8_t reg, uint8_t val) {
    for (int attempt = 0; attempt < 3; attempt++) {
        Wire.beginTransmission(_address);
        Wire.write(reg);
        Wire.write(val);
        byte err = Wire.endTransmission();
        if (err == 0) return true;
        delay(2);
    }
    return false;
}

bool ChainedServoBoard::isAsleep() {
    Wire.beginTransmission(_address);
    Wire.write(0x00); // MODE1 register
    byte err = Wire.endTransmission();
    if (err != 0) return true;

    Wire.requestFrom(_address, (uint8_t)1);
    if (Wire.available() < 1) return true;
    byte mode1 = Wire.read();
    return (mode1 & 0x10) != 0; // bit 4 = SLEEP
}

bool ChainedServoBoard::wake() {
    bool ok = i2c_write_verify(0x00, 0b00100000); // AI set, SLEEP cleared
    delay(1);
    return ok && !isAsleep();
}