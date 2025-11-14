#include <stdio.h>
#include <iostream>
#include <string>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "json.h"

#include "pivcommon.h"

// External reference for core 1 execution.
extern void do_lisaber();



std::string ParseConfiguration(const json::jobject& command, json::jobject& result) {
    lisaberConfig = defaultConfig;
    
    if (command.has_key("Minutes")) {
        lisaberConfig.Minutes = (int)command["Minutes"];
    }
    
    if (command.has_key("ShutterOpenTime")) {
        lisaberConfig.ShutterOpenTime = (int)command["ShutterOpenTime"];
    }
    
    if (command.has_key("LaserOnTime")) {
        lisaberConfig.LaserOnTime = (int)command["LaserOnTime"];
    }
    
    if (command.has_key("ImageCount")) {
        lisaberConfig.ImageCount = (int)command["ImageCount"];
    }
    
    if (command.has_key("ImageRate")) {
        lisaberConfig.ImageRate = (int)command["ImageRate"];
    }

    if (command.has_key("FrameCount")) {
        lisaberConfig.FrameCount = (int)command["FrameCount"];
    }

    if (command.has_key("FrameRate")) {
        lisaberConfig.FrameRate = (int)command["FrameRate"];
    }

    if (command.has_key("DebugMultiplier")) {
        lisaberConfig.DebugMultiplier = (int)command["DebugMultiplier"];
    }
    
    return "Ok";
}

std::string LoadConfiguration(const json::jobject& command, json::jobject& result) {
    result["Minutes"] = lisaberConfig.Minutes;
    result["ShutterOpenTime"] = lisaberConfig.ShutterOpenTime;
    result["LaserOnTime"] = lisaberConfig.LaserOnTime;
    result["ImageCount"] = lisaberConfig.ImageCount;
    result["ImageRate"] = lisaberConfig.ImageRate;
    result["FrameCount"] = lisaberConfig.FrameCount;
    result["FrameRate"] = lisaberConfig.FrameRate;
    result["DebugMultiplier"] = lisaberConfig.DebugMultiplier;
    
    return "Ok";
}

std::string LoadStatus(const json::jobject& command, json::jobject& result) {
    result["CycleCount"] = lisaberStatus.CycleCount;
    result["IsRunning"] = lisaberStatus.IsRunning;
    result["DebugCounter"] = lisaberStatus.DebugCounter;
    
    return "Ok";
}

std::string ParseCommand(std::string commandString) {
    json::jobject result;
    result["Command"] = "";
    std::string status = "Failed";

    // Parse the command string
    auto command = json::jobject::parse(commandString);
    if (command.has_key("Command")) {
        auto commandString = (std::string)command["Command"];
        result["Command"] = commandString;

        if (commandString == "Configure") {
            status = ParseConfiguration(command, result);
            status = LoadStatus(command, result);
        } else if (commandString == "GetConfiguration") {
            status = LoadConfiguration(command, result);
            status = LoadStatus(command, result);
        } else if (commandString == "GetStatus") {
            status = LoadStatus(command, result);
        } else if (commandString == "Start") {
            // Start the cycle
            multicore_fifo_push_blocking(PIV_START);
            status = LoadStatus(command, result);
            status = "Started";
        } else if (commandString == "Stop") {
            // Stop the cycle
            multicore_fifo_push_blocking(PIV_STOP);
            status = LoadStatus(command, result);
            status = "Stopped";
        } else {
            status = "Unknown command!";
        }
    }
    
    result["Status"] = status;
    return result;
}

int main()
{
    stdio_init_all();
    int rc = pico_led_init();

    // Launch core 1, wait for it to be ready.
    multicore_launch_core1(do_lisaber);
    uint32_t g = multicore_fifo_pop_blocking();
    
    auto i = 0;
    while (true) {
        std::string commandString;
        while (std::cin.peek() == EOF) {
            sleep_ms(10);
        }

        getline(std::cin, commandString);
        pico_set_led(true);
        auto response = ParseCommand(commandString);

        //printf("{\"Message\":\"Hello, world: %d!\", \"Status\":\"%s\"}\n", i, status.c_str());
        std::cout << response << std::endl;
        pico_set_led(false);

        i++;
        //sleep_ms(1000);
    }
}
