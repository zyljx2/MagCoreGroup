import funcs

# 运行过程
def run():
    gid =''
    print('''
        选择你要进行的操作
        1、创建游戏
        2、创建玩家
        3、退出
    ''')
    while 1:
        choose = input('你的选择>').strip()

        if choose =="1":
            # 创建游戏
            gid = funcs.createGame("RectSmall")
            print('游戏id', gid)
        elif choose =='2':
            # 创建玩家1
            try:
                username = input('玩家名>>').strip()
                color = input('颜色>>').strip()
                p_dic = funcs.createPlayer(username, color)
            except Exception:
                username = input('玩家名>>').strip()
                color = input('颜色>>').strip()
                p_dic = funcs.createPlayer(username, color)
            pid = p_dic["Id"]
            print("玩家1 id", pid)

            join = input('是否加入游戏？y or n >')
            if join.upper()=='Y':
                if not gid:
                    gid = input('输入游戏id >>>')
                    # 加入游戏
                    funcs.joinGame(gid, pid)

                    select = input('是否开始游戏？y or n')
                    if select.upper() == 'Y':
                        # 游戏开始
                        funcs.startGame(gid)
                        #对战
                        funcs.fight(gid, pid)
        else:
            print('退出游戏')
            break

run()