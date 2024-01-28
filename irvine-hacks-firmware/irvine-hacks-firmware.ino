// functions for movement

// counter for how long to drive for, before stopping/switching movement options
// tweak this variable to affect how far the bot drives
const static int movementTimeLimit = 1000;

int incomingByte = 52;
bool moving = false;
int moveCounter = 0;
int currentMovement = 0;

const int ENABLE_RIGHT = 14;
const int ENABLE_LEFT = 15;

// Motor 1
// right side
const int RIGHT_SIDE_1 = 16;
const int RIGHT_SIDE_2 = 17;
// Motor 2
// left side
const int LEFT_SIDE_1 = 18;
const int LEFT_SIDE_2 = 19;

const int ON_PERCENT = 0.78;

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

    // set enable
    pinMode(ENABLE_RIGHT, OUTPUT);
    pinMode(ENABLE_LEFT, OUTPUT);


    // set pin modes of motor
    pinMode(RIGHT_SIDE_1, OUTPUT);
    pinMode(RIGHT_SIDE_2, OUTPUT);
    pinMode(LEFT_SIDE_1, OUTPUT);
    pinMode(LEFT_SIDE_2, OUTPUT);
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
        Serial.println("FORWARD");
        moved = true;
        Forward();
        break;
    case 49:
        // "1"
        Serial.println("BACKWARD");
        moved = true;
        turnBack();
        break;
    case 50:
        // "2"
        Serial.println("TURNLEFT");
        moved = true;
        turnLeft();
        break;
    case 51:
        // "3"
        Serial.println("TURNRIGHT");
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
        // Serial.println(moveCounter);
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

    digitalWrite(RIGHT_SIDE_1, HIGH); // HIGH --> reverse, LOW --> forward
    digitalWrite(RIGHT_SIDE_2, LOW);  // LOW --> reverse, HIGH --> forward

    digitalWrite(LEFT_SIDE_1, HIGH);  // LOW --> forward
    digitalWrite(LEFT_SIDE_2, LOW); // HIGH --> forward

    digitalWrite(ENABLE_RIGHT, HIGH);
    digitalWrite(ENABLE_LEFT, HIGH);
}
void turnBack()
{

    digitalWrite(RIGHT_SIDE_1, HIGH);
    digitalWrite(RIGHT_SIDE_2, LOW);

    digitalWrite(LEFT_SIDE_1, LOW);
    digitalWrite(LEFT_SIDE_2, HIGH);

    digitalWrite(ENABLE_RIGHT, HIGH);
    digitalWrite(ENABLE_LEFT, HIGH);
}

void turnLeft()
{

    digitalWrite(RIGHT_SIDE_1, LOW);
    digitalWrite(RIGHT_SIDE_2, HIGH);

    digitalWrite(LEFT_SIDE_1, LOW);
    digitalWrite(LEFT_SIDE_2, HIGH);

    digitalWrite(ENABLE_RIGHT, HIGH);
    digitalWrite(ENABLE_LEFT, HIGH);
}

void Forward()
{

    digitalWrite(RIGHT_SIDE_1, LOW);
    digitalWrite(RIGHT_SIDE_2, HIGH);

    digitalWrite(LEFT_SIDE_1, HIGH);
    digitalWrite(LEFT_SIDE_2, LOW);

    digitalWrite(ENABLE_RIGHT, HIGH);
    digitalWrite(ENABLE_LEFT, HIGH);
}
void stop()
{
    digitalWrite(ENABLE_RIGHT, LOW);
    digitalWrite(ENABLE_LEFT, LOW);
}