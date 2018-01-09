#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <mbed.h>

void receive_tick();

class RevCounter {
public:
	RevCounter();

	static void receive_tick();
	void start();
	float meters_per_second();

private:
	static int cur_tick_;
	static int prev_tick_;
	static Timer timer_;
};

#endif
