#include "Main.hpp"

#include "Servo.h"

#include <misc/sequences.hpp>
#include <debug/LEDHandler.hpp>
#include <network/NetworkManager.hpp>

const int Main::NORMAL_BLINK_PERIOD = 12;
const int Main::IGNORING_BLINK_PERIOD = 1;

int main() {
	Main main;
	main.run();
	return 0;
}

Main::Main()
	: mode(NORMAL), drive(PA_12), steer(PB_0), blink_counter(0), blink_period(NORMAL_BLINK_PERIOD)
{}

void Main::handle_blink() {
	LEDHandler::update();

	// blink
	blink_counter = (blink_counter + 1) % blink_period;
	if (blink_counter == 0) {
		LEDHandler::toggle();
		NetworkManager::send(state.current_speed);
		//NetworkManager::send(state.target_speed);
		//NetworkManager::send(state.steer);
		//NetworkManager::send((float)state.side);
	}
}


void Main::run()
{
	emergency_break.disable();

	// calibrate
	sequences::calibrate();

	// test
	wait(1);
	/*
	sequences::test_steer(steer);
	sequences::test_drive(drive);
	*/

	state.target_speed = 0.f;
	state.steer_changed = true;

	NetworkManager::init(state);

	while(1) {
		if (emergency_break.emergency_stop()) {
			mode = IGNORING;

			state.target_speed = 0.f;
			steer = 0.5f;
			blink_period = IGNORING_BLINK_PERIOD;
		}

		// update current speed
		state.current_speed = controller.meters_per_second_approx();

		if (mode == NORMAL) {
			controller.update(drive);

			NetworkManager::update_car_state(&state);

			// update steer
			if (state.steer_changed) {
				steer = controller.calculate_steer(state.steer, state.side);
				state.steer_changed = false;
			}

			// update drive
			drive = controller.calculate_drive(state.current_speed, state.target_speed);

		} else if (mode == IGNORING) {
			if (NetworkManager::restart_bit_received) {
				NetworkManager::restart_bit_received = false;
				mode = NORMAL;
				blink_period = NORMAL_BLINK_PERIOD;
			}

			drive = controller.calculate_drive(state.current_speed, 0.f);
		}
		handle_blink();
		wait(0.04f);
	}

	drive = 0;

	LEDHandler::blink_blocking(0.05f, 10);
}
