#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <mbed.h>

void receive_tick();

class RevCounter {
public:
	RevCounter();

	void update();
	void receive_tick(int time);
	float meters_per_second();

private:
	int cur_tick_;
	int prev_tick_;
	Timer timer_;
};

#endif
