#pragma once
#include <avr/pgmspace.h>

#define STRING(s) #s

#define BUF_LENGTH 128
static bool do_echo = false;
extern double temperature;
extern bool heaterOn;
extern double setPoint;
extern double extruderTargetSpeed;
extern bool speedUpdate;
extern bool motorsEnabled;
extern bool statusCheck;
extern unsigned long loops;

extern float autoSpeed0;
extern float autoSpeed1;

void exec(char);
void processCom();
void printPiInfo();
void printASCIIinfo();
void printHelp();
