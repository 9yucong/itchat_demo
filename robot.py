import itchat, requests

ROBOT = 'robot'
REMOVE_ROBOT = 'remove_robot'

USER_NICKNAME = None
GROUP_NICKNAME = None

HELP_MSG = '''
设定撩对象格式：U/G:(对象名)
U(en)---机器人撩用户昵称为：en
G(en)---机器人撩群聊名字为：en
输入remove_robot，来停止机器人
'''


def get_tuling_answer(info):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '86ba8d239a4142679f4b0f7f0f3423ec',
        'info': info,
        'userid': 'cong',
    }
    resp = requests.post(url=url, data=data).json()
    return resp.get('text')


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def reply_user(msg):
    global USER_NICKNAME
    global GROUP_NICKNAME
    if msg['ToUserName'] == 'filehelper':
        content = msg['Text'].strip().lower()
        if content.find(ROBOT) != -1:
            itchat.send(help(), 'filehelper')
        elif content.find(REMOVE_ROBOT) != -1:
            GROUP_NICKNAME = None
            USER_NICKNAME = None
            itchat.send('已停止所有机器人', 'filehelper')
        else:
            type = content[0]
            nickname = content[content.find('(') + 1:len(content) - 1].strip()
            if type == 'u':
                USER_NICKNAME = nickname
                GROUP_NICKNAME = None
            elif type == 'g':
                GROUP_NICKNAME = nickname
                USER_NICKNAME = None
            itchat.send('机器人在撩%s' % nickname, 'filehelper')
        return
    '''机器人回复好友'''
    user = msg['User']
    if not USER_NICKNAME or 'NickName' not in user or user['NickName'].lower().find(
            USER_NICKNAME) == -1 or 'UserName' not in user: return
    answer = get_tuling_answer(msg['Text'])
    itchat.send(answer, toUserName=user['UserName'])


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def reply_group(msg):
    '''机器人回复群聊'''
    chatroom = msg['User']
    if not GROUP_NICKNAME or 'NickName' not in chatroom or chatroom['NickName'].lower().find(
            GROUP_NICKNAME) == -1 or 'UserName' not in chatroom: return
    answer = get_tuling_answer(msg['Text'])
    itchat.send(answer, toUserName=chatroom['UserName'])


itchat.auto_login(True)
itchat.run()
