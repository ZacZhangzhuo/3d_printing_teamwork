#include "serialcommand.h"
#include "controller.h"
#include "pins.h"
#include <Arduino.h>
#include "./hardware.h"

inline void printHelp() {
#ifdef BOARDMINI
        Serial.println(F(
            "\n===================================\n"
            "============ Commands =============\n"
            "==Low level Arduino Pin control==\n"
            "mode <pin> <mode>: pinMode()\n"
            "read <pin>: digitalRead()\n"
            "aread <pin>: analogRead()\n"
            "write <pin> <value>: digitalWrite()\n"
            "awrite <pin> <value>: analogWrite()\n"
            "out <outputchannel> <off/on>: 0-" STRING(N_OUTCHANNELS_-1) "    /   0/1\n"
            "\n"
            "==Temperature Control==\n"
            "heater <number> <value>: 0/1 off/on   /   0-250C\n"
            "settemp <value>: set target temperature 0-250C\n"
            "\n"
            "==Speed Control==\n"
            "evel <number> <value>: extruder velocity, 0/1 off/on    /   -300-300\n"
            "rspeed <value>: retraction speed /   0-300\n"
            "aspeed <number> <value>: set automatic speeds_X: X=0/1  / 0-" STRING(MAX_AUTO_SPEED) "\n"
            "speedFactor: <value>     / 0.0-1.0\n"
            "\n"
            "==Other Controls==\n"
            "manual: <value>     / 0/1 false/true\n"
            "cool: <value>       / 0/1 - cooling fan off/on\n"
            "echo: <value>       / 0/1 - set echo to false/true\n"
            //"extrude <number> <value>: 0/1 on/off  /  -3000-3000\n"
            // "load: load filament\n"
            // "unload: unload filament\n"
            "\n"
            "==Status and more==\n"
            "temp: extruder temperature\n"
            "stat: print the current status\n"
            "help: print this message\n"
            "info: print firmware info\n"
            "===================================\n"
            ));
#elif defined(BOARDPELLET)
        Serial.println(F(
              "==Low level Arduino Pin control==\n"
              "mode <pin> <mode>: pinMode()\n"
              "read <pin>: digitalRead()\n"
              "aread <pin>: analogRead()\n"
              "write <pin> <value>: digitalWrite()\n"
              "awrite <pin> <value>: analogWrite()\n"
              // "out <outputchannel> <on/off>: 0-" STRING(N_OUTCHANNELS_-1) "    /   0/1\n"
              "\n==Temperature Control==\n"
              "heater <number> <value>: 0/1 on/off   /   0-250C\n"
              "settemp <value>: set target temperature 0-250C\n\n"
              // "efan <value>: 0/1 on/off       / extruder fan \n"
              // "extrude <number> <value>: 0/1 on/off  /  -3000-3000\n"
              "evel <number> <value>: extruder velocity, 0/1 on/off    /   -300-300\n"
              "rspeed <value>: retraction speed /   0-300\n"
              "load: load filament\n"
              "unload: unload filament\n"
              "temp: extruder temperature\n"
              "cool: <value>       / x/0/1 - cooling fan auto/on/off\n"
              "manual: <value>     / 0/1 for true/false\n"
              "speedFactor: <value>     / 0.0-1.0\n"
              "help: print this message\n"
              "stat: print the current status \n"
              "info: print firmware info.\n"
              ));
#endif
}

void exec(char *cmdline) {
    char *command = strsep(&cmdline, " ");

    if (strcmp_P(command, PSTR("help")) == 0) {
      printHelp();
    }
#ifdef DBTDEBUG
    else if (strcmp_P(command, PSTR("rloop")) == 0) {
      loops = 0;
    }
    else if (strcmp_P(command, PSTR("loop")) == 0) {
      Serial.println(loops);
    }
#endif
    else if (strcmp_P(command, PSTR("mode")) == 0) {
        int pin = atoi(strsep(&cmdline, " "));
        int mode = atoi(cmdline);
        pinMode(pin, mode);
    }
    else if (strcmp_P(command, PSTR("read")) == 0) {
        int pin = atoi(cmdline);
        Serial.println(digitalRead(pin));
    }
    else if (strcmp_P(command, PSTR("aread")) == 0) {
        int pin = atoi(cmdline);
        Serial.println(analogRead(pin));
    }
    else if (strcmp_P(command, PSTR("write")) == 0) {
        int pin = atoi(strsep(&cmdline, " "));
        int value = atoi(cmdline);
        digitalWrite(pin, value);
    }
    else if (strcmp_P(command, PSTR("awrite")) == 0) {
        int pin = atoi(strsep(&cmdline, " "));
        int value = atoi(cmdline);
        analogWrite(pin, value);
    }
    else if (strcmp_P(command, PSTR("echo")) == 0) {
        do_echo = atoi(cmdline);
    }
    else if (strcmp_P(command, PSTR("heater")) == 0) {
        int number = atoi(strsep(&cmdline, " "));
        int value = atoi(cmdline);
        setPoint = value;
        heaterOn=number;
        Serial.print("Updated heater to ");
        Serial.print(heaterOn); 
        Serial.print(" and set temp to ");
        Serial.println(value);
    }
    else if (strcmp_P(command, PSTR("evel")) == 0) {
        int number = atoi(strsep(&cmdline, " "));
        float value = atof(cmdline);
        // TODO guard on the values that won't fit inside a uint16_t
        if (!number) {Controller::disableExtruder(); return;}
        else{
          Controller::setExtruderTargetSpeed(value);
          Controller::enableSteppers(); // This resets the stepper position
        }
    }
#ifdef BOARDMINI
    else if(strcmp_P(command, PSTR("out")) == 0){
      int channel = atoi(strsep(&cmdline, " "));
      int value = atoi(cmdline);
      for (auto i = 0; i < N_OUTCHANNELS_; ++i){
        if(channel == i) digitalWrite(OUTPUT_CHANNELS[channel], value ? HIGH : LOW);
      }
    }
    else if (strcmp_P(command, PSTR("cool")) == 0) {
      switchableCooling.enable = (atoi(cmdline));
    }
    else if (strcmp_P(command, PSTR("aspeed")) == 0){
      int x = atoi(strsep(&cmdline, " "));
      float value = atof(strsep(&cmdline, " "));
      if (value < 0 || value > MAX_AUTO_SPEED) {
        Serial.println(F("Requested speed out of range 0-" STRING(MAX_AUTO_SPEED) "!"));
      } else if (x == 0) {
        autoSpeed0 = value;
      } else if (x == 1){
        autoSpeed1 = value;
      } else {
        Serial.print(F("Error: Pin No. out of range: "));
        Serial.print(x);
        Serial.println();
      }
    }
#elif defined(BOARDPELLET)
    else if (strcmp_P(command, PSTR("cool")) == 0) {
      char* s = strsep(&cmdline, " ");
      if (*s != '1' && *s  != '0') { Controller::setCoolingAuto(true); }
      else {
        Controller::setCoolingAuto(false);
        switchableCooling.enable = (atoi(s));
      }
    }
#endif
    else if (strcmp_P(command, PSTR("manual")) == 0){
      int value = atoi(strsep(&cmdline, " "));
        Controller::setManualControl(bool(value));
    }
    else if (strcmp_P(command, PSTR("speedFactor")) == 0){
      float value = atof(strsep(&cmdline, " "));
      speedMultiplier = value;
    }
    else if (strcmp_P(command, PSTR("rspeed")) == 0){
      float value = atof(strsep(&cmdline, " "));
      if (value < 0 || value > MAX_RETRACT_SPEED) {
        Serial.println(F("Requested retraction speed out of range: 0-" STRING(MAX_AUTO_SPEED) "!"));
      } else {
        cli();
        retractionSpeed =value;
        sei();
      }
    } else if(strcmp_P(command, PSTR("load")) == 0){
        //TODO load filament
      Serial.print(F("Error: Unimplemented."));
    } else if(strcmp_P(command, PSTR("unload")) == 0){
      Serial.print(F("Error: Unimplemented."));
        //TODO unload filamnent
    } else if (strcmp_P(command, PSTR("temp")) == 0){
        Serial.println(temperature);
    } else if (strcmp_P(command, PSTR("settemp")) == 0){
        int value = atoi(cmdline);
        setPoint = value;
    } else if (strcmp_P(command, PSTR("stat")) == 0){
        ::statusCheck=true;
    } else if (strcmp_P(command, PSTR("info")) == 0){
        printASCIIinfo();
    } else {
        Serial.print(F("Error: Unknown command: "));
        Serial.print(command);
        Serial.println();
    }
}

void processCom() {
    /* Process incoming commands. */
  while (Serial.available()) {
    static char buffer[BUF_LENGTH];
    static int length = 0;

    int data = Serial.read();
    if (data == '\b' || data == '\177') {  // BS and DEL
      if (length) {
        length--;
        if (do_echo) Serial.write("\b \b");
      }
    }
    if (data == '\n') {
      if (do_echo) Serial.write("\n");    // output CRLF
      buffer[length] = '\0';
      if (length) exec(buffer);
      length = 0;
    }
    else if (length < BUF_LENGTH - 1) {
      buffer[length++] = data;
      if (do_echo) Serial.write(data);
    }
  }
}

void printPiInfo(){
    Serial.print("\nT");
    Serial.print(temperature);
    Serial.print(" S");
    Serial.print(extruderTargetSpeed);
    Serial.print(" C");
    //todo add speed input
#ifdef BOARDPELLET
    if ( Controller::getCoolingAuto() )
      { Serial.print("A"); }
    Serial.print(switchableCooling.enable);
#endif
    Serial.println();
}


void printASCIIinfo() {
  Serial.println("            hNNN-sNNN+            sMMMy           ");
  Serial.println("            dMMM:yMMM+            sMMMy           ");
  Serial.println("            dMMM:yMMM+            sMMMy           ");
  Serial.println("   `-/osso+-dMMM:yMMMs:+ssssssssssmMMMmsss        ");
  Serial.println(" `odMMMMMMMMMMMM:yMMMMMMMMMMMMMMNNMMMMMNNN`       ");
  Serial.println(".mMMMds++sdMMMMM:yMMMMNy+/+yNMMMd-yMMMh...        ");
  Serial.println("dMMMo`    `yMMMM:yMMMN-     -NMMM+sMMMy           ");
  Serial.println("mMMM:      +MMMM-sMMMm`     `mMMMssMMMh      `hhhy");
  Serial.println("/MMMNo-..:sNMMMh .NMMMd+-.-+dMMMN..NMMMh/-.-+mMMMo");
  Serial.println(" /mMMMMNNMMMMNs`  .hMMMMNNNMMMMh-  .yMMMMNNNMMMm/ ");
  Serial.println("   :sdNNMNmy/`      -ohmNMMmho-      .+ydmmdho-   ");
  Serial.println("                                                  ");
  Serial.println("                                                  ");
  Serial.println("dbt-mini-shield firmware 1.2.23 by Oliver Harley, Andrea Perissinotto");
  Serial.println();
  Serial.print("Firmware for: ");
#ifdef BOARDMINI
  Serial.println("Mini Extruder (UR5).");
#elif defined(BOARDPELLET)
  Serial.println("Pellet Extruder (IRB1600).");
#endif
}
