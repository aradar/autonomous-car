#ifndef __MAIN_CLASS__
#define __MAIN_CLASS__

#include "mbed.h"

class Main
{
	public:
		Main();
		void run();

	private:
		DigitalOut statusLed;

		int wait_long;
		int wait_short;
};

#endif
