#ifndef __CARSTATE_CLASS__
#define __CARSTATE_CLASS__

#include "directions.hpp"

struct CarState {
	CarState() {}
	void update_from(const CarState& other);

	float steer;
	Side side;
	bool steer_changed;

	float target_speed;
	float current_speed;
};

#endif
