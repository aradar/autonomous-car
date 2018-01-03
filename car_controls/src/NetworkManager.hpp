#ifndef __NETWORKMANAGER_CLASS__
#define __NETWORKMANAGER_CLASS__

#include "SerialInputProtocol.hpp"

/*
 * If a new packet is received the old packet will be discarded!
 */

namespace nm
{
	bool has_update();
	SerialInputProtocol get_update();
}

#endif
