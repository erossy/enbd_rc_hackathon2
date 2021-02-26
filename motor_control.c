#include <wiringPi.h>
#include <stdio.h>

int current_power = 0;
int enA = 1;
int in1 = 4; //
int in2 = 5;
int min_power = 230;
int max_power = 255;
String readString;

void setup()
{
 //TCCR1B = TCCR1B & B11111000 | B00000001;
  pwmSetClock(1920);
  pwmSetRange(max_power);
  delay(1);
  pinMode(enA, OUTPUT);
  //pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  //pinMode(in3, OUTPUT);
  //pinMode(in4, OUTPUT);
  Serial.begin(9600);
  Serial.println("serial test start"); //test
}

void loop()
{
  while(Serial.available()) // Condition: Serial up
  {
    char c = Serial.read(); // Reading serial input as char
    readString += c; // Adding serial input to string to allow "if" conditions
    String message = readString + " is pressed  --- pwm power = " + String(current_power);
    Serial.println(message);
  Serial.println(readString);
  while (current_power > 0 && readString != "w" && readString != "s") // default velocity
  {
      //digitalWrite(in1, LOW);
      //digitalWrite(in2, LOW);
      //current_power = 0;
      //analogWrite(enA, current_power);
      //String message = "No interesting keys are pressed... idling" + String(current_power);
      //Serial.println(message);
      //char c = Serial.read();
      //readString += c;
   }
    while(readString == "w") // Forward
    {
      readString = "";
      digitalWrite(in1, HIGH);
      digitalWrite(in2, HIGH);
      if(current_power < min_power)
      {
        current_power = min_power;
      }
      if(current_power < max_power)
      {
        current_power = current_power + 1;
      }
      else {}
      pwmWrite(enA, current_power);
      Serial.println("New motor speed:");
      Serial.println(current_power);
            char c = Serial.read();
      readString += c;
    }
    while(readString == "s") // Backward
    {
      readString = "";
      digitalWrite(in1, LOW);
      digitalWrite(in2, HIGH);
      if(current_power < min_power)
      {
        current_power = min_power;
      }
      Serial.println("Backward velocity cycle:");
      Serial.println(readString);
      Serial.println("Current motor speed:");
      Serial.println(current_power);
      if(current_power < max_power)
      {
        current_power = current_power + 1;
      }
      else {}
      pwmWrite(enA, current_power);
      Serial.println("New motor speed:");
      Serial.println(current_power);
      char c = Serial.read();
      readString += c;
    }
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  current_power = 0;
  pwmWrite(enA, current_power);
  readString = "";
  }
}
