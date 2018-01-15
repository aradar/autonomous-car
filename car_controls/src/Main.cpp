#include "Main.hpp"

#include "Servo.h"

#include <misc/sequences.hpp>
#include <debug/LEDHandler.hpp>
#include <network/NetworkManager.hpp>

int main() {
	Main main;
	main.run();
	return 0;
}

Main::Main()
	: drive(PA_12), steer(PB_0)
{}

bool Main::emergencyStop(){
	Timer sonar;
	int distance = 0;
	const int THRESHOLD = 35;

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
	if(distance < THRESHOLD)
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
	if(distance < THRESHOLD)
		return true;

	return false;
}

void Main::run()
{
	// calibrate
	sequences::calibrate();

	// test
	wait(1);
	/*
	sequences::test_steer(steer);
	sequences::test_drive(drive);
	*/

	int blink_counter = 0;
	const int blink_period = 7;

	state.target_speed = 0.f;
	state.steer_changed = true;

	NetworkManager::init(state);

    while(1 /*!emergencyStop()*/) {
		controller.update(drive);

		// update current speed
		state.current_speed = controller.meters_per_second_approx();

		NetworkManager::update_car_state(&state);

		// update steer
        if (state.steer_changed) {
            steer = controller.calculate_steer(state.steer, state.side);
            state.steer_changed = false;
        }

		// update drive
		drive = controller.calculate_drive(state.current_speed, state.target_speed);

		LEDHandler::update();
     	
		// blink
		blink_counter = (blink_counter + 1) % blink_period;
		if (blink_counter == 0) {
			LEDHandler::toggle();
			//NetworkManager::send(state.current_speed);
			//NetworkManager::send(state.target_speed);
			//NetworkManager::send(state.steer);
			NetworkManager::send((float)state.side);
		}

		wait(0.04f);
    }

	drive = 0;

	LEDHandler::blink_blocking(0.1f, 10);
}
