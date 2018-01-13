#ifndef __LEDHANDLER_CLASS__
#define __LEDHANDLER_CLASS__

#include "Servo.h"

class LEDHandler
{
	public:
		static void blink_blocking(float time);
		static void blink_async(int ticks);
		static void blink_blocking(float time, unsigned int count);

		static void update();

		static void on();
		static void off();

		static void toggle();
	private:
		LEDHandler();
		static DigitalOut status_led;

		static int blink_counter;
};

#endif
