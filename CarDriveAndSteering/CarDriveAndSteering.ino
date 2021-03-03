
#include <Servo.h>


/*
Motor Driver Truth Table

Pololu High-Power Motor Driver 18v15

PWM  DIR OUTA  OUTB   Operation
H     L   L     H     Forward
H     H   H     L     Backward
L     X   L     L     Brake

*/

/*
 * Declare variables
 */
// MOTOR VARIABLES
int break_power = 0;
int current_forward_power = 0;
int current_backward_power = 0;
int PWM = 9;            // PWM 
int DIR = 8;            // DIRECTION
int RESET = 7;          // RESET
int min_power = 80;     // Minimum Power
int max_power = 120;    // Maximum Power

// STEERING VARIABLES
Servo myservo;  
int servoPin = 10;       // PWM Control Pin
int feedbackPin = A0;    // Servo Feedback Pin
int pos = 0;             // Position 

int current_position = 50;  //CURRENT POSITION 
int centre = 50;            //CENTRE
int max_left = 0;           //MAXIMUM LEFT
int max_right = 130;        //MAXIMUM RIGHT

void setup() 
{

    // Create serial port with 115200 connection
    Serial.begin(115200); 
    Serial.println("Car Drive and Steering System setup started..."); 
    setupMotor();
    setupSteering();
    Serial.println("Car Drive and Steering System setup completed.");
  
}

void loop() 
{
  while(Serial.available()) // Condition: Serial up
  { 
    char c = Serial.read();
    switch (c) // Control functions for each combination.
    { 
      case 'w':
        Serial.println("FORWARD");
        Serial.println("============");
        forward();
        Serial.println("============");
        Serial.println("            ");
        break;
      case 's':
        Serial.println("STOP");
        Serial.println("============");
        stopping();
        Serial.println("============");
        Serial.println("            ");
        break;
      case 'e':
        Serial.println("FORWARD-RIGHT");
        Serial.println("            ");
        break;
      case 'd':
        Serial.println("RIGHT");
        Serial.println("============");
        right();
        Serial.println("============");
        Serial.println("            ");
        break;
      case 'c':
        Serial.println("BACKWARD-RIGHT");
        Serial.println("            ");
        break;
      case 'x':
        Serial.println("BACKWARD");
        Serial.println("============");
        backward();
        Serial.println("============");
        Serial.println("            ");
        break;
      case 'z':
        Serial.println("BACKWARD-LEFT");
        Serial.println("            ");
        break;
      case 'a':
        Serial.println("LEFT");
        Serial.println("============");
        left();
        Serial.println("============");
        Serial.println("            ");
        break;
      case 'q':
        Serial.println("FORWARD-LEFT");
        Serial.println("            ");
      break;
    }
  }
}


void setupMotor()
{
    // Setup Motor and instantiate variables
    TCCR1B = TCCR1B & B11111000 | B00000001;  // set timer 1 divisor to     1 for PWM frequency of 31372.55 Hz
    pinMode(PWM, OUTPUT);
    pinMode(DIR, OUTPUT);
    pinMode(RESET, OUTPUT);
    //digitalWrite(DIR, LOW);
    digitalWrite(RESET, HIGH);
    analogWrite(PWM, break_power);
    Serial.println("Motor driver instantiated."); 
}

void setupSteering()
{
    //Setup Servo for steering
    myservo.attach(servoPin); 
    myservo.write(50); 
    /*pos = analogRead(feedbackPin);
    Serial.println("POS:"+pos);*/
    Serial.println("Servo instantiated.");
}

void forward ()
{
      current_backward_power = break_power;
      digitalWrite(DIR, HIGH);
      //digitalWrite(RESET, HIGH);
      if(current_forward_power < min_power)
      {
        current_forward_power = min_power;
      }
      Serial.println("Current forward motor speed:");
      Serial.println(current_forward_power);
      delay(500);
      if(current_forward_power < max_power)
      {
        current_forward_power = current_forward_power + 1;
      }
      analogWrite(PWM, current_forward_power);
      Serial.println("New forward motor speed:");
      Serial.println(current_forward_power);
      //delay(100);
}

void backward ()
{

      current_forward_power = break_power;
      digitalWrite(DIR, LOW);
      //digitalWrite(RESET, HIGH);
      if(current_backward_power < min_power)
      {
        current_backward_power = min_power;
      }
      Serial.println("Current backward motor speed:");
      Serial.println(current_backward_power);
      delay(500);
      if(current_backward_power < max_power)
      {
        current_backward_power = current_backward_power + 1;
      }
      analogWrite(PWM, current_backward_power);
      Serial.println("New backward motor speed:");
      Serial.println(current_backward_power);
      //delay(100);
}

void center()
{
   myservo.write(50); 
}

void right()
{
      Serial.println("RIGHT Starting position:"+ current_position);
      current_position = max_right;
      myservo.write(current_position);  
      Serial.println("RIGHT Ending position: " + current_position);
      delay(500);
      center();
}

void left()
{

      
      Serial.println("LEFT Current position: "+current_position);
      current_position = max_left;
      myservo.write(current_position);  
      Serial.println("LEFT  Ending position: " + current_position);
      delay(500);
      center();
}

void stopping ()
{
  if(current_forward_power > min_power)
  {
      //Gradual breaking in increment of 10.
      for(int i = current_forward_power; i > break_power;i = i-20)
      {
        Serial.println("Gradual breaking:" + i);
        analogWrite(PWM, i);
      }
      analogWrite(PWM, break_power);
  }
  if(current_backward_power > min_power)
  {
      //Gradual breaking in increment of 10.
      for(int i = current_backward_power; i > break_power;i = i-20)
      {
        Serial.println("Gradual breaking:" + i);
        analogWrite(PWM, i);
      }
      analogWrite(PWM, break_power);
  }  


}
