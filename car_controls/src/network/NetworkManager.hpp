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
};

#endif
