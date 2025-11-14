#pragma once

struct LisaberConfiguration {
    int Minutes;            // Startup delay in minutes
    // NOTE: LaserOnTime must be less than ShutterOpenTime.  LaserOnTime
    // is centered in the shutter open time.
    int ShutterOpenTime;    // How long to leave the camera shutter open in ms
    int LaserOnTime;        // How long to leave the laser on in ms

    int ImageCount;         // Number of images to take in a frame
    int ImageRate;          // How long between imagesw in ms
    int FrameCount;         // Total number of frames to take
    int FrameRate;          // How long between frames in ms
    int DebugMultiplier;    // Multiplier for debug mode
};

struct LisaberStatus {
    int CycleCount;
    int IsRunning;
    int DebugCounter;
};

// Command codes sent through the FIFO.
constexpr uint32_t PIV_START = 1;   // Start PIV operation as configured.
constexpr uint32_t PIV_STOP = 2;    // Stop all PIV operation.

// Perform initialisation
int pico_led_init(void);

// Turn the led on or off
void pico_set_led(bool led_on);


#if !defined PIVCOMMON_CPP

extern LisaberConfiguration lisaberConfig;
extern LisaberConfiguration defaultConfig;
extern LisaberStatus lisaberStatus;

#endif

