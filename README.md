# IrvineHacks-2024-Software

## Inspiration
A set of members in the group were heavily invested in previous projects that incorporated IoT and hardware development. They really enjoyed the thrill of attempting new innovative projects that they have less experience in. 

## What it does
- The companion Amelia is capable of speech-to-text, text-to-speech, photo-to-speech, and speech-to-photo processes. 
- We are giving "gemini" the ability to see, hear, talk, and walk.
- Amelia is able to speak to you about landmarks all over the worl. It is your own personal tour guide!
- Amelia is able to follow you around using her camera and motors to see and move towards you.
- She can also analyze photos that you show her! If you are confused about where a certain landmark or location is, you can show her the picture and she will tell you.

## How we built it
We divided our tasks into two main sets of tasks divided by hardware and software. 

The hardware component of our project was focused on building a motorized companion, which we named Amelia. Amelia was built using a Raspberry Pi as the central processing unit.

1. Motors: We used motors to enable Amelia to move around. The motors were controlled by the Raspberry Pi through a motor driver circuit. We wrote a Python script to control the motors based on the inputs received from the software component.

2. Eyes: Amelia's eyes were implemented using a camera module connected to the Raspberry Pi. This allowed Amelia to capture images and videos, which were then processed by the software component for various tasks such as object recognition and tracking.

3. Mouth: For Amelia's mouth, we used a speaker connected to the Raspberry Pi. The speaker was used to output the text-to-speech conversions done by the software component, allowing Amelia to "speak".

4. Ears: Amelia's ears were implemented using a microphone module connected to the Raspberry Pi. The microphone captured audio input, which was then converted to text by the software component for processing.

The hardware components were carefully integrated to ensure smooth communication and coordination. The Raspberry Pi acted as the bridge between the hardware and software components, receiving inputs from the hardware, processing it with the help of the software, and then sending the appropriate commands back to the hardware.

## Challenges we ran into
- Our hardware team faced several software challenges. One major one was upgrading the software of of the raspberry pi and wiring of the chips. Many compatiblity issues between all three operating systems being used on the same development team. With enough effor and debugging, we were able to overcome these hurdles.

- Software team had difficulty utlizing the Raspberry Pi's CPU and GPU for tasks such as transcription and translation. To overcome this, we decided to leverage APIs and cloud technology. We offloaded heavy processing tasks and improved the performance of our product. 

## Accomplishments that we're proud of
- We are very proud of the fact that we all stepped out of our comfort zones and attempted to do something new to each one of us. Face many constraints and hurdles headone and dealt with them one by one. 

## What we learned
- Each member learned various things ranging from hardware to software. Some members learned how to <insert hardware info here>
Other members learned how to utilze ai / nlp tools in an application. More useful tools to add to their toolbelts as web devs and software engineer. 


## What's next for Amelia
- To improve her performance beyond basic functionaliy. 
- Improve her hardware enough to be capable of faster responses from user requests. 

# Resources Used
* Pi Serial UART Communication: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c
    * the weird 2 second delay: https://stackoverflow.com/a/57126149
* If you get serial permission denied: https://askubuntu.com/questions/210177/serial-port-terminal-cannot-open-dev-ttys0-permission-denied
    * First, connect the ground betwee nthe pi and the arduino
    * Then, run `sudo chmod 666 /dev/ttyS0`
    * Remember to match the baud rates: `stty -F /dev/ttyS0 <baud_rate>`
* Installing python versions, using pyenv: https://github.com/pyenv/pyenv
    * Use `pyenv global <version>` to swap versions

# Installation and Deployment
* Our code works with Python version 3.8.0
* Note: `pyaudio` must be installed. It is a platform/OS dependent package.
    * Windows
        * You will get an error in `Pyaudio`
        * Run `pip install pipwin`
        * Run `pipwin install pyaudio`
    * Raspberry Pi
        * Basically, follow this: https://medium.com/@niveditha.itengineer/learn-how-to-setup-portaudio-and-pyaudio-in-ubuntu-to-play-with-speech-recognition-8d2fff660e94
        * Run `sudo apt-get install python-pyaudio python3-pyaudio`
        * Run `sudo apt-get install libasound-dev`
        * Run `pip install pyaudio`