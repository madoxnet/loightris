#include <FastLED.h>

//How many LED's on are the LED strip?
#define NUM_LEDS 720
//Number of octets to fully populate the LED strip
#define LED_MEMORY_SIZE NUM_LEDS*3
//Which pin is the LED strip connected to?
#define DATA_PIN 0

CRGB leds[NUM_LEDS];

//Declare variables
int bytes_received=0;
int bytes_available=0;
int led_index=0;
int led_colour=0;

void setup()
{
  //Configure and initialize FastSPI library
  FastLED.addLeds<WS2811, DATA_PIN, GRB>(leds, NUM_LEDS);
  //Configure Serial, baud rate on a Teensy 3.0 is ignored 
  Serial.begin(9600);
}

void loop() {
  //Check if there is USB serial data available
  bytes_available = Serial.available();
  if(bytes_available > 0){
    //Serial.println(bytes_available);
    for(int i=0; (i < bytes_available); i++){
      //Read bytes from serial up to all available but checking for max strip size
      //Assign it to the LED buffer in RGB pixel order
      led_index = bytes_received / 3;
      led_colour = bytes_received % 3;
      if (bytes_received < LED_MEMORY_SIZE) {
        //Serial.flush isn't working, so lets just read it all but only write those that is valid
        switch(led_colour){
          case 0:
            leds[led_index].r =  Serial.read();
            break;
          case 1:
            leds[led_index].g = Serial.read();
            break;
          case 2:
            leds[led_index].b = Serial.read();
            break;
          default:
            break;
        }
        bytes_received++;
      } else {
        Serial.read();  //Dummy read, because Serial.flush isn't working
      } 
    }
  }
  if(bytes_received >= LED_MEMORY_SIZE){
    //Got all the data we need to populate the strip
    bytes_received = 0;  //Reset the count
    Serial.write("F");
    FastLED.show();  //Show it!
  }
}

