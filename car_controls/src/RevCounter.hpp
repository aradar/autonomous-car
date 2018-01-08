#ifndef __REV_COUNTER_CLASS__
#define __REV_COUNTER_CLASS__

#include <ctime>

void receive_tick();

class RevCounter {
public:
	RevCounter();

	void update();
	void receive_tick(std::clock_t time);
	float meters_per_second();

private:
	std::clock_t cur_tick_;
	std::clock_t prev_tick_;
};

#endif
