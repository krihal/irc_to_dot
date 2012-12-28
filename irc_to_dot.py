import re
import os
import sys

def is_nickname(str):
    nick_regexp = '>\s(?<=[^a-z_\-\[\]\\^{}|`])[a-z_\-\[\]\\^{}|`][a-z0-9_\-\[\]\\^{}|`]*:\s'
    return re.search(nick_regexp, str)

def is_nick_pair(str):
    if re.search("\w+\s--\s\w+;", str):
        return True
    return False

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
    
def get_all_nicks(data):
    nicks = set()
    
    for line in data:
        if not is_nickname(line):
            continue

        nick = get_first_nick(line)
        if nick == None:
            continue             

        nicks.add(nick)
            
    return nicks

def get_nick_pairs(nicks, data):
    pairs = set()

    for line in data:
        if not is_nickname(line):
            continue 

        lnick = get_first_nick(line)
        if lnick == None or lnick == "":
            continue             

        rnick = get_last_nick(line)
        if rnick == None or rnick == "":
            continue

        if rnick in nicks:
            lnickstr = "%s -- %s;" % (lnick, rnick) 
            rnickstr = "%s -- %s;" % (rnick, lnick) 

            if rnickstr in nicks:
                continue
                
            pairs.add(lnickstr)
                
    return pairs

def build_nick_set(data):
    nicks = set()
    tmpnicks = set()
    pairs = set()

    nicks = get_all_nicks(data)
    pairs = get_nick_pairs(nicks, data)

    return pairs
                
def parse_log(filename):
    with open(filename) as file:
        content = file.readlines()
    file.close()

    return "\n".join(build_nick_set(content))

def write_file(filename, data):
    fd = open(filename, "w+")
    fd.write(data)
    fd.close()

if __name__ == '__main__':
    graph_start = 'graph graphname {\n '
    graph_data = ""
    graph_end = '\n}\n'
    graph_data = parse_log("dalo.log")
    graph = graph_start + graph_data + graph_end

    write_file("dalo.dot2", graph)
