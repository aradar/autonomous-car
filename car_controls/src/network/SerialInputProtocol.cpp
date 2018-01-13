#include "SerialInputProtocol.hpp"

SerialInputProtocol SerialInputProtocol::read(uint8_t* buffer) {
	SerialInputProtocol result;
	
	uint8_t options = buffer[0];
	result.side = (options & SIDE_MASK) == SIDE_MASK ? RIGHT : LEFT;
	result.direction = (options & DIRECTION_MASK) == DIRECTION_MASK ? FORWARD : BACKWARD ;
	result.debugLevel = DEBUG_MASK & options;

	result.value_steer = *((float*) buffer+1);
	result.value_speed = - *((float*) buffer+5);
		 
	return result;
}
