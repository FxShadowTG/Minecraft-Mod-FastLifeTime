# -*- coding: utf-8 -*-

from mod.common.mod import Mod


@Mod.Binding(name="Script_NeteaseModfoPxb4xR", version="0.0.1")
class Script_NeteaseModfoPxb4xR(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def Script_NeteaseModfoPxb4xRServerInit(self):
        pass

    @Mod.DestroyServer()
    def Script_NeteaseModfoPxb4xRServerDestroy(self):
        pass

    @Mod.InitClient()
    def Script_NeteaseModfoPxb4xRClientInit(self):
        pass

    @Mod.DestroyClient()
    def Script_NeteaseModfoPxb4xRClientDestroy(self):
        pass
