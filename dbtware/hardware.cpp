/* Copyright 2021 - Oliver Harley */
#include <Arduino.h>
#include <stdint.h>
#include "./hardware.h"
#include "./config.h"
#include "./pins.h"

SwitchableCooler::SwitchableCooler(bool defaultOn) : enabled(false), enable(defaultOn) {}

void SwitchableCooler::forceUpdate() {
    digitalWrite(SWITCHABLE_COOLING, enable);
    enabled = enable;
}

void SwitchableCooler::update() {
    if (enabled != enable){
        digitalWrite(SWITCHABLE_COOLING, enable);
        enabled = enable;
    }
}
