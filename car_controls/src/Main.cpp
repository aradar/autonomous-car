#include "Main.hpp"

#include "Servo.h"

#include "NetworkManager.hpp"
//#include "SerialInputProtocol.hpp"
//#include "CarState.hpp"

Main::Main()
	: statusLed(LED1), wait_long(1000), wait_short(100)
{}

void Main::run()
{
    wait(1);

	nm::pi.attach(&nm::rx_interrupt);

	int wait_time = wait_long;

    while(1) {
		//nm::rx_interrupt();
		/*
		if (nm::has_update())
		{
			SerialInputProtocol input = nm::get_update();
			if (input.steer_ == 0.2f) {
				wait_time = wait_short;
			}
		}
		*/

		if (nm::received_something) {
			wait_time = wait_short;
		}

		// blinking
        wait_ms(wait_time);
		statusLed = !statusLed;
    }
}
