#include "pid.h"
#include "pins.h"

AutoPID myPID(&temperature, &setPoint, &outputVal, OUTPUT_MIN, OUTPUT_MAX, KP, KI, KD);

void runPID(){
    extrudable = myPID.atSetPoint(SETPOINT_THRESHOLD);
    if(heaterOn){
        myPID.run(); //call every loop, updates automatically at certain time interval
        digitalWrite(HEATER_PIN, outputVal);
        // Serial.print("OUTPUTVAL:");
        // Serial.println(outputVal);
    }
}

void initPID(){
    myPID.setBangBang(CONTROL_THRESHOLD);
    //set PID update interval to 4000ms
    myPID.setTimeStep(PID_TIMEINTERVAL);
}

void stopPID(){
    myPID.stop();
    extrudable = false;
}
