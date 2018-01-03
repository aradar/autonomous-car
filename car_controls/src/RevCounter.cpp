#include <vector>
#include <algorithm>
#include "RevCounter.hpp"
//#include <mbed.h> for rework

std::vector<std::clock_t> new_ticks;

void receive_tick()
{
	// rework this with us_ticker_read() instead of clock()
	// https://os.mbed.com/questions/61002/Equivalent-to-Arduino-millis/
	
	new_ticks.push_back(std::clock());
}

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
	// grab 2 latest ticks
	for (std::size_t i = std::max<std::size_t>(0, new_ticks.size() - 2); i < new_ticks.size(); i++)
		RevCounter::receive_tick(new_ticks[i]);

	new_ticks.clear();
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
