#ifndef __SERIALINPUTPROTOCOL_CLASS__
#define __SERIALINPUTPROTOCOL_CLASS__

//typedef char uint8_t;
#include <mbed.h>

struct SerialInputProtocol {
	enum Side { LEFT, RIGHT };
	enum Direction { FORWARD, BACKWARD };

	Side side_;
	Direction direction_;

	char debug_level_;
	float steer_;
	float drive_;

	static SerialInputProtocol read(uint8_t* buffer);
};

#endif
