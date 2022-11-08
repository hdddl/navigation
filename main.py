# coding=utf-8
from telnetlib import SGA
from jinja2 import Template
import json
import re

# 渲染为 HTML
def render_to_file():
    with open("data.json", "r") as f:     # read json data
        data = json.loads(f.read())
    
    with open("base.html", "r") as f:       # read template
        template = Template(f.read())
    
    html = template.render(                 # render template
        data = data["data"], 
        background=data["background"],
        copyright = data["copyright"]
    )
    with open("./assert/index.html", "w") as index:     # write to file
        index.write(html)


# 编辑网站，包括添加类别，删除类别，添加网站，删除网站
def edit_website():
    with open("data.json", "r", encoding="utf-8") as f:      
        data = json.loads(f.read())

    print("into edit mode")
    cmd = ""        # 用于记录命令
    category = ""       # 用于记录所处类别

    helpInfo = """
        1. exit 退出编辑模式
        2. list category 列出所有分类
        3. select category 选择分类
        4. list sites 列出当前分类小的所有网站
        5. add site 添加网站到当前分类
        6. delete site 从当前分类删除网站
    """

    while(True):
        print(">>(%s) " % category, end="")
        cmd = input()
        if(cmd == "help"):
            print(helpInfo)
        elif(cmd == "exit"):      # 退出编辑模式
            print("exit edit mode")
            return
        elif(cmd == "list category"):     # 列出类别
            for i in data["data"]:
                print(i["category"])
        elif(cmd == "list sites"):        # 列出当前类别的所有网站
            if category == "":
                print("select category first")
                continue
            for i in data["data"]:
                if i["category"] == category:
                    for j in i["sites"]:
                        print(j["name"])
        elif(cmd == "add site"):      # 添加网站
            if category == "":
                print("select category first")
                continue
            print("name >> ", end="")
            name = input()
            print("url >> ", end="")
            url = input()
            print("svg >> ", end="")
            svg = input()
            svg = svg.replace("\"", '\"')
            for i in data["data"]:
                if i["category"] == category:
                    i["sites"].append({
                        "name": name,
                        "url": url,
                        "svg": svg
                    })
            print("add site success")
            with open("data.json", "w", encoding="utf-8") as f:      
                json.dump(data, f, indent=4, ensure_ascii=False)
            render_to_file()
        elif cmd == "delete site":
            if category == "":
                print("select category first")
                continue
            print("name >> ", end="")
            name = input()
            for i in data["data"]:
                if i["category"] == category:
                    for j in i['sites']:
                        if j['name'] == name:
                            i['sites'].remove(j)
            print("delete site success")
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            render_to_file()
        elif(re.match("select.*", cmd)):
            category = cmd.split(" ")[-1];
        else:
            print("command not found")

# 通用命令处理
def main():
    cmd = ""
    helpInfo = """
        1. exit 退出
        2. edit 编辑模式
    """
    while(cmd != "exit"):
        print(">> ", end="")
        cmd = input()
        if(cmd == "exit"):
            print("bye bye ~")
            return
        elif(cmd == "edit"):
            edit_website()
        elif(cmd == "help"):
            print(helpInfo)
        else:
            print("command not found")



if __name__ == "__main__":
    main()