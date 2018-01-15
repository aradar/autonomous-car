#ifndef __NETWORKMANAGER_CLASS__
#define __NETWORKMANAGER_CLASS__

#include <string>
#include "mbed.h"

class CarState;

class NetworkManager
{
	public:
		NetworkManager();

		void init(const CarState& original);

		void send(float f);
		void send(int i);
		void send(const std::string& s);

		void update_car_state(CarState* car_state);

		static Serial pi;
};

#endif
