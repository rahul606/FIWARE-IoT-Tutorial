
//NOTE: The values assigned in this example must be changed following the application desired by the user and the specified pattern

#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>
#include <DHT.h>

//libraries needed for the application, in which libraries that do not come in the Arduino installation can be found in these links:
// DHT = https://github.com/adafruit/DHT-sensor-library
// PubSubClient = https://github.com/knolleary/pubsubclient

//defining pins for the LED and for the sensor
#define DHT21_PIN 2
#define LED_PIN   3


//defining in the DHT library the type of sensor that will be used
#define DHTTYPE DHT21   // AM2301

//defining Delay times for the connection to the server, and the time between measurements
#define ERROR_DELAY   2000
#define SUCCESS_DELAY 300000


//creating variables to store the time that has passed since the last event
unsigned long lastEventTime;
boolean sendMeasurementSuccess;

//MAC address setting, it must be changed with the appropriate values for the user connection
byte mac[] = { 0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };

//setting the server's IP address
IPAddress server(10, 7, 49, 163);

/**
//Withdraw comments if you want to manually assign your IP address
IPAddress ip(10, 10, 1, 2);
IPAddress localDns(10, 10, 1, 1);
IPAddress gateway(10, 10, 1, 1);
IPAddress subnet(255, 255, 255, 0);
**/

//Callback function header
void callback(char* topic, byte* payload, unsigned int length);

//instantiation of the EthernetClient, PubSubClient and DHT classes
EthernetClient ethClient;
PubSubClient client(server, 1883, callback, ethClient);
DHT dht(DHT21_PIN, DHTTYPE);

//creation of constant variables for sending commands to the device

const char* cmdAnswerTopic = "/cd2fda18947911e7a694fc15b4d94103/STELA_DHT/cmdexe"; //this assignment is made by following the "/API_KEY/ID_DEVICE/cmdexe"
const char* payloadOn = "STELA_DHT@change_state|ON";//this assignment is made following the "ID_DEVICE@ACTION_NAME|RESULT"
const char* payloadOff = "STELA_DHT@change_state|OFF";//this assignment is made following the "ID_DEVICE@ACTION_NAME|RESULT"
const char* payloadOk = "STELA_DHT@change_state|OK";//this assignment is made following the "ID_DEVICE@ACTION_NAME|RESULT"
const char* payloadError = "STELA_DHT@change_state|ERROR";//this assignment is made following the "ID_DEVICE@ACTION_NAME|RESULT"

void setup() {
  Serial.begin(115200); //starts the serial port, to monitor the measurements via the Arduino serial monitor
  delay(2000);
  pinMode(LED_PIN, OUTPUT);

  Ethernet.begin(mac); //DHCP (auto IP)
  //Ethernet.begin(mac, ip, localDns, gateway, subnet); //Manual IP
  printIPAddress();

  delay(1500);  //Allow the hardware to sort itself out

  lastEventTime = millis();
  sendMeasurementSuccess = false;
}

//prints the client's IP address on the serial monitor

void printIPAddress() {
  Serial.print("IP address: ");
  for (byte thisByte = 0; thisByte < 4; thisByte++) {
    Serial.print(Ethernet.localIP()[thisByte], DEC);
    Serial.print(".");
  }
  Serial.println();
}

//checks payload and sends commands to device according to payload
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.println("] ");

  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if (checkPayloadEqual(payloadOn, (char*)payload, length)) {
    Serial.println("ON");
    digitalWrite(LED_PIN, HIGH);
    client.publish(cmdAnswerTopic, payloadOk);

  } else if (checkPayloadEqual(payloadOff, (char*)payload, length)) {
    Serial.println("OFF");
    digitalWrite(LED_PIN, LOW);
    client.publish(cmdAnswerTopic, payloadOk);

  } else {
    Serial.println("UNKNOWN");
    client.publish(cmdAnswerTopic, payloadError);
  }

  Serial.println("Answer sent");
}

boolean checkPayloadEqual(const char* payload, char* payloadInput, unsigned int inputPayloadLength) {
  if (strlen(payload) != inputPayloadLength) {
    return false;
  }

  for(int i = 0; i < inputPayloadLength; i++) {
    if(payload[i] != payloadInput[i]) {
      return false;
    }
  }
  return true;
}

//sends the measurement made by the device to the database

void publishMeasurements() {
  char strHumidity[6];
  char strTemperature[6];

  char measurementPayloadBuf[40];

  int chk = dht.read(DHT21_PIN);
  switch (chk){
    case true:
      dtostrf(dht.readHumidity(), 4, 2, strHumidity);
      dtostrf(dht.readTemperature(), 4, 2, strTemperature);

      sprintf(measurementPayloadBuf, "h|%s|t|%s", strHumidity, strTemperature);
      Serial.println(measurementPayloadBuf);

      client.publish("/cd2fda18947911e7a694fc15b4d94103/STELA_DHT/attrs", measurementPayloadBuf);
   //command made using the default publish("/API_KEY/ID_DEVICE/attrs", "ATTR_01|VAL_01|ATTR_02|VAL_02")

      Serial.println("Mesurement sent!");
      sendMeasurementSuccess = true;
      break;

    default:
      Serial.println("Failed to read sensor. Trying again later.");
      sendMeasurementSuccess = false;
      break;
  }
  lastEventTime = millis();
}

//attempts to connect to the server in the event of a connection failure
void reconnect() {


  while (!client.connected()) {
    Serial.println("Connecting to server...");
    if (client.connect("arduinoClient")) {
      Serial.println("Connected!");

      Serial.println("Subscribing LED command topic...");
      if(client.subscribe("/cd2fda18947911e7a694fc15b4d94103/STELA_DHT/cmd"))

      {
        Serial.println("Successfully subscribed to topic!");
      } else {
        Serial.println("Error while subscribing to topic.");
      }
    } else {
      Serial.println("Connection failed. Trying again in 2 seconds.");
      delay(2000); // Wait until try again
    }
  }
}

void loop() {
  if (client.connected()) {
    unsigned long currentTime = millis();
    unsigned long elapsedTime = abs(currentTime - lastEventTime);

    if ((sendMeasurementSuccess == true && elapsedTime >= SUCCESS_DELAY)
        || (sendMeasurementSuccess == false && elapsedTime >= ERROR_DELAY)) {
      publishMeasurements();
    }
    client.loop();
  } else {
    reconnect();
  }
  client.loop();
}
