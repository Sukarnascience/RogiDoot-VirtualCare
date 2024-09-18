#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Set the I2C address (typically 0x27 or 0x3F)
#define I2C_ADDR 0x27

// Create an LCD object with the I2C address, 20 columns, and 4 rows
LiquidCrystal_I2C lcd(I2C_ADDR, 20, 4);

void setup() {
  // Initialize the LCD
  lcd.init();
  // Turn on the backlight
  lcd.backlight();

  // Print messages to the LCD
  lcd.setCursor(0, 0); // Set cursor to first row, first column
  lcd.print("Hello, World!");
  
  lcd.setCursor(0, 1); // Set cursor to second row
  lcd.print("LCD I2C Example");

  lcd.setCursor(0, 2); // Set cursor to third row
  lcd.print("Arduino & I2C");

  lcd.setCursor(0, 3); // Set cursor to fourth row
  lcd.print("20x4 Display");
}

void loop() {
  // You can add code here to update the display dynamically if needed
}
