 
#include <Servo.h>

Servo myservo;  

// Control and feedback pins
int servoPin = 9;
int feedbackPin = A0;
int pos = 0; 


int current_position = 75;  //CENTRE
int min_left=  75;          //Minimum LEFT
int max_left = 0;           //MAXIMUM LEFT
int min_right = 75;         //Minimum RIGHT
int max_right = 130;        //Maximum RIGHT
String readString; 

 
void setup() 
{ 
  Serial.begin(115200);
  myservo.attach(servoPin); 
  Serial.println("Setup done!");
  myservo.write(50); 
  /*pos = analogRead(feedbackPin);
  Serial.println("POS:"+pos);*/

  

  
}
  
void loop()
{

while(Serial.available()) // Condition: Serial up
  {
    
    char c = Serial.read(); // Reading serial input as char
    readString += c; // Adding serial input to string to allow "if" conditions
    readString = readString.substring(0,1);
    String message = readString + " is pressed  --- position = " + String(current_position);
    Serial.println(message);
    myservo.write(60);    
  

    while(readString == "d") // Right
    {
      readString = "";

      Serial.println("RIGHT Starting position:"+ current_position);
      
      if(current_position < max_right)
      {
        current_position = current_position + 5;
        myservo.write(current_position);  
        Serial.println("RIGHT Ending position: " + current_position);
      }
      else
      {
        myservo.write(max_right); 
        Serial.println("RIGHT MAX position: " + max_right);
        readString = "";
      }
      

       
      
      
      char c = Serial.read();
      readString += c;


    }


    while(readString == "a") // Left
    {
      
      readString = "";
      
      Serial.println("LEFT Current position: "+current_position);
      
      if(current_position > max_left)
      {
        current_position = current_position - 5;
        myservo.write(current_position);  
        Serial.println("LEFT  Ending position: " + current_position);
      }
      else
      {
        myservo.write(max_left); 
        Serial.println("LEFT MAX position: " + max_left);
        readString = "";
      }
      
      char c = Serial.read();
      readString += c;


    }


  /*for (int degree = 0 ; degree <= 150 ; degree++)
  {
    
    Serial.println("Servo Pos: "+degree);
    myservo.write(degree);
  
  }
  Serial.println("=====BREAK=====");

    for (int degree = 150 ; degree >= 00 ; degree--)
  {
    
    Serial.println("Servo Pos: "+degree);
    myservo.write(degree);  
  
  }*/
  readString = "";
  }

} 
