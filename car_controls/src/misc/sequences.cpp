#include "sequences.hpp"

#include "RevCounter.hpp"
#include "NetworkManager.hpp"

#include "LEDHandler.hpp"

namespace sequences {
	const float CALIBRATION_TIME = 2.f;

	// send calibration signals
	void calibrate() {
		// blink initial
		LEDHandler::blink_blocking(0.4f, 3);

		wait(CALIBRATION_TIME);

		// blink end
		LEDHandler::blink_blocking(0.2f, 3);
	}

	void test_steer(Servo& steer) {
		const float MIN_STEER_VALUE = 0.3f;
		const float MAX_STEER_VALUE = 0.7f;
		const float STEER_SPEED = 0.005f;

		// go left
		for (float f = 0.5f; f < MAX_STEER_VALUE; f += STEER_SPEED)
		{
			steer = f;
			wait_ms(15);
		}
		// go right
		for (float f = MAX_STEER_VALUE; f > MIN_STEER_VALUE; f -= STEER_SPEED)
		{
			steer = f;
			wait_ms(15);
		}
		// go mid
		for (float f = MIN_STEER_VALUE; f < 0.5f; f += STEER_SPEED)
		{
			steer = f;
			wait_ms(15);
		}
		steer = 0.5f;
	}

	void test_drive(Servo& drive)
	{
		// vorwaerts 
		drive = 0.65f;

		RevCounter revCounter;
		LEDHandler::blink_blocking(1.f);

		drive = 0.57f;

		wait(1);

		for (int cycle = 0; cycle < 6; cycle++)
		{
			wait(1.0);
			// networking::send(revCounter.meters_per_second());
		}

		drive = 0.5f;

		wait(1);

		// end
		LEDHandler::blink_blocking(0.2f, 3);
	}
}
