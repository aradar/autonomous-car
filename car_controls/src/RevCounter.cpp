#include <vector>
#include <algorithm>
#include "RevCounter.hpp"

RingBuffer<int, 100> RevCounter::buffer_;
Timer RevCounter::timer_;
int RevCounter::count_interrupts_;

RevCounter::RevCounter()
	: pin_(PA_11)
{
	reset();
}

// TODO reset timer on to prevent overflows
void RevCounter::receive_tick()
{
	count_interrupts_++;
	buffer_ << timer_.read_ms();
}

void RevCounter::reset()
{
	count_interrupts_ = 0;
	timer_.reset();
	timer_.start();
	pin_.rise(&RevCounter::receive_tick);
}

// do not give "first" a null pointer
// buffer.size() > 0
int RevCounter::count_occurrences_after(int time, int* first) {
	int count = 0;

	*first = buffer_[0];
	for (size_t i = 0; i < buffer_.size(); i++)
	{
		if (buffer_[i] > time) {
			count++;
		}
		if (*first < buffer_[i])
			*first = buffer_[i];
	}

	return count;
}

float RevCounter::meters_per_second()
{
	const float METERS_PER_REV = 0.23f;
	const int TICKS_PER_REV = 4;
	const float METERS_PER_TICK = METERS_PER_REV / TICKS_PER_REV;
	const int MONITORING_PERIOD_MS = 100;
	const float MINIMAL_SPEED = 0.0000001f;

	if (buffer_.size() == 0) {
		return 0.f;
	}

	int first;

	int now = timer_.read_ms();
	int count = count_occurrences_after(now - MONITORING_PERIOD_MS, &first);

	if (count == 1) {
		return MINIMAL_SPEED;
	}
	if (count == 0) {
		return 0.f;
	}

	//return count;
	return (count * METERS_PER_TICK * 1000.f) / std::max<int>(MONITORING_PERIOD_MS, now - first);
}

int RevCounter::count_interrupts()
{
	return count_interrupts_;
}
