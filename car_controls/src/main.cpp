#include "mbed.h"
#include "Servo.h"
#include <string>

#include "RevCounter.hpp"

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

float calculateDrive(float value_actual_speed, float value_target_speed);
float calculateSteer(float valueSteer, Side side);

void send_float(float f, Serial& ser);
void send_int(int f, Serial& ser);

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
	float current_speed;

	Side side;

	bool steer_changed;
	bool speed_changed;

	CarState() {}
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
		
		// echo
        for (int i = 0; i < BUFFER_SIZE; ++i) {
            pi.putc(rx_buffer[i]);
        }
        pi.putc('\n');
		
        
        serialReadCallback();
        received_something = true;
    }
}

float calculateSteer(float steer_Degree, Side side){
	float steer_value;
	if (side == LEFT){
		steer_value = 0.5 + steer_Degree * 0.0075 ;
	}else{
		steer_value = 0.5 - steer_Degree * 0.0075;
	}
	if (steer_value > 0.8)
		steer_value = 0.8;
	if (steer_value < 0.2)
		steer_value = 0.2;
	return steer_value;
}

float calculateDrive(float value_actual_speed, float value_target_speed)
{
	float b = 1;
	float a = 0.04;
	return b / (value_actual_speed * value_actual_speed + 1) * ((value_target_speed - value_actual_speed) * a) + 0.5;
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
	// start
	/*
	for (float f = 0.35f; f < 0.65f; f += 0.005f)
	{
		steer = f;
		wait_ms(15);
	}
	*/
	steer = 0.5f;

	// vorwaerts 
	drive = 0.65f;

	RevCounter revCounter;
	blink(0.3f);

	//revCounter.meters_per_second();

	float drive_values[] = { 0.68f, 0.65f, 0.62f, 0.59f, 0.56f, 0.59f, 0.62f, 0.65f };

	wait(1);

	for (int cycle = 0; cycle < 3; cycle++)
	{
		for (int i = 0; i < 6; i++) {
			drive = drive_values[i];
			wait(0.3);
			send_float(revCounter.meters_per_second(), pi);
		}
	}

	drive = 0.5f;

	wait(1);

	// end
	for (int i = 0; i < 3; i++)
	{
		blink(0.2f);
		wait(0.2f);
	}
}

void send_float(float f, Serial& ser)
{
	uint8_t* p = (uint8_t*)&f;
	for (int i = 0; i < sizeof(float); i++) {
		ser.putc(*p);
		p++;
	}
}

void send_int(int i, Serial& ser)
{
	send_float(i, ser);
}

DigitalOut statusLed(LED1);

void blink(float time) {
	statusLed = 1;
	wait_ms((int) (time * 1000));
	statusLed = 0;
}

bool emergencyStop(){
	Timer sonar;			
	int distance = 0;
	
	DigitalIn echo_one(PA_8);		// sensor 1
	DigitalOut trig_one(PF_1);		// sensor 1
	DigitalIn echo_two(PF_0);		// sensor 2
	DigitalOut trig_two(PB_5);		// sensor 2
		
	trig_one = 1;					// send trigger signal for sensor 1
	sonar.reset();
	wait_us(10.0);
    trig_one = 0;					
    while (echo_one==0) {};			// wait for echo signal
    sonar.start();
    while (echo_one==1) {};	
    sonar.stop();					// stops time echo needed	
    distance = (sonar.read_us())/58.0;	// distance between 
	printf("First: %d cm \n\r", distance);
	if(distance < 40)
		return true;
	
	wait_us(10.0);
	
	trig_two = 1;					//send trigger signal for sensor 2
	sonar.reset();
    wait_us(10.0);
    trig_two = 0;
    while (echo_two==0) {};
    sonar.start();
    while (echo_two==1) {};
    sonar.stop();
    distance = (sonar.read_us())/58.0;
	printf("Second: %d cm \n\r", distance);
	if(distance < 40)
		return true;
	
	return false;
}

int main() {
    //pi.attach(rx_interrupt, Serial::RxIrq);
    //pi.attach(&rx_interrupt);

	Servo drive(PA_12);
	Servo steer(PB_0);
	//calibrate(drive, steer, statusLed);
	// test
	//test_servos(drive, steer, statusLed);

	int blink_counter = 0;

	state.current_speed = 0.5f;
	state.target_speed = 0.5f;
	RevCounter revCounter;
	
    while(!emergencyStop()) {
		//printf(emergencyStop());
		/*
		state.current_speed = revCounter.meters_per_second();

        if (state.steer_changed) {
            steer = calculateSteer(state.steer, state.side);
            state.steer_changed = false;
        }
        if (state.speed_changed) {
            drive = calculateDrive(state.current_speed, state.target_speed);
            state.speed_changed = false;
        }        
		
		// blink
		blink_counter++;
		blink_counter = blink_counter % 2000;
		if (blink_counter == 0) {
			statusLed = !statusLed;
		}*/
		blink(0.5);
    }
    drive = 0;
}
