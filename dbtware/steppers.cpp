#include "steppers.h"
#include <util/atomic.h>

#ifdef BOARDMINI


Stepper::Stepper(uint8_t enablePin, uint8_t stepPin, uint8_t dirPin,
                 TMC2130Stepper &stp, bool invert)
    : enablePin(enablePin), stepPin(stepPin), dirPin(dirPin),
      speedChange(false), direction(Direction::CW), invertDir(invert),
      stpdrv(stp), tmcConf(TMCDriverConfig{}) {}

uint32_t Stepper::getDrvStatus() { return stpdrv.DRV_STATUS(); }

bool Stepper::stallStatus() { return stpdrv.stallguard(); }

bool Stepper::isEnabled() { return stpdrv.isEnabled(); }

void Stepper::tmc2130_init() {
  stpdrv.begin();
  stpdrv.I_scale_analog(false);
  stpdrv.internal_Rsense(false);
  stpdrv.rms_current(tmcConf.mA, tmcConf.hold_multiplier);
  stpdrv.setSPISpeed(4e6);
  stpdrv.microsteps(tmcConf.microsteps);
  stpdrv.blank_time(tmcConf.blank_time);
  stpdrv.intpol(tmcConf.interpolate); // Interpolate
  stpdrv.dedge(tmcConf.dedge);
  stpdrv.TPOWERDOWN(128); // ~2s until driver lowers to hold current

  if (ESTOP_TYPE == ESTOP_t::BRAKE) {
    stpdrv.stop_enable(true);
  } else {
    stpdrv.stop_enable(false);
  }

  // Could be tuned for stealthchop
  stpdrv.toff(5); // Only enables the driver if used with stealthChop
  stpdrv.hysteresis_start(3);
  stpdrv.hysteresis_end(2);

  if (STEALTHCHOP) {
    stpdrv.en_pwm_mode(true);
    stpdrv.pwm_freq(1); // f_pwm = 2/683 f_clk
    stpdrv.pwm_autoscale(true);
    stpdrv.pwm_grad(5);
    stpdrv.pwm_ampl(255);
    if (HYBRID_THRESHOLD) {
      stpdrv.TPWMTHRS(16000000UL * tmcConf.microsteps /
                      (256 * tmcConf.threshold * tmcConf.spmm));
    }
  }
  stpdrv.GSTAT(); // Clear GSTAT
}

/***************************************************************************************************
 *                                             Pellet                                             */
#elif defined BOARDPELLET
/***************************************************************************************************/

Stepper::Stepper(uint8_t enablePin, uint8_t stepPin, uint8_t dirPin,
                 bool invert)
    : enablePin(enablePin), stepPin(stepPin), dirPin(dirPin),
      speedChange(false), direction(Direction::CW), invertDir(invert) {}

#endif


/***************************************************************************************************
*                                           Both Boards                                           *
***************************************************************************************************/
void Stepper::setup(){
#ifdef BOARDMINI
  tmc2130_init();
#elif defined BOARDPELLET
#endif
  if (!(fastep = fastep_engine.stepperConnectToPin(stepPin))) {
    Serial.println("Stepper failed to connect.");
    Serial.flush();
    abort();
  }
  setupPins();
  fastep->setAutoEnable(true);
  fastep->setDelayToEnable(10);
  fastep->setDelayToDisable(10);
}

void Stepper::setupPins(){
  // Steppers are active low
  pinMode(stepPin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  if (fastep) {
    fastep->setDirectionPin(dirPin, !invertDir);
#ifdef BOARDMINI
    fastep->setEnablePin(enablePin, true);
#elif defined BOARDPELLET
    // Enable is reversed on PELLET
    fastep->setEnablePin(enablePin, false);
#endif
  }
  speedChange = false;
  disable();
}

void Stepper::disable(){
  stop();
  fastep->disableOutputs();
}

void Stepper::enable(){
  fastep->enableOutputs();
  // Serial.println("Enable stepper");
}

int Stepper::move(int32_t distance){
  return fastep->move(distance);
}

int Stepper::moveTo(int32_t distance){
  return fastep->moveTo(distance);
}


int Stepper::runForward() { return fastep->runForward();
}

int Stepper::runBackward() { return fastep->runBackward();

}

int Stepper::run(Direction dir) {
  setDirection(dir);
  return run();
}

int Stepper::run() {
  if (isZeroSpeed && (fastep->isStopping() || !fastep->isRampGeneratorActive())) {
    return 0;
  }
  switch (direction) {
    case Direction::CW:
      return fastep->runForward();
    case Direction::CCW:
      return fastep->runBackward();
    default:
      return -99;
  }
}

void Stepper::stop() {
  fastep->stopMove();
}

void Stepper::resetPosition() {
    fastep->setCurrentPosition(0);
    // fastep->moveTo(0);
}

void Stepper::forceStopAndReset() {
  fastep->forceStopAndNewPosition(0);
}

void Stepper::setDirection(const Stepper::Direction &dir) { direction = dir; }

void Stepper::changeDirection() {
  if (direction == Direction::CW) {
    setDirection(Direction::CCW);
  } else {
    setDirection(Direction::CW);
  }
}

void Stepper::setTargetVelocity(const double &speed) {
  if (speed <= 0.0001 && speed >= -0.0001){
    isZeroSpeed = true;
    stop();
    return;
  }

  bool ret;
  if (speed > 0) {
    setDirection(Direction::CW);
    ret = (fastep->setSpeedInUs(1e6/(speed * STEPS_SCALING)) == 0);
  } else {
    setDirection(Direction::CCW);
    ret = (fastep->setSpeedInUs(1e6 / (-speed * STEPS_SCALING)) == 0);
  }
  if (!ret) {
    Serial.print("Invalid Speed targeted! ");
    Serial.println(speed);
    Serial.println(1e6 / (-speed * STEPS_SCALING));
    Serial.println(fastep->getSpeedInUs());
  }
  fastep->applySpeedAcceleration();
  isZeroSpeed = false;
  Serial.print("updated speed to: ");
  Serial.println(speed);
}

void Stepper::setMaxAcceleration(const double& accel) {
  if( fastep->setAcceleration(accel * STEPS_SCALING)){
    Serial.print("Invalid accel targeted! ");
    Serial.println(accel*STEPS_SCALING);
  }
  fastep->applySpeedAcceleration();
}

void Stepper::printStatus(){
  Serial.print(fastep->isRampGeneratorActive() ? "ACTIVE_RAMP " : "INACTIVE_RAMP ");
  Serial.print(" Is running? ");
  Serial.print(fastep->isMotorRunning());
  Serial.print(fastep->getPeriodInUsAfterCommandsCompleted());
  Serial.print("us");
  if (fastep->isRunningContinuously()) {
    Serial.print(" nonstop");
  } else {
  Serial.print(" Target=");
  Serial.print(fastep->targetPos());
  }
  if (fastep->isRunning()) {
    Serial.print(" RUN ");
  } else {
    Serial.print(" STOP ");
  }
  Serial.print(" ");
  switch (fastep->rampState()) {
    case RAMP_STATE_COAST:
      Serial.print("COAST");
      break;
    case RAMP_STATE_ACCELERATE:
      Serial.print("ACC");
      break;
    case RAMP_STATE_DECELERATE:
      Serial.print("DEC");
      break;
    case RAMP_STATE_DECELERATE_TO_STOP:
      Serial.print("STOP");
      break;
    case RAMP_STATE_REVERSE:
      Serial.print("REVERSE");
      break;
    default:
      Serial.print(fastep->rampState());
  }
#if (TEST_MEASURE_ISR_SINGLE_FILL == 1)
  Serial.print(" max/us=");
  Serial.print(fastep->max_micros);
#endif
#if (TEST_CREATE_QUEUE_CHECKSUM == 1)
  Serial.print(" checksum=");
  Serial.print(fastep->checksum());
#endif
  Serial.print(" ");
}
