#ifndef __EMERGENCYBREAK_CLASS__
#define __EMERGENCYBREAK_CLASS__

#include <mbed.h>

class EmergencyBreak
{
	public:
		EmergencyBreak();

		bool emergency_stop();
		void disable();
		void enable();

		static const int THRESHOLD;
	private:
		Timer sonar;

		DigitalIn echo_one; // sensor 1
		DigitalOut trig_one; // sensor 1
		DigitalIn echo_two; // sensor 2
		DigitalOut trig_two; // sensor 2

		bool enabled;
};

#endif
