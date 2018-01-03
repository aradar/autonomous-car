#ifndef __CARSTATE_CLASS__
#define __CARSTATE_CLASS__

#include "SerialInputProtocol.hpp"

class CarState {
	public:
		CarState();
		void apply_input_protocol(const SerialInputProtocol& input_protocol);
	private:
		float drive_;
		float steer_;
};

#endif
