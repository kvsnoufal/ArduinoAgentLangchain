/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/
#include <Servo.h> 
int servoCoffeePin = 3;
int servoSugarPin = 4;
int servoSpoonPin1 = 5;
int servoSpoonPin2 = 6;
int waterPin = 13;
int milkPin = 12;
String command;
Servo ServoCoffee;
Servo ServoSugar;
Servo ServoSpoon1;
Servo ServoSpoon2;
// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(milkPin,OUTPUT);
  digitalWrite(milkPin,HIGH);
  pinMode(waterPin,OUTPUT);
  digitalWrite(waterPin,HIGH);
  ServoCoffee.attach(servoCoffeePin);
  ServoSugar.attach(servoSugarPin);
  ServoSpoon1.attach(servoSpoonPin1);
  ServoSpoon2.attach(servoSpoonPin2);
  ServoCoffee.write(30);
  ServoSugar.write(30);
  ServoSpoon1.write(0);
  ServoSpoon2.write(60);

  
  Serial.begin(9600);
}

// the loop function runs over and over again forever
void loop() {
  // digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  // delay(1000);                      // wait for a second
  // digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  // delay(1000);                      // wait for a second
  // ServoCoffee.write(30);
  // ServoSugar.write(30);
  // delay(1000);
  // ServoCoffee.write(150);
  // ServoSugar.write(150);
  // delay(1000);
  
  
  if (Serial.available()){
    command = Serial.readStringUntil("\n");
    command.trim();
    if (command.equals("coffee")){
      for (int i = 0; i<10; i++){
        ServoCoffee.write(150);
     
        delay(300);
        ServoCoffee.write(30);
     
        delay(300);

      }
    }
    if (command.equals("sugar")){
     
      for (int i = 0; i<2; i++){
   
        ServoSugar.write(150);
        delay(300);
  
        ServoSugar.write(30);
        delay(300);

      }
    }
    if (command.equals("spoon")){
      
  ServoSpoon1.write(100);
  for (int i=0;i<5;i++){
    delay(500);
    ServoSpoon2.write(120);
    delay(500);
    ServoSpoon2.write(60);
  }
  ServoSpoon1.write(0);
  
    }
    if(command.equals("milk")){
      digitalWrite(milkPin,LOW);
      delay(2000);
      digitalWrite(milkPin,HIGH);
    }

    if(command.equals("water")){
      digitalWrite(waterPin,LOW);
      delay(2000);
      digitalWrite(waterPin,HIGH);
    }
  
    
  }
  
}
