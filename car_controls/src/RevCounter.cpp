#include <vector>
#include <algorithm>
#include "RevCounter.hpp"

InterruptIn pin(PA_11);

int RevCounter::cur_tick_;
int RevCounter::prev_tick_;
Timer RevCounter::timer_;

RevCounter::RevCounter()
{
	start();
}

void RevCounter::receive_tick()
{
	countInterrupts++;
	int time = timer_.read_ms();
	prev_tick_ = cur_tick_;
	cur_tick_ = time;
}

void RevCounter::start()
{
	cur_tick_ = 0;
	prev_tick_ = 0;
	timer_.reset();
	timer_.start();
	pin.rise(&RevCounter::receive_tick);
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

int RevCounter::elasped_time()
{
	return timer_.read_ms();
}
