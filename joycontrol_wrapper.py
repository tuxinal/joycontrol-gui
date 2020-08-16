import argparse
import asyncio
import logging
import os

from aioconsole import ainput

from joycontrol import logging_default as log, utils
from joycontrol.command_line_interface import ControllerCLI
from joycontrol.controller import Controller
from joycontrol.controller_state import ControllerState, button_push, ButtonState
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

logger = logging.getLogger(__name__)

class joycontrolWrapper:
    async def init(self,mac):   
        self.spi_flash = FlashMemory()
        self.controller = Controller.PRO_CONTROLLER
        factory = controller_protocol_factory(self.controller, spi_flash=self.spi_flash)
        ctl_psm, itr_psm = 17, 19
        self.transport, self.protocol = await create_hid_server(factory, reconnect_bt_addr=mac,
                                                     ctl_psm=ctl_psm,
                                                     itr_psm=itr_psm,
                                                     )
        self.controller_state = self.protocol.get_controller_state()
        print("connected to switch initializing controller data")
        await self.controller_state.connect()
        self.connected = True
        print("ready to use!")
        await button_push(self.controller_state, 'up')
        await button_push(self.controller_state, 'down')
    async def pushButton(self,button):
        button_state = self.controller_state.button_state
        button_state.set_button(button)
        await self.controller_state.send()
    async def releaseButton(self,button):
        button_state = self.controller_state.button_state
        button_state.set_button(button ,pushed=False)
        await self.controller_state.send()
    async def moveLsitckH(self,value):
        lstick = self.controller_state.l_stick_state
        lstick.set_h(value)
        await self.controller_state.send()
    async def moveLsitckV(self,value):
        lstick = self.controller_state.l_stick_state
        lstick.set_v(value)
        await self.controller_state.send()
    async def moveRsitckH(self,value):
        rstick = self.controller_state.r_stick_state
        rstick.set_h(value)
        await self.controller_state.send()
    async def moveRsitckV(self,value):
        rstick = self.controller_state.r_stick_state
        rstick.set_v(value)
        await self.controller_state.send()
    