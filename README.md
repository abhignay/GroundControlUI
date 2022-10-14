# Ground Control UI

## About
This Ground Control UI is the software part of the ground station (hardware being an Ebyte E32 hooked up to a Teensy 3.2) that will be used to display and update telemetry in real-time, it can also be used to control a rocket.

The frontend for the UI is written in Python with the PyQt5 and PyQtGraph libraries (you will need to install these libraries)
![image](https://user-images.githubusercontent.com/74813604/195796788-8944f818-ab9f-4a6a-946b-4890dd9fc1b4.png)

## Code Explanation
The `GUI` class has all the functions that create the main GUI window, creates the boxes that display data/graphs and updates the it with telemetry data.
The `def __init__():` function creates and starts QTimer and runs the window setup function. The `window_setup():` function creates the GUI window and runs all the other functions. Your telemetry data should follow the order mentioned on `line 469`

## A couple other things
I've only tested this GUI on Ubuntu 22.04, so let me know if you have any problems using it with other platforms (Win, Mac, other Linux distros)

Feel free to open up an issue if you have any questions. comments, or feedback

## License
Code in this repository is licensed under the terms of the MIT license.
