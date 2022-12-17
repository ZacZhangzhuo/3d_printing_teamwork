#ifndef STEPPER_H
#define STEPPER_H

#include <Arduino.h>
#include "config.h"

#ifdef BOARDMINI
#include "TMCStepper.h"
#include <SPI.h>
#endif /* BOARDMINI */
//#include <FastAccelStepper.h>
#include "pins.h"

#ifdef BOARDMINI

// Settings
enum class ESTOP_t { BRAKE, FREEWHEEL };

// Settings
constexpr ESTOP_t ESTOP_TYPE = ESTOP_t::FREEWHEEL;
#define STEALTHCHOP true
// #define HYBRID_THRESHOLD true

/* https://e3d-online.dozuki.com/Guide/Extruder+steps+per+mm/96 */
#define MICROSTEPPING 16
#define MOTORSTEPS 200
#define GEAR_RATIO 3
#define HOB_DIAMETER 7.3
#define STEPS_PER_MM (MOTORSTEPS*MICROSTEPPING*GEAR_RATIO / (HOB_DIAMETER * PI))
constexpr double STEPS_SCALING = STEPS_PER_MM;

#elif defined BOARDPELLET

#define SCALE_MULTIPLIER 4.11 /* Normal Nozzle: 2020-12-09 */

#define MICROSTEPPING 1
#define MOTORSTEPS 800

// Measured values
#define SERVO_STEP_SPEED 10000 /* = 750 RPM * 800 Steps/rev  @ ROBOT_SPEED*/
#define ROBOT_SPEED 40 /* mm/s */
// #define CROSSECTION (4+4*PI) /*mm^2 */
// #define CROSSECTION (6) /*mm^2 */


// calculated
#define FLOW_VOL (CROSSECTION * ROBOT_SPEED) /* mm^3 */
#define FLOWRATE (FLOW_VOL)/(SERVO_PM)

constexpr double STEPS_SCALING = (SERVO_STEP_SPEED / ((double)ROBOT_SPEED * SCALE_MULTIPLIER));
#endif /* ifndef BOARD */


#ifdef BOARDMINI
// TMC Stepper Config
struct TMCDriverConfig {
  const uint16_t microsteps      = MICROSTEPPING;
  const uint8_t blank_time       = 24;   // [16, 24, 36, 54]
  const uint8_t off_time         = 3;    // [1..15]
  const uint8_t hysteresis_start = 1;    // [1..8]
  const int8_t hysteresis_end    = 12;   // [-3..12]
  const float hold_multiplier    = 0.5f; // [0..1]
  const float threshold          = 0.1f; // TODO
  const bool interpolate         = true;
  const bool dedge               = true;
  const uint16_t mA              = 900;
  const float spmm               = STEPS_SCALING;
};

#ifndef STEALTHCHOP
#define STEALTHCHOP false
#endif /* ifndef STEALTHCHOP */
#ifndef HYBRID_THRESHOLD
#define HYBRID_THRESHOLD false
#endif /* ifndef HYBRID_THRESHOLD */

/******************************************************************************/



#ifndef STEPPER_R_SENSE
#define STEPPER_R_SENSE (0.11f)
#endif
#define STEPPER_0_R_SENSE STEPPER_R_SENSE
#define STEPPER_1_R_SENSE STEPPER_R_SENSE
#endif /* ifdef BOARDMINI */

class Stepper;
extern FastAccelStepperEngine fastep_engine;

class Stepper {

    enum class Direction { CW, CCW };

    FastAccelStepper* fastep = nullptr;
    uint8_t enablePin;
    uint8_t stepPin;
    uint8_t dirPin;

    volatile bool speedChange = false;
    bool isZeroSpeed = true;

    Direction direction = Direction::CW;
    bool invertDir = false;


#ifdef BOARDMINI
    TMC2130Stepper &stpdrv;
    TMCDriverConfig tmcConf;
    uint16_t lastStatusUpdate = 0;
    uint32_t drvStatus = 0;
    // Internal functions
    void tmc2130_init();


#endif /* ifdef BOARDMINI */

  public:

#ifdef BOARDMINI
    // Following Quick configuration guide Page 81/103
    // https://www.trinamic.com/fileadmin/assets/Products/ICs_Documents/TMC2130_datasheet.pdf
    Stepper(uint8_t enablePin, uint8_t stepPin, uint8_t dirPin, TMC2130Stepper &stp, bool invert=false);
    uint32_t getDrvStatus();
    bool stallStatus();
#elif defined BOARDPELLET
    Stepper(uint8_t enablePin, uint8_t stepPin, uint8_t dirPin, bool invert=false);
#endif /* BOARD{MINI,PELLET} */

    ~Stepper() = default;
    void setup();
    void setDirection(const Direction& dir);
    void changeDirection();
    int run();
    int run(Direction dir);
    int runForward();
    int runBackward();
    void setTargetVelocity(const double& speed);
    void setMaxAcceleration(const double& accel);
    void disable();
    void enable();
    void setupPins();
    int move(int32_t distance);
    int moveTo(int32_t distance);
    bool isEnabled();
    void stop();
    void forceStopAndReset();
    void resetPosition();
    void printStatus();
};


#endif /* STEPPER_H */
