import re
import os
import sys
from base64 import b64encode, b64decode
import argparse

self_name = os.path.basename(__file__)
base = os.path.basename

tmp_search = "self._server_socket.accept"
TMP_CONTENT = "logging.info(\"ipin:%s\"% conn[0])"

parser = argparse.ArgumentParser()
parser.add_argument("-t","--temp-file", help="which tmp file will be patch")
parser.add_argument("-r", "--replace", default=tmp_search, help="which key will be search and replace, default: %s" %tmp_search)
parser.add_argument("-p","--path", default=".", type=str, help="setting a path as root path  to search. defualt: \".\"")
parser.add_argument("--resume", default=False, action="store_true", help="resume all files , which has patched ")

args = parser.parse_args()
tmp_search = args.replace
if not args.temp_file:
    with open("/tmp/tmp-file", "w") as fp:
        fp.write(TMP_CONTENT)
    tmp = "/tmp/tmp-file"
else:
    tmp = args.temp_file

if not os.path.exists(tmp):
    print("tmp file not exists !")
    sys.exit(1)

def _replace(raw, tmp_file):
    pre_space = 0
    new = ''
    with open(tmp_file) as fp:
        new = fp.read()
    for i in raw:
        if i == ' ':
            pre_space += 1
        else:
            break
    news = [' ' * pre_space + i for i in  new.split("\n")]
    prefix = "##<!>%s<!>##" % b64encode(raw.encode('utf-8')).decode('utf-8')
    end = "##<!!>"
    news.insert(0, prefix)
    news.append(end)
    return raw +  '\n'.join(news) + '\n'

def resume(f):
    n = []
    with open(f) as fp:
        all_lines = fp.readlines()
        st = False
        for l in all_lines:
            if l.strip().startswith("##<!>"):
                raw = b64decode(l.strip().split("<!>")[2].encode('utf-8')).decode('utf-8')
                n.append(raw)
                st = True
                continue
            if st:
                if l.strip().startswith("##<!!>"):
                    st = False
                continue

            n.append(l)
    with open(f, "w") as fp:
        fp.writelines(n)

def replace(f, line , comp, tmp):
    a = []
    line = int(line) - 1
    with open(f) as fp:
        all_lines = fp.readlines()
        qq  = all_lines[line]
        if comp in qq:
            print("replace !!")
            all_lines[line] = _replace(qq,tmp)
        else:
            print(qq)
        a = all_lines
    os.popen("cp %s /tmp/ " % f)
    with open(f, 'w') as fp:
        fp.writelines(a)


if args.resume:
    tmp_search = "##<!>"

w = os.popen("grep -nr \"%s\"  %s" %  (tmp_search, args.path) ).readlines()
for l in w:
    f,line,_ = l.split(" ")[0].split(":")
    if base(f) == self_name:continue
    print(f, line)
    if args.resume:
        resume(f)
    else:
        replace(f, line, tmp_search, tmp)

