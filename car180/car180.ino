 
String readString; 

 
void setup() 
{ 
  Serial.begin(9600); 
}
  
void loop()
{

while(Serial.available()) // Condition: Serial up
  {
    
    char c = Serial.read(); // Reading serial input as char
    readString += c; // Adding serial input to string to allow "if" conditions
    String message = readString + " is pressed  --- position = ";
    Serial.println(message);
    readString= "";
  }

} 
