#ifndef PINS_DBT_SHIELD_H
#define PINS_DBT_SHIELD_H

#ifndef dbt_MOTOR_0
#define dbt_MOTOR_0 (false)
#endif

#ifndef dbt_MOTOR_1
#define dbt_MOTOR_1 (false)
#endif

#ifndef dbt_DISPLAY
#define dbt_DISPLAY (true)
#endif

#include "display_pins.h"
#include "optoInputs_pins.h"
#include "stepper_pins.h"
#include "temperatureSensor_pins.h"


// 500mW outputs
#define OUT0 PWM7
#define OUT1 PWM8
#define OUT2 PWM9

// 100W outputs
#define OUT3 PWM6
#define OUT4 PWM7
#define HEATER_0 OUT3
#define HEATER_1 OUT4

#ifndef dbt_AUX_IS_INPUT
#define dbt_AUX_IS_INPUT (false)
#endif

#ifndef dbt_AUX_IS_MOTOR
#define dbt_AUX_IS_MOTOR (false)
#endif

static_assert((dbt_AUX_IS_MOTOR && dbt_AUX_IS_INPUT), "Only specify dbt_MOTOR_AUX _or_ dbt_INPUT_AUX not both");

// #ifdef dbt_AUX_IS_INPUT
// #ifdef dbt_AUX_IS_MOTOR
// #error Only specify dbt_MOTOR_AUX _or_ dbt_INPUT_AUX not both
// #endif
// #endif

#endif

