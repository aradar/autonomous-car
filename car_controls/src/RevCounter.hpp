#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <mbed.h>

static int countInterrupts = 0;

class RevCounter {
public:
	RevCounter();

	static void receive_tick();
	void start();
	float meters_per_second();
	int elasped_time();

private:
	static int cur_tick_;
	static int prev_tick_;
	static Timer timer_;
};

#endif
