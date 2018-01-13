#include "Controller.hpp"

#include <cmath>

const int Controller::DRIVE_BUFFER_SIZE;
const int Controller::NUM_SKIP_FRAMES = 10;

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
	if (drive_buffer.size == 0) {
		return meters_per_second();
	}

	// calculate a value representing the last drives
	float drive_representation = drive_buffer[0];
	for (unsigned int i = 0; i < drive_buffer.size(); i++) {
		drive_representation = (drive_representation + drive_buffer[i]) / 2.f;
	}

	const float approx_speed = drive_to_speed(drive_representation);
	const float measured_speed = meters_per_second();
	return LEVEL_OF_APPROXIMATION * approx_speed + // approx
		(1.f - LEVEL_OF_APPROXIMATION) * measured_speed; // measured
}

float Controller::calculate_steer(float value_steer, Side side)
{
	if (value_steer > 0.4){
		value_steer=0.4;
	}
	if (side == LEFT){
		return 0.4 - (value_steer/10);
	} else {
		return 0.4 + (value_steer/10);
	}
}

const float ACCELERATION = 0.00035f;
const float MAX_NULL_DRIVE = 0.55f; // The maximal value for which the car would stop after a time

float Controller::speed_to_drive(float target)
{
	if (target == 0.f)
		return 0.5f;
	return ACCELERATION * target * target + MAX_NULL_DRIVE;
}

float Controller::calculate_drive(float current_speed, float target_speed)
{
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
		drive_buffer << drive;
	}
}
