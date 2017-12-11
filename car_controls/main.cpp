#include "mbed.h"
#include "Servo.h"
#include <string>

uint8_t const SIDE_MASK = 0x80;
uint8_t const DIRECTION_MASK = 0x40;
uint8_t const DEBUG_MASK = ~(SIDE_MASK | DIRECTION_MASK);

bool received_something = false;
int wait_millis = 0;

//Serial pc(USBTX, USBRX); // tx, rx
Serial pi(PB_6, PB_7, 9600); //UART1_TX / D4, UART1_RX / D5
DigitalOut statusLed(LED1);

float calculateSpeed(float valueSpeed, string direction);
float calculateSteer(float valueSteer, string side);

struct SerialInputProtocol {
    enum {LEFT, RIGHT} side;
    enum {BACKWARD, FORWARD} direction;

    char debugLevel;
    float valueSteer;
    float valueSpeed;

    static SerialInputProtocol read(uint8_t* buffer) {
        SerialInputProtocol result;
        
        uint8_t options = buffer[0];
        result.side = (options & SIDE_MASK) == SIDE_MASK ? RIGHT : LEFT;
        result.direction = (options & DIRECTION_MASK) == DIRECTION_MASK ? FORWARD : BACKWARD ;
        result.debugLevel = DEBUG_MASK & options;
        result.valueSteer = (*((int*) (++buffer)));
        result.valueSpeed = (*((int*) (++buffer)));
             
        return result;
    }
};

struct CarState {
    Servo steer;
    Servo drive;

    float steer_update;
    float drive_update;
    
    bool drive_changed;
    bool steer_changed;
    
    CarState(PinName DRIVE_pin, PinName STEER_pin)
        : drive(DRIVE_pin), steer(STEER_pin){
    }
};

CarState state(PA_12, PB_0);

int const BUFFER_SIZE = 5;
uint8_t rx_buffer[BUFFER_SIZE];

void serialReadCallback() {
    SerialInputProtocol input = SerialInputProtocol::read(rx_buffer);
    
    if (input.side == SerialInputProtocol::LEFT) {
        if (input.direction == SerialInputProtocol::FORWARD) {		// Forward Left
            state.drive_update = calculateSpeed(input.valueSpeed, "FORWARD");
            state.steer_update = calculateSteer(input.valueSteer, "LEFT");
        } else {													// Backwards Left
        	state.drive_update = calculateSpeed(input.valueSpeed, "BACKWARDS");				
            state.steer_update = calculateSteer(input.valueSteer, "LEFT");				
        }
    } else if (input.side == SerialInputProtocol::RIGHT) {
        if (input.direction == SerialInputProtocol::FORWARD) {		// Forward Right
            state.drive_update = calculateSpeed(input.valueSpeed, "FORWARD");
            state.steer_update = calculateSteer(input.valueSteer, "RIGHT");
        } else {													// Backwards Right
            state.drive_update = calculateSpeed(input.valueSpeed, "BACKWARDS");
            state.steer_update = calculateSteer(input.valueSteer, "RIGHT");	
        }
    }
    state.drive_changed = true;
    state.steer_changed = true;
}

int rx_buffer_size = 0;

void rx_interrupt() {
    received_something = false;
    
    rx_buffer[rx_buffer_size] = pi.getc();
    
    rx_buffer_size = ++rx_buffer_size % BUFFER_SIZE;
    if (rx_buffer_size == 0) {
        for (int i = 0; i < BUFFER_SIZE; ++i) {
            pi.putc(rx_buffer[i]);
        }
        pi.putc('\n');
        
        serialReadCallback();
        received_something = true;
    }
}

float calculateSteer(float valueSteer, string side){
	if (valueSteer > 0.4){
		valueSteer=0.4;
	}
	if (side=="LEFT"){
		return 0.4 - (valueSteer/10);
	}else{
		return 0.4 + (valueSteer/10);
	}
}

float calculateSpeed(float valueSpeed, string direction){
	if (valueSpeed == 0.0){
			return 0;
	}
	
	if (valueSpeed > 3){ 
		valueSpeed = 3;
	}
	
	if (direction=="FORWARD"){
		return valueSpeed/10 + 0.5;
	}else{
		return valueSpeed/10;
	}
}

int main() {
    //pi.attach(rx_interrupt, Serial::RxIrq);
    pi.attach(&rx_interrupt);
    
    wait(1);
    
    while(1) {
        if (state.steer_changed) {
            state.steer = state.steer_update;
            state.steer_changed = false;
        }
        if (state.drive_changed) {
            state.drive = state.drive_update;
            state.drive_changed = false;
        }        

        wait_ms(wait_millis);
        
        if (received_something) {
            statusLed = 1;
        }
        
        wait_ms(wait_millis);
        statusLed = 0;
    }
}