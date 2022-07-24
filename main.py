# coding=utf-8
from jinja2 import Template
import json

def render_to_file():
    with open("./data.json", "r") as f:     # read json data
        data = json.load(f)
    
    with open("base.html", "r") as f:       # read template
        template = Template(f.read())
    
    html = template.render(                 # render template
        data = data["data"], 
        background=data["background"],
        copyright = data["copyright"]
    )
    with open("./assert/index.html", "w") as index:     # write to file
        index.write(html)
            

def main():
    render_to_file()
    
    




if __name__ == "__main__":
    main()