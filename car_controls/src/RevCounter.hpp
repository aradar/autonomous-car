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
	bool overflowed();

private:
	static long long cur_tick_;
	static long long prev_tick_;
	static Timer timer_;
	static bool overflowed_;
	static int count_interrupts_;
	InterruptIn pin_;

};

#endif
