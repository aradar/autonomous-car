#include "Main.hpp"

#include "Servo.h"

#include "NetworkManager.hpp"
#include "SerialInputProtocol.hpp"
#include "CarState.hpp"

Main::Main()
	: statusLed(LED1), wait_long(1000), wait_short(200)
{}

void Main::run()
{
	wait(1);
	int wait_time = wait_long;

	while(1) {
		if (nm::has_update())
		{
			wait_time = wait_short;
			nm::get_update();
		}

		// blinking
		wait_ms(wait_time);
		statusLed = 1;
		wait_ms(wait_time);
		statusLed = 0;
	}
}


DigitalOut statusLed(LED1);

int wait_long = 1000;
int wait_short = 200;
