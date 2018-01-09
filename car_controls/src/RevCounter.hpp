#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <mbed.h>

class RevCounter {
public:
	RevCounter();

	static void receive_tick();
	void start();
	float meters_per_second();
	int elasped_time();
	int count_interrupts();

private:
	static int cur_tick_;
	static int prev_tick_;
	static Timer timer_;
	static int count_interrupts_;
	InterruptIn pin_;

};

#endif
