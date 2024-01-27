// size of the movement queue
const static int queueSize = 100;

// counter for how long to drive for, before stopping/switching movement options
// tweak this variable to affect how far the bot drives
const static int movementTimeLimit = 1000;

// queue holding movement options
int movementQueue[queueSize];
// where the movement is right now
int queueEnd = 0;
int queueBegin = 0;

int incomingByte = 52;
bool moving = false;
int moveCounter = 0;
int currentMovement = 0;

void setup()
{
    Serial.begin(9600);
    Serial.println("Ready to move!");
    // DEBUG UART
    pinMode(2, OUTPUT);
}

void loop()
{
    // is there an incoming command?
    if (Serial.available() > 0)
    {
        // read the incoming byte:
        incomingByte = Serial.read();

        // filter out the newline
        if (incomingByte == 10)
        {
            return;
        }

        Serial.print("I received: ");
        Serial.println(incomingByte);
        // are we moving?
        if (moving)
        {
            // add to the movement queue
            movementQueue[queueEnd] = incomingByte;
            // increment movementQueue up
            // TODO: check for overflow
            queueEnd = (queueEnd + 1) % queueSize;
        }
        else
        {
            // set move counter to 0
            moveCounter = 0;

            // set current movement to be this command
            currentMovement = incomingByte;
        }
    }

    // execute current movement

    // commands:
    // these numbers are sent as ascii characters!
    // 0 sent (48) -> "FORWARD"
    // 1 sent (49) -> "BACKWARD"
    // 2 sent (50) -> "TURNLEFT"
    // 3 sent (51) -> "TURNRIGHT"
    // 4 sent (52) -> "WAIT"

    // TODO: tie the movement functions to each case
    bool moved = false;
    switch (currentMovement)
    {
    case 48:
        // "0"
        Serial.println("FORWARD");
        moved = true;
        break;
    case 49:
        // "1"
        Serial.println("BACKWARD");
        moved = true;
        break;
    case 50:
        // "2"
        Serial.println("TURNLEFT");
        moved = true;
        break;
    case 51:
        // "3"
        Serial.println("TURNRIGHT");
        moved = true;
        break;
    case 52:
        // "4"
        Serial.println("WAIT");
        moved = true;
        break;
    case 53:
        // "5"
        // meant for debugging UART communication
        digitalWrite(2, HIGH);
        break;
    default:
        // Serial.println("UNKNOWN");
        // TODO: make it wait
        // digitalWrite(2, HIGH);
        break;
    }

    if (moved)
    {
        // increment movement counter
        moveCounter++;
    }

    // check if we are done with the movement
    if (moveCounter > movementTimeLimit)
    {
        // stop moving
        moveCounter = 0;
        currentMovement = -1;
        // check if queue is empty
        if (queueEnd != queueBegin)
        {
            // not empty
            // move queueBegin up
            queueBegin++;
            // set the next movement
            currentMovement = movementQueue[queueBegin];

            // set current movement to be this command
            currentMovement = incomingByte;
        }
    }
}