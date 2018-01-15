#include "CarState.hpp"

CarState::CarState()
	: steer(0.f), side(RIGHT), steer_changed(false), target_speed(0.f), current_speed(0.f)
{ }

void CarState::update_from(const CarState& other)
{
	this->target_speed = other.target_speed;
	this->side = other.side;
	this->steer = other.steer;
	steer_changed = true;
}
