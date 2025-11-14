#include <stdio.h>
#include <iostream>
#include <string>
#include "pico/stdlib.h"

// Perform initialisation
int pico_led_init(void) {
    #if defined(PICO_DEFAULT_LED_PIN)
        // A device like Pico that uses a GPIO for the LED will define PICO_DEFAULT_LED_PIN
        // so we can use normal GPIO functionality to turn the led on and off
        gpio_init(PICO_DEFAULT_LED_PIN);
        gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
        return PICO_OK;
    #elif defined(CYW43_WL_GPIO_LED_PIN)
        // For Pico W devices we need to initialise the driver etc
        return cyw43_arch_init();
    #endif
}
    
    // Turn the led on or off
    void pico_set_led(bool led_on) {
    #if defined(PICO_DEFAULT_LED_PIN)
        // Just set the GPIO on or off
        gpio_put(PICO_DEFAULT_LED_PIN, led_on);
    #elif defined(CYW43_WL_GPIO_LED_PIN)
        // Ask the wifi "driver" to set the GPIO on or off
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
    #endif
}
    
    

int main()
{
    stdio_init_all();
    int rc = pico_led_init();

    auto i = 0;
    while (true) {
        pico_set_led(true);
        std::string command;
        while (std::cin.peek() == EOF) {
            sleep_ms(10);
        }
        getline(std::cin, command);

        sleep_ms(2000);
        printf("{\"Message\":\"Hello, world: %d!\", \"Status\":\"Ok\"}\n", i);
        //std::cout << command << std::endl;
        i++;
        pico_set_led(false);
        sleep_ms(1000);
    }
}
