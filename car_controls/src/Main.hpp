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
	private:
		Controller controller;
		CarState state;
		EmergencyBreak emergency_break;

		Servo drive;
		Servo steer;
};

#endif
