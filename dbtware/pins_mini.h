#ifndef PINS_H_RSOALORP
#define PINS_H_RSOALORP
#ifndef BOARDMINI
#define BOARDMINI
#endif

#define N_OUTCHANNELS_ 3

#define THERMISTOR                            A0
#define THERMISTOR_ON                         A1

#define OPTO_I_0 14
#define OPTO_I_1 15
#define OPTO_I_2 16
#define OPTO_I_3 17
#define HEATER_DISABLE_BIT (0b1000)
#define MOTORS_DISABLE_BIT (0b0100)
#define SPEED_BITS_MASK (0b0011)

#define PWM0 0
#define PWM1 1
#define PWM2 2
#define PWM3 3
#define PWM4 4
#define PWM5 5
#define PWM6 6
#define PWM7 7
#define PWM8 8
#define PWM9 9

#define POWER_OUTPUT_CHANNELS 10 /* PWM0 - PWM9 */

#define HEATER_PWM0_PIN 5
#define HEATER_PWM1_PIN 6
#define HEATER_PIN HEATER_PWM1_PIN
#define ALWAYS_ON_FAN PWM9
#define SWITCHABLE_COOLING HEATER_PWM0_PIN

const decltype(PWM7) OUTPUT_CHANNELS[] = { PWM7, PWM8, HEATER_PWM0_PIN };


#define STEPPER_0_CS      (13)
#define STEPPER_0_EN      (12)
#define STEPPER_0_STP     (7)
#define STEPPER_0_DIR     (29)

#define STEPPER_1_CS      (11)
#define STEPPER_1_EN      (10)
#define STEPPER_1_STP     (6)
#define STEPPER_1_DIR     (25)

// We map the extruder to the stepper 0 port
#define EXTRUDER_CS      STEPPER_0_CS
#define EXTRUDER_EN      STEPPER_0_EN
#define EXTRUDER_STP     STEPPER_0_STP
#define EXTRUDER_DIR     STEPPER_0_DIR
#define FAS_TIMER_MODULE 4

void __attribute__((weak)) setupPinModes() {
    // Handled by TMC2130Stepper::begin()
    pinMode(STEPPER_0_CS, OUTPUT);
    pinMode(STEPPER_1_CS, OUTPUT);
    pinMode(STEPPER_0_EN, OUTPUT);
    pinMode(STEPPER_1_EN, OUTPUT);
    pinMode(STEPPER_0_STP, OUTPUT);
    pinMode(STEPPER_1_STP, OUTPUT);
    pinMode(STEPPER_0_DIR, OUTPUT);
    pinMode(STEPPER_1_DIR, OUTPUT);
    pinMode(PWM0, OUTPUT);
    pinMode(PWM1, OUTPUT);
    pinMode(PWM2, OUTPUT);
    pinMode(PWM3, OUTPUT);
    pinMode(PWM4, OUTPUT);
    pinMode(PWM5, OUTPUT);
    pinMode(PWM6, OUTPUT);
    pinMode(PWM7, OUTPUT);
    pinMode(PWM8, OUTPUT);
    pinMode(PWM9, OUTPUT);

    pinMode(THERMISTOR_ON, OUTPUT);
    pinMode(OPTO_I_0, INPUT);
    pinMode(OPTO_I_1, INPUT);
    pinMode(OPTO_I_2, INPUT);
    pinMode(OPTO_I_3, INPUT);
    pinMode(THERMISTOR, INPUT);

    digitalWrite(STEPPER_0_CS, HIGH);
    digitalWrite(STEPPER_1_CS, HIGH);
    digitalWrite(THERMISTOR_ON, HIGH);
    digitalWrite(ALWAYS_ON_FAN, HIGH);
}

#endif /* end of include guard: PINS_H_RSOALORP */
