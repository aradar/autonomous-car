#ifndef __CONTROLLER_CLASS__
#define __CONTROLLER_CLASS__

#include "directions.hpp"
#include "RevCounter.hpp"

/*
 * The Controller has the following functions:
 *  - measures current speed (2 versions: plain and approx)
 *  - calculates the drive adapted to the current speed and the target speed
 *  - calculates the steer value adapted to the target steer
 *  - converts drive to speed values
 *  - converts speed to drive values
 *
 *  Maybe split speed measurement and drive/steer calculations
 */

class Controller
{
	public:
		static const int DRIVE_BUFFER_SIZE = 100;
		static const int NUM_SKIP_FRAMES;

		void update(float drive);

		float meters_per_second() const;
		float meters_per_second_approx() const;
		float calculate_drive(float current_speed, float target_speed);
		float calculate_steer(float valueSteer, Side side);
		static float speed_to_drive(float target);
		static float drive_to_speed(float drive);

		void update_drive_values(float drive);
	private:
		int skip_frames_counter;
		RingBuffer<int, DRIVE_BUFFER_SIZE> drive_buffer;
		RevCounter rev_counter;
};

#endif
