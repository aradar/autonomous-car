#ifndef __SERIALINPUTPROTOCOL_CLASS__
#define __SERIALINPUTPROTOCOL_CLASS__

#include "mbed.h"
#include "../misc/directions.hpp"

uint8_t const SIDE_MASK = 0x80;
uint8_t const DIRECTION_MASK = 0x40;
uint8_t const DEBUG_MASK = (uint8_t)~(SIDE_MASK | DIRECTION_MASK);

struct SerialInputProtocol
{
		Side side;
		Direction direction;

		char debugLevel;
		float value_steer;
		float value_speed;

		static SerialInputProtocol read(uint8_t* buffer);
};

#endif
