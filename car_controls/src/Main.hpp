#ifndef __MAIN_CLASS__
#define __MAIN_CLASS__

#include "Servo.h"
#include "mbed.h"

#include <controller/Controller.hpp>
#include <misc/CarState.hpp>

class Main
{
	public:
		Main();
		void run();
	private:
		Controller controller;
		CarState state;

		Servo drive;
		Servo steer;
};

#endif
