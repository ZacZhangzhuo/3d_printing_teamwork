#include <Arduino.h>
#include <util/atomic.h>
#include "./controller.h"
#include "./pins.h"
#include "./steppers.h"
#include "./hardware.h"

namespace Controller {

bool manualControl_ = false;
#ifdef BOARDPELLET
bool coolingAuto_ = true;
#endif

/*! In mm/s */
void setExtruderTargetSpeed(float target) {
  // Serial.print("Setting target speed:");
  // Serial.println(target);
  cli();
  ::extruderTargetSpeed = target;
  sei();
  ::speedUpdate = true;
}

void enableSteppers(){
    ::motorsEnable = true;
    extruderInstance.enable();
    extruderInstance.resetPosition();
}

void disableSteppers(){
    ::motorsEnable = false;
    extruderInstance.disable();
    extruderInstance.resetPosition();
    // Serial.println("Steppers disabled");
}

void enableHeater() { ::heaterOn = true; }

void disableHeater(bool verbose) {
  // digitalWrite(PWM5, LOW);
  digitalWrite(HEATER_PIN, LOW);
  if (::heaterOn || verbose) {
    ::heaterOn = false;
    Serial.println("Disabling heater");
    Serial.flush();
  }
}

void enableExtruder(){
    extruderInstance.resetPosition();
    ::motorsEnable = true;
}

void disableExtruder(bool verbose){
  extruderInstance.disable();
  ::motorsEnable = false;
  ::speedUpdate = false;
  if (verbose) {
    Serial.println("Disabling extruder");
    Serial.flush();
  }
}

void disableAllPWMs() {
  for (auto i = 0; i < POWER_OUTPUT_CHANNELS; ++i) {
    pinMode(i, OUTPUT);
  }
  // Let the pin settle before writing to it
  for (auto i = 0; i < POWER_OUTPUT_CHANNELS; ++i) {
    digitalWrite(i, LOW);
  }
  ::motorsEnable = false;
  Serial.println("Disabled Direct Power outputs");
  Serial.flush();
}

void setupKillPins() {
  disableHeater(true);
  disableAllPWMs();
  disableExtruder(true);
  pinMode(OPTO_I_0, INPUT);
  pinMode(OPTO_I_1, INPUT);
  pinMode(OPTO_I_2, INPUT);
  pinMode(OPTO_I_3, INPUT);
}

inline uint8_t readControlOpto() {
#ifdef BOARDMINI
  // bits (D14 D15 D16 D17)
  return 0xF & ~(((PINJ & 0x03) << 2) | (PINH & 0x03));

#elif defined(BOARDPELLET)
  return ~(PINA & 0xE0);
#endif
}

inline bool readHeaterBit(const uint8_t& optobyte){
  return optobyte & HEATER_DISABLE_BIT;
}


#ifdef BOARDMINI

inline uint8_t readSpeedMode(const uint8_t &optobyte) {
  return optobyte & SPEED_BITS_MASK;
}

#elif defined(BOARDPELLET)

inline uint8_t readSpeedMode(const uint8_t &optobyte) { return ~PINC; }

inline bool readCoolingBit(const uint8_t& optobyte) {
  return optobyte & COOLING_I_BIT;
}
void setCoolingAuto(bool autoOn) { coolingAuto_ = autoOn; }
bool getCoolingAuto() { return coolingAuto_; }

#endif

bool getManualControl() { return manualControl_; }
void setManualControl(bool manualControl) { manualControl_ = manualControl; }

inline bool readStepperBit(const uint8_t& optobyte) {
  return optobyte & MOTORS_DISABLE_BIT;
}

/*! Disables both steppers, if the HEATER_DISABLE pin is high.*/
void pollStepperDisable() {
  const uint8_t inputs = readControlOpto();
  if (readStepperBit(inputs)){
    disableSteppers();
  }
}

/*! Disables the heater, if the HEATER_DISABLE pin is high.*/
void pollHeaterDisable() {
  const uint8_t inputs = readControlOpto();
  if (readHeaterBit(inputs)) {
    disableHeater();
  }
}

/*! Disables the heater, if the HEATER_DISABLE pin is high.*/
void pollControlInputs() {
    uint8_t speedMode;
    const uint8_t inputs = readControlOpto();
    bool stepperdisable = readStepperBit(inputs);
    bool heaterdisable = readHeaterBit(inputs);
    static bool needSpeedSet = true;

#ifdef BOARDPELLET
    if(!coolingAuto_)
    { switchableCooling.enable = readCoolingBit(inputs); }
#endif

    if (heaterdisable) {
      disableHeater();
      }
    if (stepperdisable) {
      disableExtruder();
      }
    switchableCooling.update();
    if (stepperdisable || heaterdisable) { return; }
    float setSpeed = 0;
    static float lastTarget = 0;
    speedMode = readSpeedMode(inputs);
#ifdef BOARDMINI
    if (!Controller::manualControl_) {
      switch (speedMode) {
        case 0:
          return;
        case 1:
          setSpeed = autoSpeed0*speedMultiplier;
          break;
        case 2:
          setSpeed = autoSpeed1*speedMultiplier;
          break;
        case 3:
          setSpeed = -retractionSpeed*speedMultiplier;
          break;
        default:
          break;
      }
    }
#elif defined(BOARDPELLET)
  if (!Controller::manualControl_) {
    setSpeed = speedMode * speedMultiplier;
  }
#endif
    if (lastTarget != setSpeed || needSpeedSet) {
      lastTarget = setSpeed;
      setExtruderTargetSpeed(setSpeed);
      needSpeedSet = false;
    }
    ::motorsEnable = true;
}

/* Non critical control inputs */
void pollDigitalInputs() {
  // Nothing here currently
}


void pollPins() {
  pollControlInputs();
  pollDigitalInputs();
}

void printStatus() {
  /* Serial.print("Inputs"); */
  /* Serial.println(Controller::readControlOpto(), BIN); */
  Serial.print(F(" ExtruderTargetSpeed set to: ")); Serial.print(extruderTargetSpeed); Serial.println("mm/s");
  Serial.print(F(" Retract speed: "));
  Serial.print(retractionSpeed);
  Serial.print(F(" Auto Speeds: "));
  Serial.print(autoSpeed0);
  Serial.print(" ");
  Serial.print(autoSpeed1);
  Serial.print(F(". Speed Factor:"));
  Serial.print(speedMultiplier);
  Serial.print(F(" Heaters : "));
  Serial.print(heaterOn);
  Serial.print(F(" TEMP : "));
  Serial.print(temperature);
  Serial.print(F(" Extrudable: "));
  Serial.print(extrudable);
  Serial.print(F(" Enable?: "));
  Serial.print(motorsEnable);
  Serial.print(F(" speeds: "));
  extruderInstance.printStatus();
  Serial.print(F("\nManual Control? "));
  Serial.print(Controller::getManualControl());
#ifdef BOARDPELLET
  Serial.print(F(" Cooling on: "));
  Serial.print(switchableCooling.enable);
#endif
  Serial.println();
}

} // namespace Controller
