/*
Translated by ChatGPT 20230225
*/
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"

#define ROTENC_PIN_A 5
#define ROTENC_PIN_B 6


static int32_t value = 0;
static uint8_t bq = 0;
static bool changed = false;

void rotenc_callback(uint gpio, uint32_t events) {
    fixit();
}

void fixit() {
    uint32_t flags = (gpio_get_irq_status(ROTENC_PIN_A) & GPIO_IRQ_EDGE_FALL) |
                     (gpio_get_irq_status(ROTENC_PIN_A) & GPIO_IRQ_EDGE_RISE) |
                     ((gpio_get_irq_status(ROTENC_PIN_B) & GPIO_IRQ_EDGE_FALL) >> 2) |
                     ((gpio_get_irq_status(ROTENC_PIN_B) & GPIO_IRQ_EDGE_RISE) >> 2);
    if (flags == 0b1010) {
        if ((bq & 0b011001011001) == 0b011001011001) {
            value -= 1;
        } else if ((bq & 0b100101010110) == 0b100101010110) {
            value += 1;
        }
        bq = 0;
        changed = true;
    } else if (flags != (bq & 0b1111)) {
        bq = (bq << 4) | flags;
    }
}

int main() {
    gpio_init(ROTENC_PIN_A);
    gpio_init(ROTENC_PIN_B);
    gpio_set_dir(ROTENC_PIN_A, GPIO_IN);
    gpio_set_dir(ROTENC_PIN_B, GPIO_IN);
    gpio_pull_up(ROTENC_PIN_A);
    gpio_pull_up(ROTENC_PIN_B);
    gpio_set_irq_enabled_with_callback(ROTENC_PIN_A, GPIO_IRQ_EDGE_FALL | GPIO_IRQ_EDGE_RISE, true, &rotenc_callback);
    gpio_set_irq_enabled_with_callback(ROTENC_PIN_B, GPIO_IRQ_EDGE_FALL | GPIO_IRQ_EDGE_RISE, true, &rotenc_callback);
    
    while (true) {
        if (changed) {
            printf("%d\n", value);
            changed = false;
        }
        sleep_ms(1);
    }

    return 0;
}
