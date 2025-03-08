# use_deepseek
###一个支持用户自定义对话和知识库的人工智能科研助理，基于deepseek官方api。
###基于gradio==5.9.0框架，实现调用各家llm的api并可以本地下载保存、自定义编辑以及上传重载llm记忆（prompt）的功能。
###保存和重载记忆的功能基于一个.card格式的“记忆卡”。此记忆卡可以互相传输复制以及分享，它可以利用多轮prompt载入实现如角色扮演、信息注入、格式指定等功能，称之为模板。
###py文件内有详细注释，填入api后，支持web部署，在选择“远程部署访问”模式后打开系统防火墙对应端口出入规则便可以远程访问网页。
###还有一个基于webview的本地应用版本，之后有空会上传。
###此程序是自用人工智能工具集程序的一部分，其他部分整理好了会开源的。
###目前use_deepseek为0.3版本，后续会追加更多功能以及对应收集的各式好用的模板。
###基于组内各专业领域专家用户问答结果整理的detaset会发布。
---------------------------------------------------------
感谢深度求索公司的deepseek产品及其的开源！感谢gradio库的开源
---------------------------------------------------------
