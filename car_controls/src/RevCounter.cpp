#include <vector>
#include <algorithm>
#include "RevCounter.hpp"

RevCounter::RevCounter()
	: cur_tick_(0), prev_tick_(0)
{
	timer_.start();
}

void RevCounter::receive_tick(int time)
{
	prev_tick_ = cur_tick_;
	cur_tick_ = time;
}

void RevCounter::update()
{
	static bool active = false;
	//bool pin = std::rand() % 2;
	DigitalIn pin(PA_11);

	if (!active && pin) {
		active = true;
		receive_tick(timer_.read_ms());
	} else if(active && !pin) {
		active = false;
	}
}

float RevCounter::meters_per_second()
{
	const float METERS_PER_REV = 1.f;
	const int TICKS_PER_REV = 4;
	const float METERS_PER_TICK = METERS_PER_REV / TICKS_PER_REV;

	if (cur_tick_ == 0 && prev_tick_ == 0)
		return 0.f;

	float deltaTime = cur_tick_ - prev_tick_;

	// if car gets slower, predict speed to maximum possible speed
	if (timer_.read_ms() < cur_tick_ + deltaTime)
		deltaTime = timer_.read_ms() - cur_tick_;

	return METERS_PER_TICK / (deltaTime / 1000.f);
}
