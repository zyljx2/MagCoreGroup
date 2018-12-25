import requests
import json
url = 'http://test.magcore.clawit.com'
#创建游戏  返回游戏id   gid
def createGame(map):
    url = 'http://test.magcore.clawit.com/api/game'
    payload = "{\"Map\":\"%s\"}"%map
    # print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache'
    }
    response = requests.request('POST', url, data=payload, headers=headers)
    # print(response.status_code)
    # print(response.text)
    return response.text
#创建玩家  返回玩家信息字典
def createPlayer(username,color):
    url = 'http://test.magcore.clawit.com/api/player'
    payload = "{\"Name\":\"%s\",\"Color\":%s}" % (username, int(color))
    headers = {
        'Content-Type': 'application/json',
        'Cache-Contro': 'no-cache'
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    # print(response.status_code)
    # print(response.json())
    return response.json()
#加入游戏
def joinGame(gid,pid):
    url = 'http://test.magcore.clawit.com/api/game'
    payload ="{\"Game\":\"%s\",\"Player\":\"%s\"}"%(gid,pid)
    headers = {
        'Content-type': 'application/json',
        'Cache-Contro': 'no-cache'
    }
    response = requests.request("PATCH", url, data=payload, headers=headers)

    if response.status_code == 200:
        print('成功加入')
        return 1
    else :
        print("加入失败")
        return 0
#开始游戏
def startGame(gid):
    url = 'http://test.magcore.clawit.com/api/game/%s'%gid
    headers = {
        'Cache-Contro': 'no-cache'
    }
    response = requests.request("PUT",url,headers=headers)
    # print(response)
    if response.status_code == 200:
        print("游戏开始")
        return 1
    else :
        print('开始失败')
        return 0
#获取玩家详情
def getPlayer(pid):
    url = 'http://test.magcore.clawit.com/api/player/%s' % pid
    headers = {
        'Cache-Contro': 'no-cache'
    }
    response = requests.request("GET", url, headers=headers)
    # print(response)
    return response.json()
#获取地图详情
def getMap(map_name):
    url = 'http://test.magcore.clawit.com/api/map/%s' % map_name
    headers = {
        'Cache-Contro': 'no-cache'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()
#攻击
def attact(gid,pid,x,y):
    url = 'http://test.magcore.clawit.com/api/cell/'
    payload = "{\"Game\":\"%s\",\"Player\":\"%s\", \"X\":%s, \"Y\":%s}"%(gid,pid,x,y)
    headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache"
    }
    response = requests.request("PUT", url, data=payload, headers=headers)
    print('attack',response.text)  #结束是gameover
    if response.text == 'Game over':
        return 2
    if response.status_code == 200:
        print('攻击成功')
        return 1
    else:
        print('攻击失败')
        return 0
#获取游戏详情  得到玩家index  和每个单元的信息cell
def getGame(gid):
    url ='http://test.magcore.clawit.com/api/game/%s' % gid
    headers = {
        'Cache-Contro': 'no-cache'
    }
    response = requests.request("GET",url,headers=headers)
    # print(response.json()["Cells"])
    return response.json()

#攻击流程   传入游戏id和玩家id
def fight(gid,pid):

    # 获取自己的基地位置及相关信息 存储下来
    player_msg = getPlayer(pid)
    base=player_msg["Bases"]   #[3,7]  ['3,0']
    #玩家基地坐标
    BASE = [int(base[0].split(",")[0]),int(base[0].split(",")[1])]
    print(BASE)
    #玩家索引号
    INDEX = player_msg["Index"]
    #获取游戏详情，每个单元的信息和地图类型
    game_msg = getGame(gid)
    cell_dic = game_msg["Cells"]
    map_type = game_msg["Map"]
    #获取地图大小
    map_msg = getMap(map_type)
    rows_lst = map_msg["Rows"]
    map_size = len(rows_lst)
    #玩家可攻击单元列表
    location_lst = [[BASE[0], BASE[1] - 1], [BASE[0] + 1, BASE[1]], [BASE[0], BASE[1] + 1], [BASE[0] - 1, BASE[1]]]

    while 1:
        #遍历可攻击单元列表 cell状态为2 加入优先攻击列表 first_atk[]  状态为0但类型不为0 加入次攻击列表second_atk[]
        first_atk =[]
        second_atk=[]
        for el in location_lst:

            y = el[1]
            x = el[0]
            if y >= map_size or x >= map_size:
                print('跳过',x,y)
                continue
            if  cell_dic[y][x]['State'] == 2:
                first_atk.append([x,y])
            elif cell_dic[y][x]['State'] == 0 and cell_dic[y][x]['Type'] != 0:
                second_atk.append([x,y])

        #依次遍历攻击列表，攻击
        for point in first_atk:
            res1 = attact(gid,pid,point[0],point[1])
            if res1 == 2:
                return 2
        for point in second_atk:
            res2 = attact(gid, pid, point[0], point[1])
            if res2 == 2:
                return 2
        #判断玩家状态
        player_msg = getPlayer(pid)
        player_state = player_msg["State"]
        if player_state == 2:
            print("你已被击败！！！")
            break
        # 获取游戏详情，得到单元的信息
        game_msg = getGame(gid)
        cell_dic = game_msg["Cells"]
        #获取自己已占有的单元
        has_cell= []
        for row in cell_dic:
            for cell in  row:
                if cell['Owner'] == INDEX:
                    has_cell.append([cell["X"],cell["Y"]])
        #可攻击的单元列表
        location_lst = []
        for el in has_cell:
            location_lst.extend([[el[0],el[1]-1],[el[0]+1,el[1]],[el[0],el[1]+1],[el[0]-1,el[1]]])
        new_location_lst = []
        for i in location_lst:
            if i not in new_location_lst:
                new_location_lst.append(i)
        location_lst = new_location_lst

#------------------------------分割----------------
if __name__ == '__main__':

    # 创建游戏
    gid = createGame("RectSmall")
    print('游戏id', gid)

    #运行
    def run(gid):
        # 创建玩家1
        username = input('玩家名>>').strip()
        color = input('颜色>>').strip()
        p_dic = createPlayer(username, color)
        pid = p_dic["Id"]
        print("玩家1 id", pid)
        # 加入游戏
        joinGame(gid,pid)
        #是否开始
        # while 1:
        #     game_msg = getGame(gid)
        #     game_state = game_msg["State"]
        #     if game_state == 1:
        #         break
        #创建玩家2
        username = input('玩家名>>').strip()
        color = input('颜色>>').strip()
        p2_dic = createPlayer(username, color)
        pid2 = p2_dic["Id"]
        print("玩家2 id", pid2)
        # 加入游戏
        joinGame(gid, pid2)

        select = input('是否开始游戏？y or n')
        if select.upper()=='Y':
            #游戏开始
            startGame(gid)
            fight(gid,pid)

    run(gid)
