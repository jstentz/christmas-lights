/******************************************************************************
  MicroOLED_Hello.ino
  SFE_MicroOLED Hello World Demo
  Jim Lindblom @ SparkFun Electronics
  Original Creation Date: October 26, 2014
  
  This sketch lights up a familiar pattern on the MicroOLED
  Breakout. It's a great way to prove you've connected everything
  correctly and that your display is in working order.
  
  Hardware Connections:
    We'll be using the SPI interface on the MicroOLED, though it
    also supports I2C (and a really messy parallel). If you want
    to swap in I2C, read through the comments to find out how.
    
    MicroOLED ------------- Arduino
      GND ------------------- GND
      VDD ------------------- 3.3V (VCC)
    D1/MOSI ----------------- D11 (don't change)
    D0/SCK ------------------ D13 (don't change)
      D2
      D/C ------------------- D8 (can be any digital pin)
      RST ------------------- D9 (can be any digital pin)
      CS  ------------------- D10 (can be any digital pin)
    
  Development environment specifics:
  	IDE: Arduino 1.0.5
  	Hardware Platform: MicroOLED Breakout
                           Arduino Pro 3.3V/8MHz
  
  Note: The display on the MicroOLED is a 1.8V-3.3V device only.
  Don't try to connect a 5V Arduino directly to it! Use level
  shifters in between the data signals if you have to resort to
  a 5V board.
  
  This code is beerware; if you see me (or any other SparkFun 
  employee) at the local, and you've found our code helpful, 
  please buy us a round!
  
  Distributed as-is; no warranty is given.
*******************************************************************************/
#include <Wire.h>  // Include Wire if you're using I2C
#include <SPI.h>  // Include SPI if you're using SPI
#include <SFE_MicroOLED.h>  // Include the SFE_MicroOLED library

//////////////////////////
// MicroOLED Definition //
//////////////////////////
#define PIN_RESET D2  // Connect RST to pin 9 (req. for SPI and I2C)
#define PIN_DC    D1  // Connect DC to pin 8 (required for SPI)
#define PIN_CS    D8 // Connect CS to pin 10 (required for SPI)
#define DC_JUMPER 0 // Set to either 0 (default) or 1 based on jumper, matching the value of the DC Jumper
// Also connect pin 13 to SCK and pin 11 to MOSI

#define PASSWORD_LENGTH 8
#define BITMAP_SIZE 384
#define MESSAGE_SIZE (PASSWORD_LENGTH + BITMAP_SIZE)

//////////////////////////////////
// MicroOLED Object Declaration //
//////////////////////////////////
// Declare a MicroOLED object. The parameters include:
// 1 - Reset pin: Any digital pin
// 2 - D/C pin: Any digital pin (SPI mode only)
// 3 - CS pin: Any digital pin (SPI mode only, 10 recommended)

MicroOLED oled(PIN_RESET, PIN_DC, PIN_CS); //Example SPI declaration, comment out if using I2C

typedef struct {
  char password[PASSWORD_LENGTH];
  uint8_t bitmap[BITMAP_SIZE];
} * message_t;

uint8_t message[MESSAGE_SIZE];

void setup()
{

  delay(100);
  //Wire.begin(); //set up I2C bus, uncomment if you are using I2C
  // These three lines of code are all you need to initialize the
  // OLED and print the splash screen.
  
  // Before you can start using the OLED, call begin() to init
  // all of the pins and configure the OLED.
  oled.begin();
  // clear(ALL) will clear out the OLED's graphic memory.
  // clear(PAGE) will clear the Arduino's display buffer.
  oled.clear(ALL);  // Clear the display's memory (gets rid of artifacts)
  // To actually draw anything on the display, you must call the
  // display() function. 
  oled.display();
  Serial.begin(9600);   
}

void update_qr_code() {
  oled.drawBitmap(((message_t)message)->bitmap);
}

void update_password() {
  oled.setFontType(0);
  oled.setCursor(8, 40);
  oled.print(((message_t)message)->password);
}

void loop()
{
  //Serial.printf("%p, %p\n", ((message_t)message)->password, ((message_t)message)->bitmap);
  size_t pos = 0;
  while(pos < MESSAGE_SIZE) {
    uint32_t n = Serial.available();
    uint32_t num_to_read = min(n, MESSAGE_SIZE - pos);
    uint8_t *buf = &((uint8_t*)message)[pos];
    size_t num_read = Serial.readBytes(buf, num_to_read);
    pos += num_read;
  }
  oled.clear(ALL);
  update_qr_code();
  update_password();
  oled.display();
}
