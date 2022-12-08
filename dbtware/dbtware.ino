#include <Arduino.h>
#include "config.h"
#include "pins.h"

#include "controller.h"
#include "serialcommand.h"
#include "hardware.h"
#include "steppers.h"
#include "pid.h"
#include <thermistor.h>

FastAccelStepperEngine fastep_engine = FastAccelStepperEngine();

#ifdef BOARDMINI
TMC2130Stepper extruderDriver(EXTRUDER_CS, STEPPER_R_SENSE, 0);
Stepper extruderInstance(EXTRUDER_EN, EXTRUDER_STP, EXTRUDER_DIR, extruderDriver, true);
#elif defined(BOARDPELLET)
Stepper extruderInstance(EXTRUDER_EN, EXTRUDER_STP, EXTRUDER_DIR, true);
#endif
SwitchableCooler switchableCooling(false);

thermistor therm1(THERMISTOR, THERMISTOR_ON);

bool motorsEnable = true;
bool statusCheck = false;
bool heaterOn = false;
bool error = false;
double retractionSpeed = STARTING_RETRACTSPEED; //Give absolute (non-negative)
bool extrudable = false;
double extruderTargetSpeed = 0;
double temperature, setPoint, outputVal;
bool speedUpdate;
float speedMultiplier = 1.0;

#if (MAX_RETRACT_SPEED < STARTING_RETRACTSPEED)
#error "Max retraction speed is lower than starting retraction speed."
#endif

#if (MAX_AUTO_SPEED < AUTO_SPEED_0) || (MAX_AUTO_SPEED < AUTO_SPEED_1)
#error "Max Auto_Speed than their defaults."
#endif

float autoSpeed0 = AUTO_SPEED_0;
float autoSpeed1 = AUTO_SPEED_1;


using namespace Controller;


void setup() {
  Serial.begin(115200);
  printASCIIinfo();
  printHelp();
  delay(10);
#ifdef BOARDMINI
  SPI.begin();
  delay(10);
#endif
  while(!Serial){;};
  Serial.println("Starting...");
  delayMicroseconds(10);
  Serial.flush();

  fastep_engine.init();
  extruderInstance.setup(); // after SPI

  setupKillPins();
  setupPinModes();

  initPID();
  extruderInstance.setTargetVelocity(0);
  extruderInstance.setMaxAcceleration(MAX_ACCEL);
  Controller::enableExtruder();
  Serial.println("Finished setup...");
  delayMicroseconds(10);
  Serial.flush();
}

void errorCondition(){
  heaterOn = false;
  /* Blocking kill code */
  extruderInstance.setTargetVelocity(0);
  extruderInstance.disable();
  stopPID();
  Serial.println("Error condition, Disabling");
  Serial.flush();
}

void pollThermistor(){
  temperature = therm1.analog2temp();
}

void poll(){
  static bool motorsLastStatus = false;
  static auto lastDisableTime = millis();
  pollThermistor();
  //printStatus();
  if(temperature == 0 || temperature > THERMAL_RUNOFF) error = true;
  if (error) {
    stopPID();
    return;
  }

  pollPins();
  extrudable = !(temperature < TEMP_MIN_THRESHOLD);
  runPID();

  if(motorsEnable != motorsLastStatus){
    if(motorsEnable){
      if (extrudable && ((millis() - lastDisableTime) > MOTOR_MIN_STOP_TIME)){
        motorsLastStatus = motorsEnable;
        Controller::enableSteppers();
        //TODO merge? Controller::enableExtruder();
      }
    } else {
      Controller::disableSteppers();
      motorsLastStatus = motorsEnable;
      lastDisableTime = millis();
    }
  }

  if (speedUpdate) {
    // extruderInstance.printStatus();
    extruderInstance.setTargetVelocity(extruderTargetSpeed);
    speedUpdate=false;
  }

  if (motorsEnable && extrudable) {
    auto state = extruderInstance.run();
  }


  if (statusCheck)
  {
    Controller::printStatus();
    statusCheck=false;
  }
  /* Serial.print("Target speed is currently: "); */
  /* Serial.println(extruderTargetSpeed); */

#ifdef PYTOUCH
  printPiInfo();
#endif

  // if error, ignore reading serial
  if (!error) { processCom(); }
}

#ifdef DBTDEBUG
  unsigned long loops=0
#endif

void loop() {
  poll();
  Serial.flush();
#ifdef DBTDEBUG
  loops++;
#endif
}
