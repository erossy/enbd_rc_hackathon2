#include <Servo.h>

// MOTOR VARIABLES
int break_power = 15;
int current_forward_power = 15;
int current_backward_power = 15;
int PWM = 11;            // PWM
int DIR = 8;            // DIRECTION
int RESET = 7;          // RESET
int min_power = 20;     // Minimum Power
int max_power = 60;    // Maximum Power
int dir_value = HIGH;


// STEERING VARIABLES
Servo myservo;
int servoPin = 10;       // PWM Control Pin
int feedbackPin = A0;    // Servo Feedback Pin
int pos = 0;             // Position

int current_position = 50;  //CURRENT POSITION
int centre = 50;            //CENTRE
int max_left = 0;           //MAXIMUM LEFT
int max_right = 100;        //MAXIMUM RIGHT

void setup() {
  myservo.attach(servoPin);
  myservo.write(centre);
  Serial.println("Servo instantiated.");
  TCCR2B = TCCR2B & B11111000 | B00000001;
  Serial.begin(115200);
  delay(500);
  analogWrite(PWM, break_power);
  pinMode(PWM, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(RESET, OUTPUT);
  digitalWrite(RESET, HIGH);
  Serial.println("Motor driver instantiated.");
}
void loop() {
  while(Serial.available()){ // Condition: Serial up
    char c = Serial.read();
    switch (c) { // add necessary control functions for each direction.
      case 'w': // insert drive forward here
        Serial.println("FORWARD");
        if (current_position != centre){
          current_position = centre;
          myservo.write(current_position);
        }
        if (dir_value != HIGH){
          dir_value = HIGH;
           digitalWrite(DIR, dir_value);
        }
        if(current_forward_power < 20){
          current_forward_power = 20; // Mikhail's patented smoothness magic
          analogWrite(PWM,current_forward_power);
        }
        if(current_forward_power < max_power){
          current_forward_power = current_forward_power + 1;
          analogWrite(PWM,current_forward_power);
          Serial.println("New forward power: " + current_forward_power);
        }
        break;
      //
      case 's': // stop (can be optimized)
        Serial.println("STOP");
        if (current_position != centre){
          current_position = centre;
          myservo.write(current_position);
        }
        analogWrite(PWM,break_power);
        current_forward_power = break_power;
        current_backward_power = break_power;
        break;
      //
      case 'e': // insert forward-right function here
        Serial.println("FORWARD-RIGHT");
        if (dir_value != HIGH){
          dir_value = HIGH;
           digitalWrite(DIR, dir_value);
        }
        if(current_forward_power < 20){
          current_forward_power = 20; // Mikhail's patented smoothness magic
          analogWrite(PWM,current_forward_power);
        }
        if (current_position != max_right){
          current_position = max_right;
          myservo.write(current_position);
        }
        if(current_forward_power < max_power){
          current_forward_power = current_forward_power + 1;
          analogWrite(PWM,current_forward_power);
          Serial.println("New forward power: " + current_forward_power);
        }
        break;
      //
      case 'd': // insert right function here
        Serial.println("RIGHT");
        analogWrite(PWM,break_power);
        current_forward_power = break_power;
        current_backward_power = break_power;
        if (current_position != max_right){
          current_position = max_right;
          myservo.write(current_position);
        }
        break;
      case 'c': // insert backward-right function here
        Serial.println("BACKWARD-RIGHT");
        if (dir_value != LOW){
          dir_value = LOW;
           digitalWrite(DIR, dir_value);
        }
        if(current_backward_power < 20){
          current_backward_power = 20; // Mikhail's patented smoothness magic
          analogWrite(PWM,current_backward_power);
        }
        if (current_position != max_right){
          current_position = max_right;
          myservo.write(current_position);
        }
        if(current_backward_power < max_power){
          current_backward_power = current_backward_power + 1;
          analogWrite(PWM,current_backward_power);
          Serial.println("New forward power: " + current_backward_power);
        }
        break;
      case 'x':
        Serial.println("BACKWARD");
        if (current_position != centre){
          current_position = centre;
          myservo.write(current_position);
        }
        if (dir_value != LOW){
          dir_value = LOW;
           digitalWrite(DIR, dir_value);
        }
        if(current_backward_power < 20){
          current_backward_power = 20; // Mikhail's patented smoothness magic
          analogWrite(PWM,current_backward_power);
        }
        if(current_backward_power < max_power){
          current_backward_power = current_backward_power + 1;
          analogWrite(PWM,current_backward_power);
          Serial.println("New backward power: " + current_backward_power);
        }
        break;
      case 'z':
        Serial.println("BACKWARD-LEFT");
        if (dir_value != LOW){
          dir_value = LOW;
           digitalWrite(DIR, dir_value);
        }
        if(current_backward_power < 20){
          current_backward_power = 20; // Mikhail's patented smoothness magic
          analogWrite(PWM,current_backward_power);
        }
        if (current_position != max_left){
          current_position = max_left;
          myservo.write(current_position);
        }
        if(current_backward_power < max_power){
          current_backward_power = current_backward_power + 1;
          analogWrite(PWM,current_backward_power);
          Serial.println("New forward power: " + current_backward_power);
        }
        break;
      case 'a':
        Serial.println("LEFT");
        analogWrite(PWM,break_power);
        current_forward_power = break_power;
        current_backward_power = break_power;
        if (current_position != max_left){
          current_position = max_left;
          myservo.write(current_position);
        }
        break;
      case 'q':
        Serial.println("FORWARD-LEFT");
        if (dir_value != HIGH){
          dir_value = HIGH;
           digitalWrite(DIR, dir_value);
        }
        if(current_forward_power < 20){
          current_forward_power = 20; // Mikhail's patented smoothness magic
          analogWrite(PWM,current_forward_power);
        }
        if (current_position != max_left){
          current_position = max_left;
          myservo.write(current_position);
        }
        if(current_forward_power < max_power){
          current_forward_power = current_forward_power + 1;
          analogWrite(PWM,current_forward_power);
          Serial.println("New forward power: " + current_forward_power);
        }
    }
  }
}
