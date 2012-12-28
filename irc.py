import re
import os
import sys
import tempfile

def is_nickname(str):
    nick_regexp = '>\s(?<=[^a-z_\-\[\]\\^{}|`])[a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]*:\s'
    return re.search(nick_regexp, str)

def get_first_nick(str):
    nick = str[str.find("<")+1:str.find(">")]
    nick = re.sub("[@\+ ]+", "", nick)
    if re.search(".+-!-", nick):
        return None
    return nick

def get_last_nick(str):
    nick = re.search(r'(>.+:\s)', str).group(0)
    nick = nick.split(":")[0].replace("> ", "")
    nick = re.sub("[@\+ ]+", "", nick)
    if re.search(".+-!-", nick):
        return None
    return nick
    
def build_nick_set(data):
    nicks = set()
    
    for line in data:
        if is_nickname(line):
            nick = get_first_nick(line)
            if nick == None:
                continue             
            nicks.add(nick)

    for line in data:
        if is_nickname(line):
            lnick = get_first_nick(line)
            if lnick == None:
                continue             
            rnick = get_last_nick(line)
            if rnick == None:
                continue
            if rnick in nicks:
                nicks.add("%s -- %s;\n" % (lnick, rnick))   

    return " ".join(nicks)
                

def parse_log(filename):
    with open(filename) as file:
        content = file.readlines()
    file.close()

    return build_nick_set(content)

def write_file(filename, data):
    fd = open(filename, "w+")
    fd.write(data)
    fd.close()

if __name__ == '__main__':
    graph_start = 'graph graphname {\n '
    graph_data = ""
    graph_end = '}\n'
    graph_data = parse_log("dalo.log")
    graph = graph_start + graph_data + graph_end

    write_file("dalo.dot", graph)
