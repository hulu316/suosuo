SuoSuo
===========
基于tornado、redis和bootstrap的一个聊天室。

简介
===========
1. 利用长轮询和redis的PUB/SUB实现了多人多频道实时通信。
2. 这个版本只实现了几个最基本的功能。

所需
===========
 * [tornado](https://github.com/tornadoweb/tornado)
 * [tornado-redis](https://github.com/leporo/tornado-redis)
 * [wtforms](https://github.com/wtforms/wtforms)
 * [wtforms-tornado](https://github.com/puentesarrin/wtforms-tornado)

已实现功能
===========
1. 用户注册、登陆和登出；
2. 频道的创建和订阅；
3. 频道未读信息的实时提醒；
4. 文字聊天；

待实现功能
===========
1. 用户邮箱验证；
2. 频道的修改和删除；
3. 所有频道的按序展示；
4. 用户和频道的头像；
5. 图片聊天；

链接说明
===========
1. 频道创建：/channel/create
2. 频道订阅：/channel/subscribe?cname=频道名

