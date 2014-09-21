loightris
=========
#How to Run
```
python test_game.py
```
#How to Play (Controls)
##Keyboard
 - Start New Game = Enter

###Left Player
 - Rotate = W
 - Left = A
 - Down = S
 - Right = D

###Right Player
 - Rotate = Up Arrow
 - Left = Left Arrow
 - Down = Down Arrow
 - Right = Right Arrow

##Dance Mat
The controls are mapped to a single 'DDR' mat with the players intended to face each other.  Each player has thus have 3 'buttons' on their respective side, the buttons in the row in between is split such that the one on the right from the perspective of each player is their rotate button.
 - Start New Game = Start

###Left Player
 - Rotate = "Down Arrow"
 - Left = X
 - Down = "Left Arrow"
 - Right = Triangle

###Right Player
 - Rotate = "Up Arrow"
 - Left = Square
 - Down = "Right Arrow"
 - Right = Circle

#Hardware
The LED Array consists of 24 LED strips, each containing 30 WS2811 LEDs and half a metre in length.  The strips are arranged in a zig-zag pattern with each head of the strip placed closest and connected to the adjacent strip's tail.  This is done to minimise the data wire length between each strip and allows for all LEDs to be connected serially.

The serial connection of all 720 LEDs requires only one data signal to drive the entire display.  For the purposes of the Tetris game, the update rate achieved with this arrangement is sufficient.

A 3D Printed guide was used to lay the strips with the required separation and ensured the strips was placed parallel.

A Teensy3 (3.0) using the Fast_LED library is used to control the LEDs via Pin 0, the Teensy3 receives the image information to be displayed via USB.

A 200/250W power supply was used to power the LED panel.  The Teensy was powered by USB.  Only GND and DATA wires were connected between the Teensy and the LED Panel.

#Software

