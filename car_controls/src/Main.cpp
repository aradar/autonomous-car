#include "Main.hpp"

#include "Servo.h"

#include "sequences.hpp"
#include "LEDHandler.hpp"

Main::Main()
	: drive(PA_12), steer(PB_0)
{}

void Main::run()
{
	network_manager.init();

	sequences::calibrate();

	// test
	wait(1);
	sequences::test_steer(steer);
	sequences::test_drive(drive);

	int blink_counter = 0;

	state.target_speed = 1.5f;
	state.steer_changed = true;
	
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
		blink_counter = (blink_counter + 1) % 1000;
		if (blink_counter == 0) {
			LEDHandler::toggle();
			//send_float(state.current_speed, pi);
			//send_float(drive, pi);
		}
    }
}
