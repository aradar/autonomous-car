#include "CarState.hpp"

CarState::CarState()
	: drive_(0.f), steer_(0.f)
{}

void CarState::apply_input_protocol(const SerialInputProtocol& input_protocol)
{
	if (input_protocol.side_) // RIGHT
		steer_ = input_protocol.steer_;
	else // LEFT
		steer_ = -input_protocol.steer_;

	if (input_protocol.direction_) // FORWARD
		drive_ = input_protocol.drive_;
	else
		drive_ = -input_protocol.drive_;
}
