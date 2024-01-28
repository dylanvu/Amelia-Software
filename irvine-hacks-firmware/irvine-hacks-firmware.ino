// functions for movement

// counter for how long to drive for, before stopping/switching movement options
// tweak this variable to affect how far the bot drives
const static int movementTimeLimit = 1000;

int incomingByte = 52;
bool moving = false;
int moveCounter = 0;
int currentMovement = 0;

const int ENABLE = 2;
// Motor 1
const int AA1 = 3;
const int AA2 = 4;
// Motor 2
const int AA3 = 18;
const int AA4 = 19;

// function declarations
void turnRight();
void turnLeft();
void Forward();
void turnBack();
void stop();

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

        // set move counter to 0
        moveCounter = 0;

        // set current movement to be this command
        currentMovement = incomingByte;
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
        // Serial.println("FORWARD");
        moved = true;
        Forward();
        break;
    case 49:
        // "1"
        // Serial.println("BACKWARD");
        moved = true;
        turnBack();
        break;
    case 50:
        // "2"
        // Serial.println("TURNLEFT");
        moved = true;
        turnLeft();
        break;
    case 51:
        // "3"
        // Serial.println("TURNRIGHT");
        moved = true;
        turnRight();
        break;
    case 52:
        // "4"
        // Serial.println("WAIT");
        moved = true;
        stop();
        break;
    case 53:
        // "5"
        // meant for debugging UART communication
        digitalWrite(2, HIGH);
        break;
    default:
        // Serial.println("UNKNOWN");
        // TODO: make it wait
        moved = false;
        stop();
        // digitalWrite(2, HIGH);
        break;
    }

    if (moved)
    {
        // increment movement counter
        moveCounter++;
        Serial.println(moveCounter);
    }

    // check if we are done with the movement
    if (moveCounter > movementTimeLimit)
    {
        Serial.println("Done");
        // stop moving
        moving = false;
        moveCounter = 0;
        currentMovement = -1;
    }
}

void turnRight()
{

    digitalWrite(AA1, HIGH);
    digitalWrite(AA2, LOW);

    digitalWrite(AA3, LOW);
    digitalWrite(AA4, HIGH);

    digitalWrite(ENABLE, HIGH);
}
void turnBack()
{

    digitalWrite(AA1, HIGH);
    digitalWrite(AA2, LOW);

    digitalWrite(AA3, HIGH);
    digitalWrite(AA4, LOW);

    digitalWrite(ENABLE, HIGH);
}

void turnLeft()
{

    digitalWrite(AA1, LOW);
    digitalWrite(AA2, HIGH);

    digitalWrite(AA3, HIGH);
    digitalWrite(AA4, LOW);

    digitalWrite(ENABLE, HIGH);
}

void Forward()
{

    digitalWrite(AA1, LOW);
    digitalWrite(AA2, HIGH);

    digitalWrite(AA3, LOW);
    digitalWrite(AA4, HIGH);

    digitalWrite(ENABLE, HIGH);
}
void stop()
{
    digitalWrite(ENABLE, LOW);
}