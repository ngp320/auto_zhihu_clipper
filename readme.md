需要开着ss 防止被502
破解版的pycharm 用vpn 就不好用了。 偶尔下载包的时候打开，平时关掉。尤其是运行的时候
粘贴到link.txt时，用记事本 或者 notepad++ 不然软件容易炸
记得最后最新一条收藏完以后 标题上加两个字 标记，之后收藏就很方便了

# 使用说明
1 点开知乎 → 点头像 翻到状态 
2 使用ahk的自动PgDn，翻到没有剪藏的那一页（大概估计一下天数即可，
印象笔记搜索 "- 知乎" 能看到最近剪藏的网页），
F12 → copy outHtml → 用记事本或notepad++ 粘贴到 link.txt
3 用python 正则提取所有 question和zhuanlan 的链接link以及 question名
4 根据印象笔记，删除多余的链接
5 使用main.py 开始剪藏， 双手离开键盘即可
