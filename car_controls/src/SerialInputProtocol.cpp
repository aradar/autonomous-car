#include "SerialInputProtocol.hpp"

uint8_t const SIDE_MASK = 0x80;
uint8_t const DIRECTION_MASK = 0x40;
uint8_t const DEBUG_MASK = ~ (SIDE_MASK | DIRECTION_MASK);

SerialInputProtocol SerialInputProtocol::read(uint8_t* buffer) {
	SerialInputProtocol result;

	uint8_t options = buffer[0];

	result.side_ = (options & SIDE_MASK) == SIDE_MASK ? LEFT : RIGHT;
	result.direction_ = (options & DIRECTION_MASK) == DIRECTION_MASK ? BACKWARD : FORWARD;
	result.debug_level_ = DEBUG_MASK & options;

	// interpret the four bytes 1-5 as int*
	result.steer_ = *((int*) (buffer + 1));
	result.drive_ = *((int*) (buffer + 5));
		 
	return result;
}
