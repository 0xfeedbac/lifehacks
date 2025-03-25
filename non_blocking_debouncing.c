#include <Arduino.h>

// state machine
enum DebounceState { IDLE, SAMPLING };
DebounceState dbState = IDLE;

volatile bool interruptFlag = false;
bool buttonPos = HIGH; // with pull-up resistors: HIGH = not pressed, LOW = pressed
unsigned int timesPressed = 0; // track bow many times the button was pressed
unsigned int rawBounces = 0; // track how many interrupts there were in total

// counters for the SAMPLING state, high/low button readings
unsigned int h = 0, l = 0;

// timing vars for non-blocking code
unsigned long uLast = 0; // last sample timing (in us)
const unsigned long SAMPLE_INTERVAL_US = 10;  // e.g., 10 µs between samples

// ISR, keep it simple
void handleChange() {
  interruptFlag = true;
  rawBounces++; // for stats
}

// finish SAMPLING state, print results
void finalizeDebounce(bool newPos) {
  dbState = IDLE;

  if (newPos != buttonPos) {
    if (newPos) {
      timesPressed++;
      Serial.print("Pressed. Count = "); 
      Serial.print(timesPressed);
      Serial.print("\tfrom raw interrupts = ");
      Serial.println(rawBounces);
    } else {
      Serial.println("Released.");
    }
    buttonPos = newPos;
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), handleChange, CHANGE);

  Serial.println("\nStart counting button presses (non-blocking)...");
}

void loop() {
  // 1) If IDLE and an interrupt just arrived, start SAMPLING
  if (dbState == IDLE && interruptFlag) {
    // Clear interrupt flag
    interruptFlag = false;

    uLast = micros(); // make time reference
    h = 0; l = 0; // Reset counters
    dbState = SAMPLING;
  }

  // 2) If SAMPLING, collect pin readings incrementally
  if (dbState == SAMPLING) {
    if ((micros() - uLast) >= SAMPLE_INTERVAL_US) {
      uLast += SAMPLE_INTERVAL_US;
      digitalRead(2) == HIGH ? h++ : l++; 

      if (l >= h + 1000) {
        finalizeDebounce( true);
      } else 
      if (h >= l + 1000) {
        finalizeDebounce(false);
      }
    }
  }

  // the rest of the loop: custom program code, etc.
}
