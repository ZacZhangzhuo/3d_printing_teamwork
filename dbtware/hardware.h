/* Copyright 2021 - Oliver Harley */
#ifndef HARDWARE_H_QNLGMXOB
#define HARDWARE_H_QNLGMXOB
class SwitchableCooler {
    bool enabled;
    public:
    bool enable;
    explicit SwitchableCooler(bool defaultOn = false);

    void forceUpdate();
    void update();
};
#endif /* end of include guard: HARDWARE_H_QNLGMXOB */
