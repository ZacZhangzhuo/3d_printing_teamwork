#ifndef CONTROLLER_H
#define CONTROLLER_H
#include "config.h"
#include <stdint.h>

extern bool motorsEnable;
extern double temperature;
extern double setPoint, outputVal;
extern bool heaterOn;
extern double retractionSpeed;
extern double extruderTargetSpeed;
extern bool speedUpdate;
extern float speedMultiplier;

extern float autoSpeed0;
extern float autoSpeed1;

class Stepper;
extern Stepper extruderInstance;
extern bool extrudable;

class SwitchableCooler;
extern SwitchableCooler switchableCooling;


namespace Controller {

    void disableAllPWMs();
    void disableExtruder(bool verbose=false);
    void disableHeater(bool verbose=false);
    void disableSteppers();

    void enableExtruder();
    void enableHeater();
    void enableSteppers();

    void pollPins();
    void pollControlInputs();
    void pollHeaterDisable();
    void pollStepperDisable();
    void pollDigitalInputs();

    bool getManualControl();
    void setManualControl(bool);
#ifdef BOARDPELLET
    void setCoolingAuto(bool setAuto=true);
    bool getCoolingAuto();
#endif

    void setExtruderTargetSpeed(float target);
    void setupControlTimers();

    void setupKillPins();
    void printStatus();
    inline uint8_t readControlOpto();

    void timerISR(void);
}

#endif /* CONTROLLER_H */
