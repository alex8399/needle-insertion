#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include "Adafruit_VL6180X.h"

uint16_t SAMPLERATE_DELAY_MS = 10;
uint16_t PRINT_DELAY_MS = 100;
uint16_t printCount = 0;

int fsrAnalogPin = A0;

Adafruit_VL6180X vl = Adafruit_VL6180X();
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

void setup(void)
{
  Serial.begin(115200);

  while (!Serial) delay(10);
  
  if (!bno.begin())
  {
    Serial.print("No gyroscope detected.");
    while (1);
  }

  if (!vl.begin()) {
    Serial.println("No distance sensor detected.");
    while (1);
  }

  delay(1000);
}

void loop(void)
{
  unsigned long tStart = micros();

  if (printCount * SAMPLERATE_DELAY_MS >= PRINT_DELAY_MS) {
    Serial.print("range=");
    Serial.print(vl.readRange());

    sensors_event_t orientationData;
    bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);

    Serial.print(" | roll=");
    Serial.print(orientationData.orientation.z);
    Serial.print(" | pitch=");
    Serial.print(orientationData.orientation.y);
    Serial.print(" | yaw=");
    Serial.print(orientationData.orientation.x);

    Serial.print(" | force=");
    Serial.print(analogRead(fsrAnalogPin));

    Serial.println();

    printCount = 0;
  }
  else {
    printCount = printCount + 1;
  }

  while ((micros() - tStart) < (SAMPLERATE_DELAY_MS * 1000)) { }
}