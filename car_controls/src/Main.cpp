#include "Main.hpp"

#include "Servo.h"

#include <misc/sequences.hpp>
#include <debug/LEDHandler.hpp>

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
	const int blink_period = 50;

	state.target_speed = 0.5f;
	state.steer_changed = true;

	network_manager.init(state);

    while(1) {
		controller.update(drive);

		// update current speed
		state.current_speed = controller.meters_per_second_approx();

		network_manager.update_car_state(&state);

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
			network_manager.send(state.current_speed);
			network_manager.send(state.target_speed);
			network_manager.send(drive);
		}

		wait(0.01f);
    }
}
