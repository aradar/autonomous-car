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

enum Side { LEFT, RIGHT };
enum Direction { BACKWARD, FORWARD };
enum Movement { STANDING, MOVING_BACKWARD, MOVING_FORWARD };

float calculateDrive(float value_actual_speed, Movement actual_movement, float value_target_speed, Movement target_movement);
float calculateSteer(float valueSteer, Side side);

void blink(float f);

struct SerialInputProtocol {
	Side side;
	Direction direction;

    char debugLevel;
    float value_steer;
    float value_speed;

    static SerialInputProtocol read(uint8_t* buffer) {
        SerialInputProtocol result;
        
        uint8_t options = buffer[0];
        result.side = (options & SIDE_MASK) == SIDE_MASK ? RIGHT : LEFT;
        result.direction = (options & DIRECTION_MASK) == DIRECTION_MASK ? FORWARD : BACKWARD ;
        result.debugLevel = DEBUG_MASK & options;

		result.value_steer = *((float*) buffer+1);
		result.value_speed = - *((float*) buffer+5);
             
        return result;
    }
};

struct CarState {
	float steer;

	float target_speed;
	float actual_speed;

	Side side;

	Movement target_movement;
	Movement actual_movement;

	bool speed_changed;
	bool steer_changed;

	CarState()
		: target_movement(STANDING), actual_movement(STANDING)
	{}
};

int const BUFFER_SIZE = 9;
uint8_t rx_buffer[BUFFER_SIZE];

CarState state;

void serialReadCallback() {
    SerialInputProtocol input = SerialInputProtocol::read(rx_buffer);

	state.target_speed = input.value_speed;
	state.steer = input.value_steer;

	state.speed_changed = true;
	state.steer_changed = true;
}

int rx_buffer_size = 0;

void rx_interrupt() {
    received_something = false;
    
    rx_buffer[rx_buffer_size] = pi.getc();
    
	rx_buffer_size++;
    rx_buffer_size = rx_buffer_size % BUFFER_SIZE;
    if (rx_buffer_size == 0) {
		/*
		// echo
        for (int i = 0; i < BUFFER_SIZE; ++i) {
            pi.putc(rx_buffer[i]);
        }
        pi.putc('\n');
		*/
        
        serialReadCallback();
        received_something = true;
    }
}

float calculateSteer(float value_steer, Side side){
	if (value_steer > 0.4){
		value_steer=0.4;
	}
	if (side == LEFT){
		return 0.4 - (value_steer/10);
	}else{
		return 0.4 + (value_steer/10);
	}
}

// wrong
float calculateDrive(float value_actual_speed, Movement actual_movement, float value_target_speed, Movement target_movement)
{
	// TODO
	return 0.f;
}

const int CALIBRATION_TIME = 2;

// send calibration signals
void calibrate(Servo& drive, Servo& steer, DigitalOut& statusLed) {
	// blink initial
	for (int i = 0; i < 3; i++) {
		wait(0.5f);
		blink(0.5f);
	}

	wait(CALIBRATION_TIME);

	// blink end
	for (int i = 0; i < 3; i++) {
		wait(0.2f);
		blink(0.2f);
	}
}

void test_servos(Servo& drive, Servo& steer, DigitalOut& statusLed)
{
	for (float f = 0.35f; f < 0.65f; f += 0.005f)
	{
		steer = f;
		wait_ms(15);
	}
	steer = 0.5f;

	// vorwaerts 
	drive = 0.65f;
	blink(0.5f);

	drive = 0.5f;
	wait(2);

	for (int i = 0; i < 3; i++)
	{
		blink(0.2f);
		wait(0.2f);
	}
}

DigitalOut statusLed(LED1);

void blink(float time) {
	statusLed = 1;
	wait_ms((int) (time * 1000));
	statusLed = 0;
}

int main() {
    //pi.attach(rx_interrupt, Serial::RxIrq);
    //pi.attach(&rx_interrupt);

	Servo drive(PA_12);
	Servo steer(PB_0);

	calibrate(drive, steer, statusLed);

	test_servos(drive, steer, statusLed);

	/*
    while(1) {
        if (state.steer_changed) {
            steer = calculateSteer(state.steer, state.side);
            state.steer_changed = false;
        }
        if (state.speed_changed) {
            drive = calculateDrive(state.actual_speed, state.actual_movement, state.target_speed, state.target_movement);
            state.speed_changed = false;
        }        

		// blink
		blink_counter++;
		blink_counter = blink_counter % 2000;
		if (blink_counter == 0) {
			statusLed = !statusLed;
		}
    }
	*/
}
