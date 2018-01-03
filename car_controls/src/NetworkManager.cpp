#include "NetworkManager.hpp"

#include "mbed.h"

namespace nm {
	Serial pi(PB_6, PB_7, 9600); //UART1_TX / D4, UART1_RX / D5

	int received_bytes_counter_ = 0; // counter for incoming bytes. Used as index for tmp_buffer
	const int BUFFER_SIZE = 9;
	uint8_t tmp_buffer[BUFFER_SIZE];
	uint8_t valid_buffer[BUFFER_SIZE];

	bool has_update_ = false;

	void rx_interrupt() {
		while (pi.readable())
		{
			tmp_buffer[received_bytes_counter_] = pi.getc();
			
			// increase counter and restart, if buffer is full
			received_bytes_counter_++;
			received_bytes_counter_ = received_bytes_counter_ % BUFFER_SIZE;

			/*
			 * If a new packet is received the old packet will be discarded!
			 */
			if (received_bytes_counter_ == 0) // is tmp_buffer full?
			{
				// fill all bytes in valid_buffer
				for (int i = 0; i < BUFFER_SIZE; i++) {
					SerialInputProtocol prot = SerialInputProtocol::read(tmp_buffer);
					valid_buffer[i] = tmp_buffer[i];
				}
				
				has_update_ = true;
			}
		}
	}

	bool has_update()
	{
		return has_update_;
	}

	SerialInputProtocol get_update()
	{
		has_update_ = false;
		return SerialInputProtocol::read(valid_buffer);
	}

}

