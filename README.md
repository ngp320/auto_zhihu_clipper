# 前置条件
1 chrome → Tampermonkey → 知乎重排for印象笔记  
2 chrome 关闭 油猴 印象笔记 以外的插件.避免影响  

# 注意事项
1 (个人原因)pycharm 运行的时候关闭 全局vpn（例如proxifier）  
2 粘贴到link.txt时，
3 记得关闭chrome插件 onenote 和 adblock ，影响selenium元素查找  

# 使用说明
1 点开知乎 → 点头像 翻到状态   
2 浏览器F12, 选中所有需要剪藏的链接, 右键, copyoutHtml (链接>100时,用记事本 黏贴 不然软件容易炸)
3 黏贴到link.txt
4 运行 pre.py
5 根据last_time_newlink，删除多余的链接  
6 使用main.py 开始剪藏， 双手离开键盘即可  
P.S. 自动保存, link到根据 last_time_newlink
P.S. 因为是倒序剪藏, last_time_newlink第一行就是上次运行程序最后剪藏的位置
