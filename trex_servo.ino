#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

#ifndef APSSID
#define APSSID "PROJ_Trex"
#define APPSK "Google"
#endif

Servo myservo;
ESP8266WebServer server(80);
String command;
int speedCar = 1024;
const char *ssid = APSSID;
const char *password = APPSK;
const int channel = 1;
bool hidden = false;
const int  max_connection = 1;
int ledPin = 2; //GPIO16 ---D0 of NodeMcu
int pos = 0;



void setup() {
  // put your setup code here, to run once:
  myservo.attach(2);
  delay(1000);
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  Serial.println();
  Serial.print("Configuring access point...");
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password, channel, hidden, max_connection);
  delay(100);
  
  IPAddress Ip(192,168,5,1);
  IPAddress NMask(255, 255, 255, 0);
  WiFi.softAPConfig(Ip, Ip, NMask);

  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);
  server.on( "/", HTTP_handleRoot);
  server.onNotFound (HTTP_handleRoot);
  //server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
  myservo.write(0);
 
}

void jump(){
  myservo.write(15);
  delay(1);
  myservo.write(0);
}
void idle() {
  Serial.println("idle");
}


void HTTP_handleRoot(void) {

if( server.hasArg("State") ){
       Serial.println(server.arg("State"));
  }
  server.send ( 200, "text/html", "<title>connected</title>" );
  delay(1);
}

void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();
  
  command  = server.arg("State");
  if (command == "J") jump();
  else if (command == "I") idle();
  
  }
