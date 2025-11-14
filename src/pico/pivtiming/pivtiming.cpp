#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/timer.h"
#include "hardware/clocks.h"

int64_t alarm_callback(alarm_id_t id, void *user_data) {
    // Put your timeout handler code in here
    return 0;
}

constexpr int LASER_TIMER_PIN0 = 0;
constexpr int LASER_TIMER_PIN1 = 1;
constexpr int LASER_TIMER_PIN2 = 2;
constexpr int LASER_TIMER_PIN3 = 3;
constexpr int LASER_TIMER_PIN4 = 4;
constexpr int LASER_TIMER_PIN5 = 5;
constexpr int LASER_TIMER_PIN6 = 6;
constexpr int LASER_TIMER_PIN7 = 7;

constexpr int LASER_TIMER_SELECT0 = 10;
constexpr int LASER_TIMER_SELECT1 = 11;
constexpr int LASER_TIMER_SELECT2 = 12;
constexpr int LASER_TIMER_SELECT3 = 13;

constexpr uint32_t LASER_TIMER_MASK = 0xff; // Mask for pins 0-7

constexpr uint32_t LASER_TIMER_1S = 1000;      // 1 second in milliseconds
constexpr uint32_t LASER_TIMER_100MS = 100;    // 100 milliseconds
constexpr uint32_t LASER_TIMER_10MS = 10;      // 10 milliseconds
constexpr uint32_t LASER_TIMER_1MS = 1;        // 1 millisecond

int32_t delay_counter = 0;

bool repeating_callback(struct repeating_timer *t) {
    delay_counter--;
    if (delay_counter > 0) {
        return true; // Continue the timer
    }

    uint32_t pattern = (uint32_t)(uintptr_t)t->user_data;
    pattern = (pattern << 1) & LASER_TIMER_MASK; // Shift left and wrap around
    if (pattern == 0) {
        pattern = 0x01010101 & LASER_TIMER_MASK; // Reset to first pin if all are off
    }
    gpio_put_masked(LASER_TIMER_MASK, pattern); // 0xFF mask for GPIO 0-7
    
    t->user_data = (void*)(uintptr_t)pattern; // Update user_data with new pattern


    // Read the timer selection and set delay_counter to the fastest selected timer
    if (!gpio_get(LASER_TIMER_SELECT3)) {
        delay_counter = LASER_TIMER_1MS;
    } else if (!gpio_get(LASER_TIMER_SELECT2)) {
        delay_counter = LASER_TIMER_10MS;
    } else if (!gpio_get(LASER_TIMER_SELECT1)) {
        delay_counter = LASER_TIMER_100MS;
    } else if (!gpio_get(LASER_TIMER_SELECT0)) {
        delay_counter = LASER_TIMER_1S;
    } else {
        delay_counter = LASER_TIMER_1S; // Default to 1 second if none selected
    }

    return true; // Return true to keep repeating
}

void piv_timing_init()
{
    // Initialize GPIO LED pins 0-7 as outputs
    gpio_init(LASER_TIMER_PIN0);
    gpio_set_dir(LASER_TIMER_PIN0, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN1);
    gpio_set_dir(LASER_TIMER_PIN1, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN2);
    gpio_set_dir(LASER_TIMER_PIN2, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN3);
    gpio_set_dir(LASER_TIMER_PIN3, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN4);
    gpio_set_dir(LASER_TIMER_PIN4, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN5);
    gpio_set_dir(LASER_TIMER_PIN5, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN6);
    gpio_set_dir(LASER_TIMER_PIN6, GPIO_OUT);
    gpio_init(LASER_TIMER_PIN7);
    gpio_set_dir(LASER_TIMER_PIN7, GPIO_OUT);

    gpio_init(LASER_TIMER_SELECT0);
    gpio_set_dir(LASER_TIMER_SELECT0, GPIO_IN);
    gpio_pull_up(LASER_TIMER_SELECT0);
    gpio_init(LASER_TIMER_SELECT1);
    gpio_set_dir(LASER_TIMER_SELECT1, GPIO_IN);
    gpio_pull_up(LASER_TIMER_SELECT1);
    gpio_init(LASER_TIMER_SELECT2);
    gpio_set_dir(LASER_TIMER_SELECT2, GPIO_IN);
    gpio_pull_up(LASER_TIMER_SELECT2);
    gpio_init(LASER_TIMER_SELECT3);
    gpio_set_dir(LASER_TIMER_SELECT3, GPIO_IN);
    gpio_pull_up(LASER_TIMER_SELECT3);
}


int main()
{
    stdio_init_all();
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);

    piv_timing_init();
    
    // Set up a repeating timer that fires every 1000 ms
    struct repeating_timer timer;
    add_repeating_timer_us(1000, repeating_callback, NULL, &timer);
    timer.user_data = (void*)1;

    while (true) {
        printf("LASER timing status\n");

        auto OneSecond = !gpio_get(LASER_TIMER_SELECT0);
        printf("'One Second'        %s selected\n", OneSecond ? "IS    " : "is not");
        auto OneHundredMs = !gpio_get(LASER_TIMER_SELECT1);
        printf("'100 Millisecond'   %s selected\n", OneHundredMs ? "IS    " : "is not");
        auto TenMs = !gpio_get(LASER_TIMER_SELECT2);
        printf("'10 Millisecond'    %s selected\n", TenMs ? "IS    " : "is not");
        auto OneMs = !gpio_get(LASER_TIMER_SELECT3);
        printf("'One Millisecond'   %s selected\n", OneMs ? "IS    " : "is not");

        gpio_put(PICO_DEFAULT_LED_PIN, 1);
        sleep_ms(500);
        gpio_put(PICO_DEFAULT_LED_PIN, 0);
        sleep_ms(250);
    }
}
