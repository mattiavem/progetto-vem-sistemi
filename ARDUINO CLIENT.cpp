#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <DHT.h>

#define DHTPIN 6
#define DHTTYPE DHT22


byte mac[] = { 0x90, 0xAA, 0xDA, 0x01, 0x02, 0x03};
IPAddress ip(192, 168, 179, 60);

//creo un ip address per il raspberry
IPAddress ip_remote(192, 168, 789, 80);
//creo una porta per la scheda Arduino
unsigned int localPort = 20006; 

char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
char chrBuffer[11];

//altre variabili 
String strTempUmid = "";
byte ciclo = 0;

// Creo degli oggetti per l'utilizzo di udp e del 
//sensore dht
EthernetUDP Udp;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  //inizializzo lo shield mkr eth
  Ethernet.init(5);

  //inizializzo la scheda di rete
  Ethernet.begin(mac, ip);

  //inizializzo la seriale
  Serial.begin(9600);
  
  // verifico la ethernet shield
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("MKR ETH non presente o configurata in modo errato!");
    while (true) {
      delay(1);
    }
  }

  //inizializzo l'oggetto udp
  Udp.begin(localPort);
  //inizializzo l'oggetto dht
  dht.begin();
}

void loop() {

  //verifico presenza pacchetti udp in arrivo
  int packetSize = Udp.parsePacket();
  
  //se coi sono pacchetti
  if (packetSize) {
    //Serial.println(packetSize);
    //leggo i pacchetti e gli inserisco nell'array di char
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    //printo i dati ricevuti
    Serial.println(packetBuffer);
  }

  //leggo umidità e temperatura dal sensore dht
  float h = dht.readHumidity();