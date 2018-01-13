#include "CarState.hpp"

void CarState::update_from(const CarState& other)
{
	this->target_speed = other.target_speed;
	this->side = other.side;
	this->steer = other.steer;
	steer_changed = true;
}
