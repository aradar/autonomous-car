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

float Controller::meters_per_second_approx() const
{
	// calculate the average of the last drive-values
	float avg_drive = 0.f;
	for (unsigned int i = 0; i < drive_buffer.size(); i++) {
		avg_drive += drive_buffer[i];
	}

	avg_drive = avg_drive / drive_buffer.size();

	const float target_speed = drive_to_speed(avg_drive);
	const float approx_speed = (target_speed + meters_per_second()) / 2.f;

	return approx_speed;
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
