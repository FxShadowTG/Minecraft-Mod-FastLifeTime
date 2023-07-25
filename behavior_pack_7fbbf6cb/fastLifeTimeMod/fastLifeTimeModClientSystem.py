# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi
ClientSystem = clientApi.GetClientSystemCls()
Factory = clientApi.GetEngineCompFactory()

class fastLifeTimeModClientSystem(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.ListenEvent()
        print("Client ok")

    def ListenEvent(self):
        self.levelId = self.GetLevelId()
        self.localId = clientApi.GetLocalPlayerId()
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), 'ClientJumpButtonPressDownEvent', self, self.OnClientJumpButtonPressDownEvent)
        #self.ListenForEvent("fastLifeTimeMod", "fastLifeTimeModServerSystem", 'testEvent', self, self.OntestEvent)
        self.ListenForEvent("fastLifeTimeMod", "fastLifeTimeModServerSystem", 'checkAgeEvent', self, self.OncheckAgeEvent)
        print("ListenEvent ok")
    
    def OncheckAgeEvent(self, args):
        print("客户端年龄：")
        print(args)
        # compByCreatePostProcess = Factory.CreatePostProcess(self.levelId)
        # #老人(85-100)儿童(0-5)视力模糊
        # if args["playerId"] in (0,1,2,3,4,5,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100):
        #     compByCreatePostProcess.SetEnableDepthOfField(True)
        # else:
        #     compByCreatePostProcess.SetEnableDepthOfField(False)
        

    def OntestEvent(self,args):
        print("客户端收到：")
        print(args)

    def OnClientJumpButtonPressDownEvent(self,args):
        print("down!")
        print(self.localId)
        self.NotifyToServer("jumpEvent",args)

    def OnScriptTickServer(self, args):
        print("客户端监听：")
        print(args)

    # 监听引擎OnScriptTickClient事件，引擎会执行该tick回调，1秒钟30帧
    def OnTickClient(self):
        """
        Driven by event, One tick way
        """
        pass

    # 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):

        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), 'ClientJumpButtonPressDownEvent', self, self.OnClientJumpButtonPressDownEvent)
        self.UnListenForEvent("fastLifeTimeMod", "fastLifeTimeModServerSystem", 'testEvent', self, self.OntestEvent)
        self.UnListenForEvent("fastLifeTimeMod", "fastLifeTimeModServerSystem", 'checkAgeEvent', self, self.OncheckAgeEvent)