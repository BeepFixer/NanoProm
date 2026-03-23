#include <Wire.h>

#define EEPROM_ADDR   0x54  // Xbox onboard
#define EEPROM_ADDR2  0x50  // Standalone EEPROM
#define EEPROM_SIZE   256

uint8_t eepromData[EEPROM_SIZE];

void setup() {
  Wire.begin();
  Serial.begin(9600);
  while (!Serial); // wait for Serial
}

void loop() {
  if (Serial.available()) {
    uint8_t cmd = Serial.read();

    // ----------------
    // READ command (EEPROM_ADDR)
    // ----------------
    if (cmd == 0x00) {
      for (uint16_t addr = 0; addr < EEPROM_SIZE; addr++) {
        Wire.beginTransmission(EEPROM_ADDR);
        Wire.write(addr & 0xFF);
        if (Wire.endTransmission() != 0) {
          eepromData[addr] = 0x00;
          continue;
        }
        Wire.requestFrom(EEPROM_ADDR, (uint8_t)1);
        if (Wire.available()) {
          eepromData[addr] = Wire.read();
        } else {
          eepromData[addr] = 0x00;
        }
        delay(5);
      }
      Serial.write(eepromData, EEPROM_SIZE);
    }

    // ----------------
    // WRITE command (EEPROM_ADDR)
    // ----------------
    else if (cmd == 0x01) {
      uint16_t bytesRead = 0;
      while (bytesRead < EEPROM_SIZE) {
        if (Serial.available()) {
          eepromData[bytesRead++] = Serial.read();
        }
      }
      for (uint16_t addr = 0; addr < EEPROM_SIZE; addr++) {
        Wire.beginTransmission(EEPROM_ADDR);
        Wire.write(addr & 0xFF);
        Wire.write(eepromData[addr]);
        Wire.endTransmission();
        delay(10);
      }
      Serial.write((uint8_t)0x00); // ACK
    }

    // ----------------
    // ERASE command (EEPROM_ADDR)
    // ----------------
    else if (cmd == 0x02) {
      while (!Serial.available());
      uint8_t eraseValue = Serial.read(); // 0x00 or 0xFF

      for (uint16_t addr = 0; addr < EEPROM_SIZE; addr++) {
        eepromData[addr] = eraseValue;
        Wire.beginTransmission(EEPROM_ADDR);
        Wire.write(addr & 0xFF);
        Wire.write(eraseValue);
        Wire.endTransmission();
        delay(10);
      }
      Serial.write((uint8_t)0x00); // ACK
    }

    // ----------------
    // READ2 command (EEPROM_ADDR2)
    // ----------------
    else if (cmd == 0x03) {
      for (uint16_t addr = 0; addr < EEPROM_SIZE; addr++) {
        Wire.beginTransmission(EEPROM_ADDR2);
        Wire.write(addr & 0xFF);
        if (Wire.endTransmission() != 0) {
          eepromData[addr] = 0x00;
          continue;
        }
        Wire.requestFrom(EEPROM_ADDR2, (uint8_t)1);
        if (Wire.available()) {
          eepromData[addr] = Wire.read();
        } else {
          eepromData[addr] = 0x00;
        }
        delay(5);
      }
      Serial.write(eepromData, EEPROM_SIZE);
    }

    // ----------------
    // WRITE2 command (EEPROM_ADDR2)
    // ----------------
    else if (cmd == 0x04) {
      uint16_t bytesRead = 0;
      while (bytesRead < EEPROM_SIZE) {
        if (Serial.available()) {
          eepromData[bytesRead++] = Serial.read();
        }
      }
      for (uint16_t addr = 0; addr < EEPROM_SIZE; addr++) {
        Wire.beginTransmission(EEPROM_ADDR2);
        Wire.write(addr & 0xFF);
        Wire.write(eepromData[addr]);
        Wire.endTransmission();
        delay(10);
      }
      Serial.write((uint8_t)0x00); // ACK
    }

    // ----------------
    // ERASE2 command (EEPROM_ADDR2)
    // ----------------
    else if (cmd == 0x05) {
      while (!Serial.available());
      uint8_t eraseValue = Serial.read(); // 0x00 or 0xFF

      for (uint16_t addr = 0; addr < EEPROM_SIZE; addr++) {
        eepromData[addr] = eraseValue;
        Wire.beginTransmission(EEPROM_ADDR2);
        Wire.write(addr & 0xFF);
        Wire.write(eraseValue);
        Wire.endTransmission();
        delay(10);
      }
      Serial.write((uint8_t)0x00); // ACK
    }
  }
}