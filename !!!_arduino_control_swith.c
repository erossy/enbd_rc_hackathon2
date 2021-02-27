String readString;

void setup() {
  Serial.begin(9600);
  delay(500);
}
void loop() {
  while(Serial.available()){ // Condition: Serial up
    char c = Serial.read();
    switch (c) { // add necessary control functions for each direction.
      case 'w':
        Serial.println("FORWARD");
        break;
      case 's':
        Serial.println("STOP");
        break;
      case 'e':
        Serial.println("FORWARD-RIGHT");
        break;
      case 'd':
        Serial.println("RIGHT");
        break;
      case 'c':
        Serial.println("BACKWARD-RIGHT");
        break;
      case 'x':
        Serial.println("BACKWARD");
        break;
      case 'z':
        Serial.println("BACKWARD-LEFT");
        break;
      case 'a':
        Serial.println("LEFT");
        break;
      case 'q':
        Serial.println("FORWARD-LEFT");
    }
  }
}
