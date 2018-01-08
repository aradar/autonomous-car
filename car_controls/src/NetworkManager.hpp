#ifndef __NETWORKMANAGER_CLASS__
#define __NETWORKMANAGER_CLASS__

#include "SerialInputProtocol.hpp"

/*
 * If a new packet is received the old packet will be discarded!
 */

namespace nm
{
	static Serial pi(PB_6, PB_7, 9600); //UART1_TX / D4, UART1_RX / D5
	static bool received_something = false;
	void rx_interrupt();
	bool has_update();
	SerialInputProtocol get_update();
}

#endif
