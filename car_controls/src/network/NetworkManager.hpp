#ifndef __NETWORKMANAGER_CLASS__
#define __NETWORKMANAGER_CLASS__

#include <string>
#include "mbed.h"

class CarState;

class NetworkManager
{
	public:
		NetworkManager();

		static void init(const CarState& original);

		static void send(float f);
		static void send(int i);
		static void send(const std::string& s);

		static void update_car_state(CarState* car_state);

		static Serial pi;

		static float test_value1;
		static float test_value2;

		static bool restart_bit_received;
};

#endif
