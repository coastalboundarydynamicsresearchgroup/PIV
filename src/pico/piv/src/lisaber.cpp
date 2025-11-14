#include <iostream>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/gpio.h"
#include "pivcommon.h"
//#include "hardware/irq.h"
//#include "hardware/sync.h"

#include "pivcommon.h"

constexpr int CAMERA_SHUTTER_LED_PIN = 4;   // GPIO pin for the camera shutter
constexpr int CAMERA_SHUTTER_PIN = 5;       // GPIO pin for the camera shutter
constexpr int LASER_LED_PIN = 0;            // GPIO pin for the laser
constexpr int LASER_PIN = 1;                // GPIO pin for the laser

bool checkAbort() {
    if (lisaberStatus.IsRunning == 0) {
        return true;
    }

    if (multicore_fifo_rvalid()) {
        uint32_t abort = multicore_fifo_pop_blocking();
        if (abort == PIV_STOP) {
            lisaberStatus.IsRunning = 0;
            return true;
        }
    }

    return false;
}

void InitializeGpio() {
    // Initialize GPIO pins for the laser and shutter
    gpio_init(CAMERA_SHUTTER_LED_PIN);
    gpio_set_dir(CAMERA_SHUTTER_LED_PIN, GPIO_OUT);
    gpio_init(CAMERA_SHUTTER_PIN);
    gpio_set_dir(CAMERA_SHUTTER_PIN, GPIO_OUT);
    gpio_put(CAMERA_SHUTTER_LED_PIN, 0); // Turn off the LED initially
    gpio_put(CAMERA_SHUTTER_PIN, 0);     // Turn off the LED initially

    gpio_init(LASER_LED_PIN);
    gpio_set_dir(LASER_LED_PIN, GPIO_OUT);
    gpio_init(LASER_PIN);
    gpio_set_dir(LASER_PIN, GPIO_OUT);
    gpio_put(LASER_LED_PIN, 0);         // Turn off the LED initially
    gpio_put(LASER_PIN, 1);             // Turn off the laser initially

    // Initialize other GPIO pins as needed
}

constexpr int LASER_PULSE_DURATION = 150;   // How long to pulse laser start/stop in us.

// Define the Runtimes class to manage the timing of the laser and shutter
class Runtimes {
public:
    // NOTE: These are delays in ms from each other, not from any datum point.
    int ShutterOpenDelay; // ms
    int LaserOnDelay;        // ms
    int LaserOffDelay;       // ms 
    int ShutterCloseDelay;        // ms
    int DwellDelay;              // ms

    Runtimes()
        : ShutterOpenDelay(0),
          LaserOnDelay(0),
          LaserOffDelay(0),
          ShutterCloseDelay(0),
          DwellDelay(0)
    {
        int centerTime = lisaberConfig.ShutterOpenTime / 2;
        this->ShutterOpenDelay = 0;
        this->LaserOnDelay = centerTime - lisaberConfig.LaserOnTime / 2;
        this->LaserOffDelay = lisaberConfig.LaserOnTime;
        this->ShutterCloseDelay = centerTime - lisaberConfig.LaserOnTime / 2;
        this->DwellDelay = lisaberConfig.ImageRate - lisaberConfig.ShutterOpenTime;
    }  
};


void TakeAPicture(const Runtimes& runtimes, int frame) {
    sleep_us(runtimes.ShutterOpenDelay * 1000 * lisaberConfig.DebugMultiplier);

    // Open the shutter
    gpio_put(CAMERA_SHUTTER_PIN, 1);
    //gpio_put(CAMERA_SHUTTER_LED_PIN, 1);
    sleep_us(runtimes.LaserOnDelay * 1000 * lisaberConfig.DebugMultiplier);

    // Turn on the laser
    gpio_put(LASER_PIN, 0);
    if (frame % 2 == 0) {
        gpio_put(LASER_LED_PIN, 1);
    } else {
        gpio_put(CAMERA_SHUTTER_LED_PIN, 1);
    }
    sleep_us(runtimes.LaserOffDelay * 1000 * lisaberConfig.DebugMultiplier);

    // Turn off the laser
    gpio_put(LASER_PIN, 1);
    if (frame % 2 == 0) {
        gpio_put(LASER_LED_PIN, 0);
    } else {
        gpio_put(CAMERA_SHUTTER_LED_PIN, 0);
    }
    sleep_us(runtimes.ShutterCloseDelay * 1000 * lisaberConfig.DebugMultiplier);

    // Close the shutter
    gpio_put(CAMERA_SHUTTER_PIN, 0);
    gpio_put(CAMERA_SHUTTER_LED_PIN, 0);
}

absolute_time_t nextGroupTime{make_timeout_time_ms(0)};

void RunPiv() {
    auto frameCount = lisaberConfig.FrameCount;

    Runtimes runtimes;
    nextGroupTime = delayed_by_us(get_absolute_time(), lisaberConfig.FrameRate * 1000 * lisaberConfig.DebugMultiplier);

    for (int frame = 0; frame < frameCount; ++frame) {
        if (checkAbort()) {
            break;
        }

        for (auto image = 0; image < lisaberConfig.ImageCount; ++image) {
            if (checkAbort()) {
                break;
            }

            TakeAPicture(runtimes, image);

            // Delay between images in a frame, except for the last image.
            if (image != lisaberConfig.ImageCount - 1) {
                sleep_us(runtimes.DwellDelay * 1000 * lisaberConfig.DebugMultiplier);
            }
        }

        if (checkAbort()) {
            break;
        }

        lisaberStatus.CycleCount++;

        // TODO - This is wrong, capture time at start, compute elapsed time, sleep for the remainder.
        // sleep_ms(lisaberConfig.FrameRate * lisaberConfig.DebugMultiplier);
        sleep_until(nextGroupTime);

        nextGroupTime = delayed_by_us(nextGroupTime, lisaberConfig.FrameRate * 1000 * lisaberConfig.DebugMultiplier);
    }
}

void DoLisaberCommand(uint32_t command) {
    switch (command) {
        case PIV_START: // Start
            lisaberStatus.CycleCount = 0;
            lisaberStatus.IsRunning = 1;
            RunPiv();
            lisaberStatus.IsRunning = 0;
            break;
        case PIV_STOP: // Stop
            lisaberStatus.IsRunning = 0;
            break;
        default:
            break;
    }
}

void do_lisaber() {
    InitializeGpio();
    multicore_fifo_push_blocking(0); // Notify core 0 that core 1 is ready


    while (true) {
        uint32_t command = multicore_fifo_pop_blocking();
        DoLisaberCommand(command);
        lisaberStatus.DebugCounter++;
    }
}

