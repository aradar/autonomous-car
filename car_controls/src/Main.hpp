#ifndef __MAIN_CLASS__
#define __MAIN_CLASS__

#include "Servo.h"
#include "mbed.h"

#include "Controller.hpp"
#include "CarState.hpp"
#include "NetworkManager.hpp"

class Main
{
	public:
		Main();
		void run();
	private:
		Controller controller;
		CarState state;
		NetworkManager network_manager;

		Servo drive;
		Servo steer;
};

#endif
