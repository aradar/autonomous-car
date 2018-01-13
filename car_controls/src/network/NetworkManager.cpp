#include "NetworkManager.hpp"

#include "SerialInputProtocol.hpp"
#include "CarState.hpp"

Serial NetworkManager::pi(PB_6, PB_7, 9600); //UART1_TX / D4, UART1_RX / D5

NetworkManager::NetworkManager()
{}

// private stuff
int const BUFFER_SIZE = 9;
uint8_t rx_buffer[BUFFER_SIZE];

CarState car_state_tmp;

void serialReadCallback() {
	SerialInputProtocol input = SerialInputProtocol::read(rx_buffer);

	car_state_tmp.target_speed = input.value_speed;
	car_state_tmp.steer = input.value_steer;
	car_state_tmp.steer_changed = true;
}

int rx_buffer_size = 0;

void rx_interrupt() {
	rx_buffer[rx_buffer_size] = NetworkManager::pi.getc();
	
	rx_buffer_size++;
	rx_buffer_size = rx_buffer_size % BUFFER_SIZE;
	if (rx_buffer_size == 0) {
		
		// echo
		for (int i = 0; i < BUFFER_SIZE; ++i) {
			NetworkManager::pi.putc(rx_buffer[i]);
		}
		NetworkManager::pi.putc('\n');
		
		serialReadCallback();
	}
}


// public stuff ############

void NetworkManager::init()
{
	NetworkManager::pi.attach(&rx_interrupt);
}

void NetworkManager::send(float f)
{
	NetworkManager::pi.printf("%f", f);
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
