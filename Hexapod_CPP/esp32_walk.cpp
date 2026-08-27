#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include "PCA9685_header.h"

const int esp32_rx = 11;
const int esp32_tx = 12;
const int SDA_main = 8;
const int SCL_main = 9;
const int OE_pin = 18;

//PCA9685 stuff
const int servo_freq = 50;
const int servo_min_us = 500;
const int servo_max_us = 2500;

ChainedServoBoard right_board_270(0x41, servo_freq, servo_min_us, servo_max_us, 270);
ChainedServoBoard left_board_270(0x40, servo_freq, servo_min_us, servo_max_us, 270);

//JOINT MATRIX SETUP
const int LF = 0; //left front
const int LM = 1; //left middle
const int LB = 2; //left back

const int RF = 0; //right front
const int RM = 1; //right middle
const int RB = 2; //right back

const int coxa = 0; 
const int femur = 1;
const int tibia = 2;

const int left_leg_matrix[3][3]= {
    {5, 6, 7}, //LF: coxa on PCA5, femur PCA6, tibia PCA7
    {9, 10, 11}, //same but for LM
    {13, 14, 15} //LB
};

const int right_leg_matrix[3][3]= {
    {10, 9, 8}, //RF: coxa on PCA10, femur PCA9, tibia PCA8
    {6, 5, 4}, //same but for RM
    {2, 1, 0} //RB
};

//SERVO OFFSETS
float left_leg_offsets[3][3]{
    {135.0, 135.0, 135.0+0.0}, //LF coxa, femur, tibia (midpoint 135.0+found offset values)
    {135.0+0.0, 135.0+0.0, 135.0+0.0}, //LM coxa, femur, tibia
    {135+0.0, 135.0+0.0, 135.0+0.0}, //LB coxa, femur, tibia
};

float right_leg_offsets[3][3]{
    {135.0+31.0, 135.0+36.0, 135+33.0}, //RF coxa, femur, tibia (Increasing angle drives coxa forward (CCW), femur up, tibia down)
    {135.0+31.0, 135.0+36.0, 135.0+33.0}, //RM coxa, femur, tibia
    {135.0+31.0, 135.0+36.0, 135.0+0.0}, //RB coxa, femur, tibia
};

//MOVE LEG AND ADD OFFSETS:
void set_left_leg(int leg, int joint, float target_angle){

    int pin = left_leg_matrix[leg][joint]; //looks up which PCA pin is needed
    float offset = left_leg_offsets[leg][joint]; //looks up the offset needed
    float trimmed_angle = target_angle + offset;
    left_board_270.writeAngle(pin, trimmed_angle);

}

void set_right_leg(int leg, int joint, float target_angle){

    int pin = right_leg_matrix[leg][joint]; //looks up which PCA pin is needed
    float offset = right_leg_offsets[leg][joint]; //looks up the offset needed
    float trimmed_angle = target_angle + offset;
    right_board_270.writeAngle(pin, trimmed_angle);
    
}

unsigned long last_watchdog = 0;
const unsigned long watchdog_interval_ms = 500;
bool check_right_next = true;

void servo_watchdog() {
    if (check_right_next) {
        if (right_board_270.isAsleep()) {
            Serial.println("WATCHDOG: 0x41 was asleep, re-waking");
            right_board_270.wake();
        }
    } else {
        if (left_board_270.isAsleep()) {
            Serial.println("WATCHDOG: 0x40 was asleep, re-waking");
            left_board_270.wake();
        }
        
    }
    check_right_next = !check_right_next;
}

void setup() {

  pinMode(OE_pin, OUTPUT);
  digitalWrite(OE_pin, LOW);
  Serial.begin(9600);

  delay(1500);

    Wire.begin(SDA_main, SCL_main);
    Wire.setClock(100000); // Set to 100kHz to stop timeout errors
    right_board_270.begin();
    left_board_270.begin();

  Serial.print("setup done");
    
}
double last_check = millis();


void loop(){

  for (int leg = 0; leg <3; leg++){
    for (int joint = 0; joint <3; joint++){
        set_left_leg(leg, joint, 0.0f);
        set_right_leg(leg, joint, 0.0f);
        delay(5);
    }
       
  }

  if (millis() - last_watchdog >= watchdog_interval_ms) {
    servo_watchdog();
      last_watchdog = millis();
  }

  // // MODE1 check, throttled so it doesn't spam Serial
  // if (millis() - last_check >= 1000) {
  //   Wire.beginTransmission(0x40);
  //   Wire.write(0x00);
  //   Wire.endTransmission();
  //   Wire.requestFrom(0x40, 1);
  //   byte mode1 = Wire.read();
  //   Serial.print("MODE1 (0x40): 0b");
  //   Serial.println(mode1, BIN);

  //   Wire.beginTransmission(0x41);
  //   Wire.write(0x00);
  //   Wire.endTransmission();
  //   Wire.requestFrom(0x41, 1);
  //   byte mode1_b = Wire.read();
  //   Serial.print("MODE1 (0x41): 0b");
  //   Serial.println(mode1_b, BIN);

  //   last_check = millis();
  // }

}
