/* 
Arduino controller for Benchmark myTemp Temperature Chamber
Clarity Movement Co.
James Stevick

Control Arduino with Python
Press 1 of 4 myTemp buttons using CMDs:
-Set: \x53\x45
-Shift: \x53\x48
-Decrease: \x53\x44
-Increase: \x53\x49

1. Connect Arduino to computer (powered usb)
2. Wait 10 seconds
3. Turn on Benchmark myTemp
4. Make sure "Set" is not on Temp or Time
5. Send CMDs from Python
*/

#define COMMAND_TIMEOUT 1000

// CMDs   (SI, SD, SH, SE)
#define COMMAND_HEADER 0x53
#define COMMAND_INCREASE 0x49
#define COMMAND_DECREASE 0x44
#define COMMAND_SHIFT 0x48
#define COMMAND_SET 0x45

// SET PINS
#define incPin 2
#define decPin 3
#define shiftPin 4
#define setPin 5

// INTIALIZE
void setup()
{

  // Set relay pins as digital logic outputs
  pinMode(incPin, OUTPUT);
  pinMode(decPin, OUTPUT);
  pinMode(shiftPin, OUTPUT);
  pinMode(setPin, OUTPUT);

  // Turn off all pins - START WITH SET - HIGH IS OFF
  pinsOff();

  Serial.begin(9600);
}

// TURN OFF ALL BUTTONS
void pinsOff()
{
  digitalWrite(setPin, HIGH);
  digitalWrite(shiftPin, HIGH);
  digitalWrite(decPin, HIGH);
  digitalWrite(incPin, HIGH);
}

// SIMULATE PRESSED BUTTON
void pressButton(uint8_t pin)
{
  delay(100);
  digitalWrite(pin, LOW);
  delay(100);
  digitalWrite(pin, HIGH);
  delay(150);
}

uint8_t cmd[2];
unsigned long t0;

// MAIN LOOP WAITS FOR CMD
void loop()
{

  pinsOff();

  Serial.flush();

  while (true)
  {
    while (!Serial.available())
    {
    }

    t0 = millis();
    while (Serial.available() < 2)
    {
      if (millis() - t0 > COMMAND_TIMEOUT)
      {
        Serial.read();
        break;
      }
    }
    if (Serial.available() >= 2)
    {
      cmd[0] = Serial.read();
      cmd[1] = Serial.read();
      break;
    }
  }

  if (cmd[0] == COMMAND_HEADER)
  {

    if (cmd[1] == COMMAND_SET)
    {
      pressButton(setPin);
    }
    else if (cmd[1] == COMMAND_SHIFT)
    {
      pressButton(shiftPin);
    }
    else if (cmd[1] == COMMAND_DECREASE)
    {
      pressButton(decPin);
    }
    else if (cmd[1] == COMMAND_INCREASE)
    {
      pressButton(incPin);
    }
  }
}