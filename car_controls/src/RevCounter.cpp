#include <vector>
#include <algorithm>
#include "RevCounter.hpp"
#include <mbed.h>

RevCounter::RevCounter()
	: cur_tick_(0), prev_tick_(0)
{}

void RevCounter::receive_tick(std::clock_t time)
{
	prev_tick_ = cur_tick_;
	cur_tick_ = time;
}

void RevCounter::update()
{
	static bool active = false;
	DigitalIn pin(PA_11);

	if (!active && pin) {
		active = true;
		receive_tick(std::clock());
	} else if(active && !pin) {
		active = false;
	}
}

float RevCounter::meters_per_second()
{
	const double METERS_PER_REV = 1.f;
	const int TICKS_PER_REV = 1;

	if (cur_tick_ == 0 && prev_tick_ == 0)
		return 0.f;

	double deltaTime = static_cast<double>(cur_tick_ - prev_tick_) / CLOCKS_PER_SEC;
	return METERS_PER_REV / deltaTime / TICKS_PER_REV;
}
