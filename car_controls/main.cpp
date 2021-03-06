#include "mbed.h"
#include "Servo.h"

uint8_t const MODE_MASK = 0x80;
uint8_t const DIRECTION_MASK = 0x40;
uint8_t const DEBUG_MASK = ~ (MODE_MASK | DIRECTION_MASK);

bool received_something = false;
int wait_millis = 0;

//Serial pc(USBTX, USBRX); // tx, rx
Serial pi(PB_6, PB_7, 9600); //UART1_TX / D4, UART1_RX / D5
DigitalOut statusLed(LED1);

struct SerialInputProtocol {
    enum {STEER, DRIVE} mode;
    enum {FORWARD, BACKWARD} direction;

    char debugLevel;
    float value;

    static SerialInputProtocol read(uint8_t* buffer) {
        SerialInputProtocol result;
        
        uint8_t options = buffer[0];
        result.mode = (options & MODE_MASK) == MODE_MASK ? DRIVE : STEER;
        result.direction = (options & DIRECTION_MASK) == DIRECTION_MASK ? BACKWARD : FORWARD;
        result.debugLevel = DEBUG_MASK & options;
        
        //unsigned int value_as_int = value1_as_byte*16777216 + value2_as_byte*65536 + value3_as_byte*256 + value4_as_byte;
        //int value_as_int = (*((int*) (buffer + 1)));
        result.value = (*((int*) (buffer + 1))) / 100.f;
             
        return result;
    }
};

struct CarState {
    Servo drive;
    Servo steer;
    
    float drive_update;
    float steer_update;
    
    bool drive_changed;
    bool steer_changed;
    
    CarState(PinName drive_pin, PinName steer_pin)
        : drive(drive_pin), steer(steer_pin) {
    }
};

CarState state(PA_12, PB_0);

int const BUFFER_SIZE = 5;
uint8_t rx_buffer[BUFFER_SIZE];

void serialReadCallback() {
    SerialInputProtocol input = SerialInputProtocol::read(rx_buffer);
    
    if (input.mode == SerialInputProtocol::STEER) {
        if (input.direction == SerialInputProtocol::FORWARD) {
            state.steer_update = input.value;
        } else {
            state.steer_update = 1 - input.value;
        }
        state.steer_changed = true;
    } else if (input.mode == SerialInputProtocol::DRIVE) {
        pi.putc('a');
        pi.putc('\n');
        if (input.direction == SerialInputProtocol::FORWARD) {
            state.drive_update = input.value;
        } else {
            state.drive_update = 1 - input.value;
        }
        state.drive_changed = true;
    }
}

int rx_fuck_off = 0;

void rx_interrupt() {
    received_something = false;
    
    rx_buffer[rx_fuck_off] = pi.getc();
    
    rx_fuck_off = ++rx_fuck_off % BUFFER_SIZE;
    if (rx_fuck_off == 0) {
        for (int i = 0; i < BUFFER_SIZE; ++i) {
            pi.putc(rx_buffer[i]);
        }
        pi.putc('\n');
        
        serialReadCallback();
        received_something = true;
    }
}

int main() {
    //pi.attach(rx_interrupt, Serial::RxIrq);
    pi.attach(&rx_interrupt);
    
    wait(1);
    
    while(1) {
        //__disable_irq();

        if (state.drive_changed) {
            state.drive = state.drive_update;
            state.drive_changed = false;
        }
        if (state.steer_changed) {
            state.steer = state.steer_update;
            state.steer_changed = false;
        }
        //__enable_irq();
        
        wait_ms(wait_millis);
        
        if (received_something) {
            statusLed = 1;
        }
        
        wait_ms(wait_millis);
        statusLed = 0;
    }
}