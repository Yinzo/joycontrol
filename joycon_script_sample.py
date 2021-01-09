#! -*- coding: utf8 -*-
import os
import asyncio

from joycontrol.controller import Controller
from joycontrol.controller_state import ControllerState, button_push, button_press, button_release
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server



async def _main():
    controller = Controller.from_arg("PRO_CONTROLLER")
    factory = controller_protocol_factory(controller, spi_flash=FlashMemory())
    print("waiting for 'Change Grip/Order' menu of the Switch.")
    transport, protocol = await create_hid_server(factory, ctl_psm=17, itr_psm=19)
    controller_state = protocol.get_controller_state()
    
    await controller_state.connect()
    print("controller connected.")

    await button_push(controller_state, "home", sec=0.1)
    await asyncio.sleep(1)
    await button_push(controller_state, "right", sec=0.1)
    await button_push(controller_state, "right", sec=0.1)
    await button_push(controller_state, "left", sec=0.1)

    await button_push(controller_state, "right", sec=0.1)
    await button_push(controller_state, "right", sec=0.1)
    await button_push(controller_state, "left", sec=0.1)
    
    await button_push(controller_state, "right", sec=0.1)
    await button_push(controller_state, "right", sec=0.1)
    await button_push(controller_state, "left", sec=0.1)

    controller_state.r_stick_state.set_right()
    await asyncio.sleep(60)

if __name__ == "__main__":
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')
    asyncio.run(_main())
