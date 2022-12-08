#pragma once
/**************************************************************************************************/

//Set build options
// #define BOARDPELLET
// #define BOARDMINI
// #define PYTOUCH

/**************************************************************************************************/

/**************************************************************************************************/
/* Specify default as MINI */
#if !defined(BOARDMINI) && !defined(BOARDPELLET)
#define BOARDMINI
#endif
#if defined(BOARDMINI) && defined(BOARDPELLET)
#error CAN ONLY DEFINE ONE OF BOARDMINI OR BOARDELLET!
#endif

/**************************************************************************************************/
/* Some parameters - should not need to change */

#define MAX_ACCEL 100

#ifdef BOARDPELLET
#define MOTOR_MIN_STOP_TIME 8
#define TEMP_MIN_THRESHOLD 160
#define STARTING_RETRACTSPEED 30
#define THERMAL_RUNOFF 300
#endif

#ifdef BOARDMINI
#define MOTOR_MIN_STOP_TIME 8
#define TEMP_MIN_THRESHOLD 160
#define STARTING_RETRACTSPEED 30
#define THERMAL_RUNOFF 300

// Positive Integer values only
#define AUTO_SPEED_0 2
#define AUTO_SPEED_1 7

#ifndef MAX_AUTO_SPEED
#define MAX_AUTO_SPEED 20
#endif

#ifndef MAX_RETRACT_SPEED
#define MAX_RETRACT_SPEED 60
#endif

#endif

#if defined(BOARDMINI) && defined(BOARDPELLET)
#error "Must define BOARDMINI xor BOARDPELLET"
#endif
