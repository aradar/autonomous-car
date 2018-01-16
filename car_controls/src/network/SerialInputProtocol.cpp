#include "SerialInputProtocol.hpp"

#include "NetworkManager.hpp"
#include "../misc/CarState.hpp"

SerialInputProtocol SerialInputProtocol::read(uint8_t* buffer) {
	SerialInputProtocol result;
	
	uint8_t options = buffer[0];
	result.side = (options & SIDE_MASK) == SIDE_MASK ? RIGHT : LEFT;
	result.direction = (options & DIRECTION_MASK) == DIRECTION_MASK ? FORWARD : BACKWARD ;
	result.debugLevel = DEBUG_MASK & options;
	result.restart_bit = (options & RESTART_MASK) == RESTART_MASK;

	result.value_steer = *(reinterpret_cast<float*> (buffer+1));
	result.value_speed = *(reinterpret_cast<float*> (buffer+5));


	return result;
}

void SerialInputProtocol::update_car_state(CarState* car_state) const
{
	car_state->side = this->side;
	car_state->steer = this->value_steer;
	car_state->steer_changed = true;
	car_state->target_speed = this->value_speed;
}
