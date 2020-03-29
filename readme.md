pycharm 运行的时候关闭 全局vpn（例如proxifier）

粘贴到link.txt时，用记事本 或者 notepad++ 不然软件容易炸

记得最后最新一条收藏完以后 标题上加两个字 标记，之后收藏就很方便了

记得关闭chrome插件 onenote 和 adblock ，影响selenium元素查找

# 使用说明
1 点开知乎 → 点头像 翻到状态 

2 使用ahk的自动PgDn，翻到没有剪藏的那一页（第一次只能手动判断, 第二次可以看保存的newlink历史txt文档,第一条链接即是分界线），

F12 → copy outHtml → 用 "记事本" 或 "notepad++" 粘贴到 link.txt

3 用python(pre.py) 正则提取所有 question和zhuanlan 的链接link以及 question名, 到newLink

4 根据印象笔记，删除多余的链接

5 使用main.py 开始剪藏， 双手离开键盘即可
