#include "LEDHandler.hpp"

DigitalOut LEDHandler::status_led(LED1);
int LEDHandler::blink_counter = 0;

void LEDHandler::blink_blocking(float time)
{
	status_led = 1;
	wait(time);
	status_led = 0;
}

void LEDHandler::blink_blocking(float time, unsigned int count)
{
	for (unsigned int i = 0; i < count; i++) {
		blink_blocking(time);
		wait(time);
	}
}

void LEDHandler::blink_async(int ticks)
{
	status_led = 1;
	blink_counter = ticks;
}

void LEDHandler::update()
{
	if (blink_counter > 0) {
		blink_counter--;

		if (blink_counter == 0) {
			status_led = 0;
		}
	}
}

void LEDHandler::on()
{
	status_led = 1;
}

void LEDHandler::off()
{
	status_led = 0;
}

void LEDHandler::toggle()
{
	status_led = !status_led;
}

LEDHandler::LEDHandler() {}
