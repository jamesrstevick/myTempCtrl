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

// CMDs   (SI, SD, SH, SE)
const char INCREASE[2] = {0x53, 0x49};
const char DECREASE[2] = {0x53, 0x44};
const char SHIFT[2] = {0x53, 0x48};
const char SET[2] = {0x53, 0x45};

// SET PINS
int incPin = 2;
int decPin = 3;
int shiftPin = 4;
int setPin = 5;

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
void pressButton(int pin)
{
  delay(100);
  digitalWrite(pin, LOW);
  delay(100);
  digitalWrite(pin, HIGH);
  delay(150);
}

// MAIN LOOP WAITS FOR CMD
void loop()
{

  pinsOff();
  byte cmd[2];

  while (Serial.available() < 2)
  {
    pinsOff();
  }
  cmd[0] = Serial.read();

  if (cmd[0] == 0x53)
  {
    if (Serial.available())
    {

      cmd[1] = Serial.read();

      if (cmd[1] == 0x45)
      {
        pressButton(setPin);
        pinsOff();
        Serial.flush();
      }
      else if (cmd[1] == 0x48)
      {
        pressButton(shiftPin);
        pinsOff();
        Serial.flush();
      }
      else if (cmd[1] == 0x44)
      {
        pressButton(decPin);
        pinsOff();
        Serial.flush();
      }
      else if (cmd[1] == 0x49)
      {
        pressButton(incPin);
        pinsOff();
        Serial.flush();
      }
      else
      {
        pinsOff();
        Serial.flush();
      }
    }
    else
    {
      pinsOff();
      Serial.flush();
    }
  }
  else
  {
    pinsOff();
    Serial.flush();
  }
}
