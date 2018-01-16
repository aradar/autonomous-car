#include "NetworkManager.hpp"

#include "SerialInputProtocol.hpp"
#include "../misc/CarState.hpp"

Serial NetworkManager::pi(PB_6, PB_7, 9600); //UART1_TX / D4, UART1_RX / D5

float NetworkManager::test_value1 = 0.f;
float NetworkManager::test_value2 = 0.f;

bool NetworkManager::restart_bit_received = false;

NetworkManager::NetworkManager()
{}

// private stuff
int const BUFFER_SIZE = 9;
uint8_t rx_buffer[BUFFER_SIZE];

CarState car_state_tmp;

void serialReadCallback(uint8_t* fixed_buffer) {
	SerialInputProtocol input = SerialInputProtocol::read(fixed_buffer);
	input.update_car_state(&car_state_tmp);
	if (input.restart_bit) {
		NetworkManager::restart_bit_received = true;
	}
}

int rx_buffer_index = 0;

void rx_interrupt() {
	rx_buffer[rx_buffer_index] = NetworkManager::pi.getc();
	
	rx_buffer_index = (rx_buffer_index + 1) % BUFFER_SIZE;
	if (rx_buffer_index == 0) {
		
		// echo
		for (int i = 0; i < BUFFER_SIZE; ++i) {
			NetworkManager::pi.putc(rx_buffer[i]);
		}

		serialReadCallback(rx_buffer);
	}
}

// public stuff ############

void NetworkManager::init(const CarState& original)
{
	car_state_tmp.update_from(original);
	NetworkManager::pi.attach(&rx_interrupt);
}

void NetworkManager::send(float f)
{
	uint8_t* p = (uint8_t*)&f;
	for (unsigned int i = 0; i < sizeof(float); i++) {
		NetworkManager::pi.putc(*p);
		p++;
	}
	//NetworkManager::pi.printf("%f", f);
}

void NetworkManager::send(int i)
{
	NetworkManager::pi.printf("%d", i);
}

void NetworkManager::send(const std::string& s)
{
	NetworkManager::pi.printf(s.c_str());
}

void NetworkManager::update_car_state(CarState* car_state_arg)
{
	car_state_arg->update_from(car_state_tmp);
}
