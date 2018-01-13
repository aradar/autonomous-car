#ifndef __SEQUENCES_CLASS__
#define __SEQUENCES_CLASS__

#include "Servo.h"

namespace sequences
{
	void calibrate();
	void test_steer(Servo& steer);
	void test_drive(Servo& drive);
}

#endif
