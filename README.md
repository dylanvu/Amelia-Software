# IrvineHacks-2024-Software

## Inspiration

## What it does

## How we built it

## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for Amelia

# Resources Used
* Pi Serial UART Communication: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c
* If you get serial permission denied: https://askubuntu.com/questions/210177/serial-port-terminal-cannot-open-dev-ttys0-permission-denied
    * First, connect the ground betwee nthe pi and the arduino
    * Then, run `sudo chmod 666 /dev/ttyS0`
    * Remember to match the baud rates: `stty -F /dev/ttyS0 <baud_rate>`
* Installing python versions, using pyenv: https://github.com/pyenv/pyenv
    * Use `pyenv global <version>` to swap versions