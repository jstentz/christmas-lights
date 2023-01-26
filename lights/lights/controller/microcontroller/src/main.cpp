#include <Arduino.h>
#include <WS2812Serial.h>
#define USE_WS2812SERIAL
#include <FastLED.h>

#define NUM_LEDS 500

// Usable pins:
//   Teensy LC:   1, 4, 5, 24
//   Teensy 3.2:  1, 5, 8, 10, 31   (overclock to 120 MHz for pin 8)
//   Teensy 3.5:  1, 5, 8, 10, 26, 32, 33, 48
//   Teensy 3.6:  1, 5, 8, 10, 26, 32, 33
//   Teensy 4.0:  1, 8, 14, 17, 20, 24, 29, 39
//   Teensy 4.1:  1, 8, 14, 17, 20, 24, 29, 35, 47, 53

#define DATA_PIN 8

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() {
	LEDS.addLeds<WS2812SERIAL,DATA_PIN,BGR>(leds,NUM_LEDS);
	LEDS.setBrightness(UINT8_MAX);
  // Wait for usb to be ready.
  while(!Serial);
}

void loop() {
  size_t bytesRead = 0;
  while(bytesRead < sizeof(leds)) {
    if(Serial.available()) {
      ((uint8_t *)leds)[bytesRead++] = Serial.read();
    }
  }
  LEDS.show();
}
