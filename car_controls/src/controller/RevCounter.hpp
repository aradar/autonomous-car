#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <mbed.h>

#include "RingBuffer.hpp"

class RevCounter {
public:
	RevCounter();

	static void receive_tick();
	void reset();
	float meters_per_second() const;
	int count_interrupts() const;
	static Timer timer_;
	static RingBuffer<int, 100> buffer_;

private:
	int count_occurrences_after(int time, int* first) const;

	static int count_interrupts_;
	InterruptIn pin_;
};

#endif
