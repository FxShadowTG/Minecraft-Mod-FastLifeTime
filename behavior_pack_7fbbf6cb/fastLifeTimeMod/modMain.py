# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.server.extraServerApi as serverApi
import mod.client.extraClientApi as clientApi


@Mod.Binding(name="fastLifeTimeMod", version="0.0.1")
class fastLifeTimeMod(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def fastLifeTimeModServerInit(self):
        serverApi.RegisterSystem("fastLifeTimeMod","fastLifeTimeModServerSystem","fastLifeTimeMod.fastLifeTimeModServerSystem.fastLifeTimeModServerSystem")
        print("===服务端注册完毕===")

    @Mod.DestroyServer()
    def fastLifeTimeModServerDestroy(self):
        print("===服务端销毁完毕===")

    @Mod.InitClient()
    def fastLifeTimeModClientInit(self):
        clientApi.RegisterSystem("fastLifeTimeMod","fastLifeTimeModClientSystem","fastLifeTimeMod.fastLifeTimeModClientSystem.fastLifeTimeModClientSystem")
        print("===客户端注册完毕===")


    @Mod.DestroyClient()
    def fastLifeTimeModClientDestroy(self):
        print("===客户端销毁完毕===")
