# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi
ServerSystem = serverApi.GetServerSystemCls()
Factory = serverApi.GetEngineCompFactory()


class fastLifeTimeModServerSystem(ServerSystem):
    def __init__(self, namespace, systemName):
        print("加载监听ing")
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenEvent()
        #玩家岁数等级词典
        self.playerAgeDict = {}
        #玩家时代等级词典
        self.playerEraDict = {}
        #玩家年龄增长值（所有玩家共享）（每1秒增加30数值，30秒后就到900数值，到900数值就升一年龄）
        self.playerAgeValue = 0
        #定义天数
        self.age = 0
        #新进游戏不影响天数
        self.ageFlag = False
        #是否开启检测死亡
        self.checkDie = True
        print("加载监听ok")

    def ListenEvent(self):
        #获取levelId
        self.levelId = serverApi.GetLevelId()
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'OnScriptTickServer', self, self.OnScriptTickServer)
        #self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerTrySleepServerEvent', self, self.OnPlayerTrySleepServerEvent)
        self.ListenForEvent("fastLifeTimeMod", "fastLifeTimeModClientSystem", 'jumpEvent', self, self.OnJumpEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerDieEvent', self, self.OnPlayerDieEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerEatFoodServerEvent', self, self.OnPlayerEatFoodServerEvent)
        print("ListenEvent,OK")

    #传递年龄给客户端
    def checkAgeEvent(self,playerId):
        # 向客户端发送事件
        self.NotifyToClient(playerId,'checkAgeEvent', self.playerAgeDict)
    

    #检测跳跃
    def OnJumpEvent(self, args):
        #拿到跳跃玩家的id
        playerId = args['__id__']
        print("take playerid")

        print("add time")
        #时间加快
        if self.playerAgeDict[playerId] in (0,1,2,3,4,5):
            compByCreateCommand = Factory.CreateCommand(self.levelId)
            compByCreateCommand.SetCommand("/time add 500")

    #玩家吃下特定的物品时触发
    def OnPlayerEatFoodServerEvent(self, args):
        playerId = args["playerId"]
        itemDict = args["itemDict"]
        if (itemDict["itemName"] == "kuljz:oldertochildrendrug") and self.playerAgeDict[playerId] >= 18:
            self.playerAgeDict[playerId] = 18
            #通知全部人
            compByCreateName = Factory.CreateName(playerId)
            playerName = compByCreateName.GetName()
            compByCreateGame = Factory.CreateGame(self.levelId)
            if self.playerEraDict[playerId] > 0:
                compByCreateGame.SetNotifyMsg("§l§b" + playerName + str(self.playerEraDict[playerId]) + "世 使用返老还童药剂年轻到了 18 岁", serverApi.GenerateColor('RED'))
            else:
                compByCreateGame.SetNotifyMsg("§l§b" + playerName + " 使用返老还童药剂年轻到了 18 岁", serverApi.GenerateColor('RED'))

        elif (itemDict["itemName"] == "kuljz:childrentoolderdrug") and self.playerAgeDict[playerId] <= 70:
            self.playerAgeDict[playerId] = 70
            #通知全部人
            compByCreateName = Factory.CreateName(playerId)
            playerName = compByCreateName.GetName()
            compByCreateGame = Factory.CreateGame(self.levelId)
            #大小
            compByCreateScale = Factory.CreateScale(playerId)
            compByCreateScale.SetEntityScale(playerId, 1)
            if self.playerEraDict[playerId] > 0:
                compByCreateGame.SetNotifyMsg("§l§d" + playerName + str(self.playerEraDict[playerId]) + "世 使用未老先衰药剂衰老到了 70 岁", serverApi.GenerateColor('RED'))
            else:
                compByCreateGame.SetNotifyMsg("§l§d" + playerName + " 使用未老先衰药剂衰老到了 70 岁", serverApi.GenerateColor('RED'))
        
        elif (itemDict["itemName"] == "kuljz:middrug"):
            self.playerAgeDict[playerId] = 45
            #通知全部人
            compByCreateName = Factory.CreateName(playerId)
            playerName = compByCreateName.GetName()
            compByCreateGame = Factory.CreateGame(self.levelId)
            #大小
            compByCreateScale = Factory.CreateScale(playerId)
            compByCreateScale.SetEntityScale(playerId, 1)
            if self.playerEraDict[playerId] > 0:
                compByCreateGame.SetNotifyMsg("§l§e" + playerName + str(self.playerEraDict[playerId]) + "世 使用不惑之年药剂到了 45 岁", serverApi.GenerateColor('RED'))
            else:
                compByCreateGame.SetNotifyMsg("§l§e" + playerName + " 使用不惑之年药剂到了 45 岁", serverApi.GenerateColor('RED'))

        elif (itemDict["itemName"] == "kuljz:hourglass"):
            CreatePlayer = Factory.CreatePlayer(playerId)
            resultDict = CreatePlayer.GetPlayerRespawnPos()

            postX = resultDict["pos"][0]
            postY = resultDict["pos"][1]
            postZ = resultDict["pos"][2]

            #传送玩家
            #如果它没设置过重生点，那么就会是32767
            if postY == 32767:
                compByCreateDimension = Factory.CreateDimension(playerId)
                compByCreateDimension.ChangePlayerDimension(0, (postX,256,postZ))
            else:
                compByCreateDimension = Factory.CreateDimension(playerId)
                compByCreateDimension.ChangePlayerDimension(0, (postX,postY,postZ))

            #通知全部人
            compByCreateName = Factory.CreateName(playerId)
            playerName = compByCreateName.GetName()
            compByCreateGame = Factory.CreateGame(self.levelId)
            if self.playerEraDict[playerId] > 0:
                compByCreateGame.SetNotifyMsg("§l§d" + playerName + str(self.playerEraDict[playerId]) + "世 使用了时间沙漏回到了复活点", serverApi.GenerateColor('RED'))
            else:
                compByCreateGame.SetNotifyMsg("§l§d" + playerName + " 使用了时间沙漏回到了复活点", serverApi.GenerateColor('RED'))


    #玩家死亡时换代
    def OnPlayerDieEvent(self,args):
        if self.checkDie == False:
            return

        playerId = args['id']
        #个人世代+1
        self.AddPlayerEra(playerId,1)
        #重置年龄
        self.playerAgeDict[playerId] = 0

        compByCreateName = Factory.CreateName(playerId)
        playerName = compByCreateName.GetName()

        #非自然死亡只有骷髅头
        skullItemDict = {
            'itemName': 'minecraft:skull',
            'count': 1,
            'enchantData': [(serverApi.GetMinecraftEnum().EnchantType.BowDamage, 1),],
            'auxValue': 0,
            'customTips':'§c' + playerName + str(self.playerEraDict[playerId] - 1) + "世" '的非自然头颅',
        }
        compByCreateItem = Factory.CreateItem(playerId)
        compByCreateItem.SpawnItemToPlayerInv(skullItemDict, playerId)

        #通知全部人
        compByCreateGame = Factory.CreateGame(self.levelId)
        compByCreateGame.SetNotifyMsg("§l" + playerName + str(self.playerEraDict[playerId]) + "世 破壳了", serverApi.GenerateColor('BLUE'))
        self.checkAge()
        #发送消息
        self.sendMessageToPlayer()

    # #测试专用
    # def OnPlayerTrySleepServerEvent(self,args):
    #     playerId = args['playerId']
    #     self.playerAgeDict[playerId] += 1

    #     print("已广播给客户端")
    #     self.NotifyToClient(playerId,"testEvent", args)

    #     self.checkAge()
    #     self.sendMessageToPlayer()

    #玩家加入时
    def OnAddServerPlayerEvent(self,args):
        playerId = args['id']
        #把playerId添加进岁数等级里
        self.playerAgeDict[playerId] = 0
        #把playerId添加进增长值内
        self.playerAgeValue = 0
        #把playerId添加进时代列表里
        self.playerEraDict[playerId] = 1

        #读取持久化年龄，如果有额外数据的话下面才会生效，否则依然是0
        compByCreateExtraData = Factory.CreateExtraData(playerId)
        age = compByCreateExtraData.GetExtraData("age")
        if age == None:
            self.playerAgeDict[playerId] = 0
        else:
            self.playerAgeDict[playerId] = age
        print("持久化后年龄数(age)：")
        print(self.playerAgeDict[playerId])

        #读取持久化年世代，如果有额外数据的话下面才会生效，否则依然是0
        era = compByCreateExtraData.GetExtraData("era")
        if era == None:
            self.playerEraDict[playerId] = 1
        else:
            self.playerEraDict[playerId] = era
        print("持久化后世代数(era)：")
        print(self.playerEraDict[playerId])

    #所有人添加年龄
    def AddPlayerAge(self,ageCount):
        for player in self.playerAgeDict:
            self.playerAgeDict[player] += ageCount
            #保存数据
            entitycompByCreateExtraData = Factory.CreateExtraData(player)
            entitycompByCreateExtraData.SetExtraData("age", self.playerAgeDict[player])
            result = entitycompByCreateExtraData.SaveExtraData()
            print("保存年龄结果：")
            print(result)

    #添加个人世代
    def AddPlayerEra(self,playerId,eraCount):
        self.playerEraDict[playerId] += eraCount
        #保存数据
        entitycompByCreateExtraData = Factory.CreateExtraData(playerId)
        entitycompByCreateExtraData.SetExtraData("era", self.playerEraDict[playerId])
        result = entitycompByCreateExtraData.SaveExtraData()
        print("保存世代结果：")
        print(result)

    def sendMessageToPlayer(self):
        for playerId in self.playerAgeDict:
            age = self.playerAgeDict[playerId]
            compByCreateGame = Factory.CreateGame(self.levelId)
            compByCreateMsg = Factory.CreateMsg(playerId)
            compByCreateName = Factory.CreateName(playerId)
            playerName = compByCreateName.GetName()

            if age >= 101:
                return

            compByCreateGame.SetOneTipMessage(playerId, serverApi.GenerateColor("RED") + "§7你 " + str(age) + " 岁了")

            if age in (0,1):
                compByCreateMsg.NotifyOneMessage(playerId, "5 岁前每次跳跃会加快时间的流逝", "§7")
            if age == 3:
                compByCreateMsg.NotifyOneMessage(playerId, "呜呜", "§f")
            if age == 10:
                compByCreateMsg.NotifyOneMessage(playerId, "今天出去春游了，我非常开心", "§b")
            if age == 16:
                compByCreateMsg.NotifyOneMessage(playerId, "我上了重点高中", "§a")   
                compByCreateMsg.NotifyOneMessage(playerId, "我喜欢呆在图书馆里学习", "§a") 
            if age == 30:      
                compByCreateMsg.NotifyOneMessage(playerId, "我创办了一家新能源公司，名字叫源神科技", "§6")
            if age == 31:      
                compByCreateMsg.NotifyOneMessage(playerId, "今年公司的营收很不错，达到了300W", "§6") 
                compByCreateMsg.NotifyOneMessage(playerId, "我买了房子和车子", "§6")
            if age == 44:      
                compByCreateMsg.NotifyOneMessage(playerId, "十几年过去了，公司营收入达到了之前的十倍", "§c") 
                compByCreateMsg.NotifyOneMessage(playerId, "我非常兴奋", "§c")     
            if age == 47:  
                compByCreateMsg.NotifyOneMessage(playerId, "公司进500强了，我承担的责任也更大了", "§c") 
            if age == 50:  
                compByCreateMsg.NotifyOneMessage(playerId, "终于！我实现了真正意义上的财富自由", "§c") 
            if age == 51:  
                compByCreateMsg.NotifyOneMessage(playerId, "家里出变故了...我的Dad离开了我", "§c") 
            if age == 53:  
                compByCreateMsg.NotifyOneMessage(playerId, "我的Mom也离开了我", "§c") 
            if age == 55:
                compByCreateMsg.NotifyOneMessage(playerId, "我退休了", "§d")
            if age == 60:
                compByCreateMsg.NotifyOneMessage(playerId, "我老了", "§d")
            if age == 80:
                compByCreateMsg.NotifyOneMessage(playerId, "十年过去了，我快到终点了", "§d")
            if age == 85:
                compByCreateMsg.NotifyOneMessage(playerId, "我走不动了...", "§d")
            if age == 90:
                compByCreateMsg.NotifyOneMessage(playerId, "今天快摔倒的时候，还好我的孩子扶了扶我，真是万幸", "§d")
            if age == 91:
                compByCreateMsg.NotifyOneMessage(playerId, "我跳不起来...眼睛突然也看不见了", "§d")
            if age == 95:
                compByCreateMsg.NotifyOneMessage(playerId, "我告诉孩子们，一定要听爸爸的话，努力学习，天天向上，为未来奋斗！", "§f")
            if age == 96:
                compByCreateMsg.NotifyOneMessage(playerId, "我说不了话了", "§f")
            if age == 97:
                compByCreateMsg.NotifyOneMessage(playerId, "我每天晚上睡觉都害怕哪一天我会离开了这个世界", "§f")
            if age == 99:
                compByCreateMsg.NotifyOneMessage(playerId, "我快不行了...", "§f")
            if age == 100:
                compByCreateMsg.NotifyOneMessage(playerId, "我快倒下了，生命的旅程即将结束了。", "§6")
                compByCreateMsg.NotifyOneMessage(playerId, "-------------------------", "§f")
                compByCreateMsg.NotifyOneMessage(playerId, "你的曾孙子即将出生，他们准备取名叫" + playerName + str(self.playerEraDict[playerId] + 1) + "世", "§e")

    def checkAge(self):
        for playerId in self.playerAgeDict:
            age = self.playerAgeDict[playerId]
            compByCreateEffect = Factory.CreateEffect(playerId)
            compByCreateCommand = Factory.CreateCommand(self.levelId)
            compByCreateName = Factory.CreateName(playerId)
            playerName = compByCreateName.GetName()
            compByCreateScale = Factory.CreateScale(playerId)
            compByCreateAttr = Factory.CreateAttr(playerId)
            #设置岁数
            compByCreateName.SetPlayerPrefixAndSuffixName('§c ' + str(self.playerEraDict[playerId]) + " 世§f",serverApi.GenerateColor('RED'),'§b ' + str(age) + " 岁",serverApi.GenerateColor('RED'))
            if age in (0,1,2):
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 3, False)
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 0, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 3, False)
                #夜视
                compByCreateEffect.AddEffectToEntity("night_vision", 31, 0, False)
                #缓降
                compByCreateEffect.AddEffectToEntity("slow_falling", 31, 0, False)
                #播放粒子
                compByCreateCommand.SetCommand("execute " + playerName + " ~~~ " + "particle " +  "minecraft:water_splash_particle" + "^^^-0.5")
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.3)
                #恢复玩家跳跃
                compByCreatePlayer = Factory.CreatePlayer(playerId)
                compByCreatePlayer.SetPlayerJumpable(True)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 10)
            elif age in (3,4,5):
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 0, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 1, False)
                #夜视
                compByCreateEffect.AddEffectToEntity("night_vision", 31, 0, False)
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.4)
                #再次恢复玩家跳跃(防止bug)
                compByCreatePlayer = Factory.CreatePlayer(playerId)
                compByCreatePlayer.SetPlayerJumpable(True)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 12)
            elif age in (6,7,8,9,10,11,12):
                #跳跃
                compByCreateEffect.AddEffectToEntity("jump_boost", 31, 0, False)
                #速度
                compByCreateEffect.AddEffectToEntity("speed", 31, 0, False)
                #饥饿
                compByCreateEffect.AddEffectToEntity("hunger", 31, 0, False)
                #播放粒子
                compByCreateCommand.SetCommand("execute " + playerName + " ~~~ " + "particle " +  "minecraft:water_splash_particle" + "^^^-0.5")
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.5)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 14)
            elif age in (13,14,15):
                #速度
                compByCreateEffect.AddEffectToEntity("speed", 31, 1, False)
                #跳跃
                compByCreateEffect.AddEffectToEntity("jump_boost", 31, 1, False)
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 1, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 0, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 0, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 0, False)
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.6)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 16)
            elif age in (16,17,18):
                #速度
                compByCreateEffect.AddEffectToEntity("speed", 31, 0, False)
                #跳跃
                compByCreateEffect.AddEffectToEntity("jump_boost", 31, 0, False)
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 2, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 2, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 1, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 1, False)
                #生命提升
                compByCreateEffect.AddEffectToEntity("health_boost", 31, 0, False)
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.7)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 18)
            elif age in (19,20,21,22):
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 3, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 1, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 1, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 2, False)
                #生命提升
                compByCreateEffect.AddEffectToEntity("health_boost", 31, 1, False)
                #抗性提升
                compByCreateEffect.AddEffectToEntity("resistance", 31, 1, False)
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.8)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 20)
            elif age in (23,24,25):
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 2, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 1, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 1, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 2, False)
                #生命提升
                compByCreateEffect.AddEffectToEntity("health_boost", 31, 0, False)
                #抗性提升
                compByCreateEffect.AddEffectToEntity("resistance", 31, 1, False)
                #大小
                compByCreateScale.SetEntityScale(playerId, 0.9)
            elif age in (26,27,28,29,30):
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 1, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 0, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 1, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 2, False)
                #生命提升
                compByCreateEffect.AddEffectToEntity("health_boost", 31, 0, False)
                #抗性提升
                compByCreateEffect.AddEffectToEntity("resistance", 31, 1, False)
                #大小
                compByCreateScale.SetEntityScale(playerId, 1)
            elif age in (31,32,33,34,35,36,37,38,39,40):
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 1, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 0, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 0, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 2, False)
                #抗性提升
                compByCreateEffect.AddEffectToEntity("resistance", 31, 1, False)
            elif age == 41:
                #急迫
                compByCreateEffect.AddEffectToEntity("haste", 31, 1, False)
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 0, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 0, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 2, False)
                #抗性提升
                compByCreateEffect.AddEffectToEntity("resistance", 31, 1, False)
                #村庄英雄
                compByCreateEffect.AddEffectToEntity("village_hero", 31, 0, False)
            elif age in (42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58):
                #水下呼吸
                compByCreateEffect.AddEffectToEntity("water_breathing", 31, 0, False)
                #伤害吸收
                compByCreateEffect.AddEffectToEntity("absorption", 31, 0, False)
                #力量
                compByCreateEffect.AddEffectToEntity("strength", 31, 3, False)
                #抗性提升
                compByCreateEffect.AddEffectToEntity("resistance", 31, 3, False)
            elif age in (59,60,61,62,63,64,65):
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 0, False)
                #饱和
                compByCreateEffect.AddEffectToEntity("saturation", 31, 0, False)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 18)
            elif age in (66,67,68,69,70,71,72,73,74,75):
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 0, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 1, False)
                #饱和
                compByCreateEffect.AddEffectToEntity("saturation", 31, 1, False)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 16)
            elif age in (76,77,78,79,80):
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 0, False)
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 1, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 2, False)
                #饱和
                compByCreateEffect.AddEffectToEntity("saturation", 31, 2, False)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 14)
            elif age in (81,82,83,84,85,86,87,88,89,90):
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 1, False)
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 2, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 3, False)
                #饱和
                compByCreateEffect.AddEffectToEntity("saturation", 31, 3, False)
                #不致命的中毒
                compByCreateEffect.AddEffectToEntity("poison", 31, 3, False)
                #播放粒子
                compByCreateCommand.SetCommand("execute " + playerName + " ~~~ " + "particle " +  "minecraft:water_splash_particle" + "^^^-0.5")
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 12)
            elif age in (91,92,93,94,95,96,97,98):
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 2, False)
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 2, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 4, False)
                #失明
                compByCreateEffect.AddEffectToEntity("blindness", 31, 0, False)
                #播放粒子
                compByCreateCommand.SetCommand("execute " + playerName + " ~~~ " + "particle " +  "minecraft:water_splash_particle" + "^^^-0.5")
                #禁止玩家跳跃
                compByCreatePlayer = Factory.CreatePlayer(playerId)
                compByCreatePlayer.SetPlayerJumpable(False)
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 10)
            elif age == 99:
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 2, False)
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 3, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 4, False)
                #失明
                compByCreateEffect.AddEffectToEntity("blindness", 31, 0, False)
                #不致命的中毒
                compByCreateEffect.AddEffectToEntity("poison", 31, 1, False)
                #不祥征兆
                compByCreateEffect.AddEffectToEntity("bad_omen", 31, 0, False)
                #播放粒子
                compByCreateCommand.SetCommand("execute " + playerName + " ~~~ " + "particle " +  "minecraft:water_splash_particle" + "^^^-0.5")
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 8)
            elif age == 100:
                #挖掘疲劳
                compByCreateEffect.AddEffectToEntity("mining_fatigue", 31, 3, False)
                #缓慢
                compByCreateEffect.AddEffectToEntity("slowness", 31, 5, False)
                #虚弱
                compByCreateEffect.AddEffectToEntity("weakness", 31, 5, False)
                #失明
                compByCreateEffect.AddEffectToEntity("blindness", 31, 0, False)
                #反胃
                compByCreateEffect.AddEffectToEntity("nausea", 31, 5, False)
                #致命的中毒
                compByCreateEffect.AddEffectToEntity("fatal_poison", 31, 0, False)
                #凋零
                compByCreateEffect.AddEffectToEntity("wither", 31, 0, False)
                #播放粒子
                compByCreateCommand.SetCommand("execute " + playerName + " ~~~ " + "particle " +  "minecraft:totem_particle" + "~~~")
                #设置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 6)

            elif age >= 101:
                #重置年龄
                self.playerAgeDict[playerId] = 0
                #self.checkAge()
                #生成头颅
                skullItemDict = {
                    'itemName': 'minecraft:skull',
                    'count': 1,
                    'enchantData': [(serverApi.GetMinecraftEnum().EnchantType.BowDamage, 1),],
                    'auxValue': 3,
                    'customTips':'§c' + playerName + str(self.playerEraDict[playerId]) + "世" '的头颅',
                    'enchantData': (0, 2)
                }
                compByCreateItem = Factory.CreateItem(playerId)
                compByCreateItem.SpawnItemToPlayerInv(skullItemDict, playerId)

                #个人世代+1
                self.AddPlayerEra(playerId,1)

                compByCreateCommand = Factory.CreateCommand(self.levelId)

                #改模型大小
                compByCreateScale.SetEntityScale(playerId, 0.3)

                #重置生命值
                compByCreateAttr.SetAttrMaxValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, 10)

                self.checkDie = False
                compByCreateCommand.SetCommand("kill @s")
                self.checkDie = True

                #获得等级作为奖励
                compByCreateLv = Factory.CreateLv(playerId)
                playerLv = compByCreateLv.GetPlayerLevel()
                rewardLv = playerLv + 10
                compByCreateLv.AddPlayerLevel(rewardLv)
                #获得钻石作为奖励
                diamondItemDict = {
                    'itemName': 'minecraft:diamond',
                    'count': 1,
                    'enchantData': [(serverApi.GetMinecraftEnum().EnchantType.BowDamage, 1),],
                    'auxValue': 0,
                }
                compByCreateItem.SpawnItemToPlayerInv(diamondItemDict, playerId)

                #通知全部人
                compByCreateGame = Factory.CreateGame(self.levelId)
                compByCreateGame.SetNotifyMsg("§l" + playerName + str(self.playerEraDict[playerId]) + "世 破壳了", serverApi.GenerateColor('BLUE'))

            #发送年龄字典给客户端
            print("发送年龄字典给客户端")
            self.checkAgeEvent(playerId)

    # OnScriptTickServer的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def OnScriptTickServer(self):

        #每秒增加30数值，到900时即30秒，就会添加年龄一次
        self.playerAgeValue += 1

        if self.playerAgeValue >= 900:
                if self.ageFlag == True:
                    print("30秒已到")
                    #调用添加所有人年龄
                    self.AddPlayerAge(1)
                    self.checkAge()
                    #发送消息
                    self.sendMessageToPlayer()
                self.playerAgeValue = 0
                self.ageFlag = True



    def UnListenEvent(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'OnScriptTickServer', self, self.OnScriptTickServer)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'AddServerPlayerEvent', self, self.OnAddServerPlayerEvent)
        self.UnListenForEvent("lifeTimeMod", "lifeTimeModClientSystem", 'jumpEvent', self, self.OnJumpEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerDieEvent', self, self.OnPlayerDieEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), 'PlayerEatFoodServerEvent', self, self.OnPlayerEatFoodServerEvent)
    def Destroy(self):
        self.UnListenEvent()