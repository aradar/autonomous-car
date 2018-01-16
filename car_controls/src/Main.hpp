#ifndef __MAIN_CLASS__
#define __MAIN_CLASS__

#include "Servo.h"
#include "mbed.h"

#include <controller/Controller.hpp>
#include <misc/CarState.hpp>
#include <misc/EmergencyBreak.hpp>

class Main
{
	public:
		Main();
		void run();
		bool emergencyStop();
		void handle_blink();
	private:
		enum Mode {
			NORMAL,
			IGNORING
		};
		Controller controller;
		CarState state;
		EmergencyBreak emergency_break;

		// NORMAL: receiving signals from pi, updating steer and drive values depending on target_speed and target_steer
		// IGNORING: receiving signals from pi, but does not drive or steer anymore. Can be set to normal mode with flag
		Mode mode;

		Servo drive;
		Servo steer;

		int blink_counter;
		int blink_period;

		static const int NORMAL_BLINK_PERIOD;
		static const int IGNORING_BLINK_PERIOD;
};

#endif
