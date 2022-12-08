#ifndef PINS_PELLET_H_HHMLG39D
#define PINS_PELLET_H_HHMLG39D
#ifndef BOARDPELLET
#define BOARDPELLET
#endif


#define SSR_1_PIN                             A3
#define SSR_2_PIN                             A2
#define SSR_3_PIN                             A1
#define SSR_4_PIN                             A0

#define THERMISTOR                            A4
#define THERMISTOR_ON                         A5

#define HEADER_A_0                            A6
#define HEADER_A_1                            A7
#define HEADER_A_2                            A8
#define HEADER_A_3                            A9

#define MOSFET_0_PIN                          10
#define MOSFET_1_PIN                          11
#define MOSFET_2_PIN                          12
#define MOSFET_3_PIN                          13

#define POWER_OUTPUT_CHANNELS 14 /* A0 - D13 */

#define SWITCHABLE_COOLING                    MOSFET_2_PIN
#define ALWAYS_ON_FAN                         MOSFET_3_PIN

#define HEATER_PIN SSR_4_PIN

#define OPTO_I_0                                 25
#define OPTO_I_1                                 26
#define OPTO_I_2                                 27
#define OPTO_I_3                                 28
#define OPTO_I_4                                 29
#define OPTO_I_5                                 30
#define OPTO_I_6                                 31
#define OPTO_I_7                                 32
#define OPTO_I_8                                 33
#define OPTO_I_9                                 34
#define OPTO_I_10                                35
#define OPTO_I_11                                36
#define OPTO_I_12                                37
#define OPTO_I_13                                38
#define OPTO_I_14                                39
#define OPTO_I_15                                40

#define COOLING_I_PIN    OPTO_I_2
#define MOTOR_I_PIN  OPTO_I_3
#define HEATER_I_PIN OPTO_I_4

// Opto Inputs bitmask
// Pin 27 - PA5
#define COOLING_I_BIT      0x20
//  PA6, PA7 (28, 29)
#define MOTORS_DISABLE_BIT 0x40
#define HEATER_DISABLE_BIT 0x80


#define OPTO_O_0                                44
#define OPTO_O_1                                45
#define OPTO_O_2                                42
#define OPTO_O_3                                43
#define OPTO_O_4                                49
#define OPTO_O_5                                48
#define OPTO_O_6                                46
#define OPTO_O_7                                47

#define HEADER_D_0                            0
#define HEADER_D_1                            1
#define HEADER_D_2                            2
#define HEADER_D_3                            3
#define HEADER_D_4                            4
#define HEADER_D_5                            5

#define MOT_STP                               7
#define MOT_DIR                               24
#define MOT_EN                                23


#define EXTRUDER_EN      MOT_EN
#define EXTRUDER_STP     MOT_STP
#define EXTRUDER_DIR     MOT_DIR
#define FAS_TIMER_MODULE 4

void __attribute__((weak)) setupPinModes() {
    // Handled by TMC2130Stepper::begin()

    pinMode(MOSFET_0_PIN, OUTPUT);
    pinMode(MOSFET_1_PIN, OUTPUT);
    pinMode(MOSFET_2_PIN, OUTPUT);
    pinMode(MOSFET_3_PIN, OUTPUT);

    pinMode(HEADER_A_0, OUTPUT);
    pinMode(HEADER_A_1, OUTPUT);
    pinMode(HEADER_A_2, OUTPUT);
    pinMode(HEADER_A_3, OUTPUT);

    pinMode(HEADER_D_0, OUTPUT);
    pinMode(HEADER_D_1, OUTPUT);
    pinMode(HEADER_D_2, OUTPUT);
    pinMode(HEADER_D_3, OUTPUT);
    pinMode(HEADER_D_4, OUTPUT);
    pinMode(HEADER_D_5, OUTPUT);

    pinMode(THERMISTOR_ON, OUTPUT);
    pinMode(THERMISTOR, INPUT);

    // 0-7 speed input 
    // TODO: 8-13 control inputs
    pinMode(OPTO_I_0, INPUT);
    pinMode(OPTO_I_1, INPUT);
    pinMode(OPTO_I_2, INPUT);
    pinMode(OPTO_I_3, INPUT);
    pinMode(OPTO_I_4, INPUT);
    pinMode(OPTO_I_5, INPUT);
    pinMode(OPTO_I_6, INPUT);
    pinMode(OPTO_I_7, INPUT);
    pinMode(OPTO_I_8, INPUT);
    pinMode(OPTO_I_9, INPUT);
    pinMode(OPTO_I_10, INPUT);
    pinMode(OPTO_I_11, INPUT);
    pinMode(OPTO_I_12, INPUT);
    pinMode(OPTO_I_13, INPUT);
    pinMode(OPTO_I_14, INPUT);
    pinMode(OPTO_I_15, INPUT);

    // OPTO0 noERR , OPTO1 tool ready
    pinMode(OPTO_O_0, OUTPUT);
    pinMode(OPTO_O_1, OUTPUT);
    pinMode(OPTO_O_2, OUTPUT);
    pinMode(OPTO_O_3, OUTPUT);
    pinMode(OPTO_O_4, OUTPUT);
    pinMode(OPTO_O_5, OUTPUT);
    pinMode(OPTO_O_6, OUTPUT);
    pinMode(OPTO_O_7, OUTPUT);

    pinMode(SSR_1_PIN, OUTPUT);
    pinMode(SSR_2_PIN, OUTPUT);
    pinMode(SSR_3_PIN, OUTPUT);
    pinMode(SSR_4_PIN, OUTPUT);
    pinMode(MOT_EN, OUTPUT);
    pinMode(MOT_STP, OUTPUT);
    pinMode(MOT_DIR, OUTPUT);

    digitalWrite(THERMISTOR_ON, HIGH);
    digitalWrite(ALWAYS_ON_FAN, HIGH);
    digitalWrite(SSR_1_PIN, LOW);
    digitalWrite(SSR_2_PIN, LOW);
    digitalWrite(SSR_3_PIN, LOW);
    digitalWrite(SSR_4_PIN, LOW);
}

#endif /* end of include guard: PINS_PELLET_H_HHMLG39D */
