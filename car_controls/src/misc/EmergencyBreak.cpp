#include "EmergencyBreak.hpp"

const int EmergencyBreak::THRESHOLD = 35;

EmergencyBreak::EmergencyBreak()
	: echo_one(PA_8), trig_one(PF_1), echo_two(PF_0), trig_two(PB_5), enabled(true)
{}

void EmergencyBreak::disable()
{
	enabled = false;
}

void EmergencyBreak::enable()
{
	enabled = true;
}

bool EmergencyBreak::emergency_stop() {
	if (!enabled) {
		return false;
	}
	int distance = 0;

	trig_one = 1; // send trigger signal for sensor 1
	sonar.reset();
	wait_us(10.0);
    trig_one = 0;
    while (echo_one==0) {}; // wait for echo signal
    sonar.start();
    while (echo_one==1) {};

    sonar.stop(); // stops time echo needed
    distance = (sonar.read_us())/58.0; // distance between
	printf("First: %d cm \n\r", distance);
	if(distance < THRESHOLD)
		return true;

	wait_us(10.0);

	trig_two = 1; //send trigger signal for sensor 2
	sonar.reset();
    wait_us(10.0);
    trig_two = 0;
    while (echo_two==0) {};
    sonar.start();
    while (echo_two==1) {};
    sonar.stop();
    distance = (sonar.read_us())/58.0;
	//printf("Second: %d cm \n\r", distance);
	if(distance < THRESHOLD)
		return true;

	return false;
}
