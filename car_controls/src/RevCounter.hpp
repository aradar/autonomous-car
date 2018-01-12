#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <mbed.h>

#include "RingBuffer.hpp"

class RevCounter {
public:
	RevCounter();

	static void receive_tick();
	void reset();
	float meters_per_second();
	int count_interrupts();
	static Timer timer_;
	static RingBuffer<int, 100> buffer_;

private:
	int count_occurrences_after(int time, int* first);

	static int count_interrupts_;
	InterruptIn pin_;

};

#endif
