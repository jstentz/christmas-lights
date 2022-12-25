# QR-Code

This repo contains all the code for generating qr codes and displaying them on a [SparkFun Micro OLED Display](https://learn.sparkfun.com/tutorials/micro-oled-breakout-hookup-guide). For the Christmas Lights project, we used an [NodeMCU 1.0 ESP-12E](https://protosupplies.com/product/esp8266-nodemcu-v1-0-esp-12e-wifi-module/) module to drive the display, but any 3.3v Arduino or Arduino-like microcontroller will also work. Instructions for connecting the OLED to the ESP-12E can be found [here](https://www.electronicshub.org/nodemcu-esp8266-oled-display/)

## How it works

In this setup, there's a main computer that generates a QR code + password and sends it to a microcontroller to display. The main computer uses the [QR-Code-generator](https://github.com/nayuki/QR-Code-generator) python package to generate a qr code, converts it to a bitmap, then converts this bitmap to a bytestream that mirrors the OLED's display buffer. The password and bytestream are then sent to the microcontroller which unpacks the message and displays the QR code + password on the OLED.