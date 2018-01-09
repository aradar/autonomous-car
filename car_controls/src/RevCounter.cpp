#include <vector>
#include <algorithm>
#include "RevCounter.hpp"

long long RevCounter::cur_tick_;
long long RevCounter::prev_tick_;
Timer RevCounter::timer_;
int RevCounter::count_interrupts_;

RevCounter::RevCounter()
	: pin_(PA_11)
{
	start();
}

// TODO reset timer on to prevent overflows
void RevCounter::receive_tick()
{
	count_interrupts_++;
	int time = timer_.read_us();
	prev_tick_ = cur_tick_;
	cur_tick_ = time;
}

void RevCounter::start()
{
	cur_tick_ = 0;
	prev_tick_ = 0;
	count_interrupts_ = 0;
	timer_.reset();
	timer_.start();
	pin_.rise(&RevCounter::receive_tick);
}

float RevCounter::meters_per_second()
{
	const float METERS_PER_REV = 0.23f;
	const int TICKS_PER_REV = 4;
	const float METERS_PER_TICK = METERS_PER_REV / TICKS_PER_REV;

	if (cur_tick_ == 0 && prev_tick_ == 0)
		return 0.f;

	long long deltaTime = cur_tick_ - prev_tick_;

	// if car gets slower, predict speed to maximum possible speed
	if (timer_.read_us() < cur_tick_ + deltaTime)
		deltaTime = timer_.read_us() - cur_tick_;

	return METERS_PER_TICK / (deltaTime / 1000000.f);
}

int RevCounter::elasped_time()
{
	return timer_.read_us();
}

int RevCounter::count_interrupts()
{
	return count_interrupts_;
}
