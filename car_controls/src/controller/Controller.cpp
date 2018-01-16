#include "Controller.hpp"

#include <cmath>

const int Controller::DRIVE_BUFFER_SIZE;
const int Controller::NUM_SKIP_FRAMES = 100;

const float Controller::MAX_STEER_VALUE = 0.7f;
const float Controller::MIN_STEER_VALUE = 1-Controller::MAX_STEER_VALUE;

const float Controller::MAX_SPEED_LIMIT = 2.f;

void Controller::update(float drive)
{
	update_drive_values(drive);
}

float Controller::meters_per_second() const
{
	return rev_counter.meters_per_second();
}

const float LEVEL_OF_APPROXIMATION = 0.7f; // should be between 0.f and 1.f

float Controller::meters_per_second_approx() const
{
	if (drive_buffer.size() == 0) {
		return meters_per_second();
	}

	// calculate a value representing the last drives
	float drive_representation = drive_buffer[0];
	for (std::deque<int>::const_iterator iter = drive_buffer.begin(); iter != drive_buffer.end(); ++iter) {
		drive_representation = (drive_representation + *iter) / 2.f;
	}

	const float approx_speed = drive_to_speed(drive_representation);
	const float measured_speed = meters_per_second();
	return LEVEL_OF_APPROXIMATION * approx_speed + // approx
		(1.f - LEVEL_OF_APPROXIMATION) * measured_speed; // measured
}

float Controller::calculate_steer(float steer_Degree, Side side){
	float steer_value;
	if (side == LEFT){
		steer_value = 0.5 + steer_Degree * 0.0075 ;
	}else{
		steer_value = 0.5 - steer_Degree * 0.0075;
	}
	if (steer_value > MAX_STEER_VALUE)
		steer_value = MAX_STEER_VALUE;
	if (steer_value < MIN_STEER_VALUE)
		steer_value = MIN_STEER_VALUE;
	return steer_value;
}

const float ACCELERATION = 0.00035f;
const float MAX_NULL_DRIVE = 0.57f; // The maximal value for which the car would stop after a time

float Controller::speed_to_drive(float target)
{
	if (target == 0.f)
		return 0.5f;
	return ACCELERATION * target * target + MAX_NULL_DRIVE;
}

float Controller::calculate_drive(float current_speed, float target_speed)
{
	if (target_speed > MAX_SPEED_LIMIT) {
		target_speed = MAX_SPEED_LIMIT;
	}
	float acceleration = 0.05;
	return acceleration * (target_speed - current_speed) + speed_to_drive(target_speed);
}

float Controller::drive_to_speed(float drive)
{
	float t = drive - MAX_NULL_DRIVE;
	if (t <= 0.f)
		return 0.f;
	return std::sqrt(t / ACCELERATION);
}

void Controller::update_drive_values(float drive) {
	skip_frames_counter = (skip_frames_counter + 1) % NUM_SKIP_FRAMES;
	if (skip_frames_counter == 0) {
		drive_buffer.push_front(drive);
		// limit to DRIVE_BUFFER_SIZE drive values
		if (drive_buffer.size() > DRIVE_BUFFER_SIZE) {
			drive_buffer.pop_back();
		}
	}
}
