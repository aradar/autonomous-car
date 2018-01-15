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
	const int blink_period = 250;

	state.target_speed = 0.f;
	state.steer_changed = true;

	NetworkManager::init(state);

    while(1) {
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

		wait(0.01f);
    }
}
