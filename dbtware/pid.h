#pragma once
#include <AutoPID.h>

#define SETPOINT_THRESHOLD 15
#define CONTROL_THRESHOLD 4

//pid settings and gains

#define KP 22.2
#define KI 1.04
#define KD 114
#define PID_TIMEINTERVAL 15
#define OUTPUT_MIN  0
#define OUTPUT_MAX  1

extern double temperature, setPoint, outputVal;
extern bool heaterOn;
extern bool extrudable;



void initPID();
void runPID();
void stopPID();

