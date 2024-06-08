#include <DHT.h>
#ifdef ESP32
  #include <HTTPClient.h>
  #include <WiFi.h>
#elif defined(ESP8266)
  #include <ESP8266HTTPClient.h>
  #include <ESP8266WiFi.h>
#endif

// Replace with your network credentials
const char* ssid = "Aqilla";
const char* password = "07122017";

// Your server URL
const char* serverName = "http://192.168.1.4:2000/sensor"; // Replace with your Flask server IP

// Create an instance of the DHT11 class.
DHT dht(15, DHT11); // Pin 2 and DHT11

void setup() {
    // Initialize serial communication
    Serial.begin(9600);
    
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
    
    // Initialize the DHT11 sensor
    dht.begin();
}

void loop() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Failed to read from DHT sensor!");
    } else {
        Serial.print("Temperature: ");
        Serial.print(temperature);
        Serial.print(" °C\tHumidity: ");
        Serial.print(humidity);
        Serial.println(" %");

        // Create JSON payload
        String jsonPayload = "{\"temperature\":" + String(temperature) + ", \"humidity\":" + String(humidity) + "}";

        if (WiFi.status() == WL_CONNECTED) {
            HTTPClient http;

            http.begin(serverName);
            http.addHeader("Content-Type", "application/json");

            int httpResponseCode = http.POST(jsonPayload);

            if (httpResponseCode > 0) {
                String response = http.getString();
                Serial.println(httpResponseCode);
                Serial.println(response);
            } else {
                Serial.print("Error on sending POST: ");
                Serial.println(httpResponseCode);
            }
            http.end();
        } else {
            Serial.println("Error in WiFi connection");
        }
    }
    
    delay(2000); // Send a request every 2 seconds
}
