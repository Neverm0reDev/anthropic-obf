from marshal import dumps
from binascii import hexlify
from random import randint, shuffle
import os 

from pystyle import *

RED = '\033[1;91m'
WHITE = '\033[0m'
GREEN = '\033[1;32m'
GRAY = '\033[1;90m'
BLUE = '\033[1;34m'
CYAN = '\033[1;36m'
PURPLE = '\033[1;35m'

art = """
 ▄▄▄       ███▄    █ ▄▄▄█████▓ ██░ ██  ██▀███   ▒█████   ██▓███   ██▓ ▄████▄  
▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒▓██░ ██▒▓██ ▒ ██▒▒██▒  ██▒▓██░  ██▒▓██▒▒██▀ ▀█  
▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██▀▀██░▓██ ░▄█ ▒▒██░  ██▒▓██░ ██▓▒▒██▒▒▓█    ▄ 
░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ░▓█ ░██ ▒██▀▀█▄  ▒██   ██░▒██▄█▓▒ ▒░██░▒▓▓▄ ▄██▒
 ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ░▓█▒░██▓░██▓ ▒██▒░ ████▓▒░▒██▒ ░  ░░██░▒ ▓███▀ ░
 ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░    ▒ ░░▒░▒░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒▓▒░ ░  ░░▓  ░ ░▒ ▒  ░
  ▒   ▒▒ ░░ ░░   ░ ▒░    ░     ▒ ░▒░ ░  ░▒ ░ ▒░  ░ ▒ ▒░ ░▒ ░      ▒ ░  ░  ▒   
  ░   ▒      ░   ░ ░   ░       ░  ░░ ░  ░░   ░ ░ ░ ░ ▒  ░░        ▒ ░░        
      ░  ░         ░           ░  ░  ░   ░         ░ ░            ░  ░ ░      
                                                                     ░        
"""

purple = Col.StaticMIX([Col.blue, Col.purple])

def stage(text: str, symbol: str = f'+') -> str:
    ppurple = purple if symbol == '...' else Col.light_blue
    return f""" {Col.Symbol(symbol, ppurple, Col.blue)} {ppurple}{text}{Col.reset}"""

class Anthropic:

    vars = []

    def specterize(script: str) -> str:
        script = Anthropic.layer_1(script=script)
        script = Anthropic.layer_2(script=script)
        script = Anthropic.layer_3(script=script)
        return script

    def hex(text: str) -> bytes:
        return "b'" + "".join(fr"\x{hexlify(t.encode('utf-8')).decode()}" for t in text) + "'"

    def encrypt(text: str, key: int) -> str:
        return "\x00".join(str(ord(x)+key) for x in text)

    def randvar() -> str:
        var = randint(1000, 9999)
        while var in Anthropic.vars:
            var = randint(1000, 9999)
        Anthropic.vars.append(var)
        return f"__{var}__"
    
    def get_key_by_value(vars, key) -> str:
        return list(vars.keys())[list(vars.values()).index(key)]

    def layer_1(script: str) -> str:
        ten_split = []
        key = randint(3, 33)
        splitting = randint(3, 9)
        while True:
            if len(script) >= splitting:
                ten_split.append(Anthropic.hex(Anthropic.encrypt(script[:splitting], key)))
                script = script[splitting:]
            else:
                ten_split.append(Anthropic.hex(Anthropic.encrypt(script, key)))
                break
        lexec = Anthropic.hex(Anthropic.encrypt("exec", key))
        lkey = Anthropic.hex(str(key))
        ten_split.append(lexec)
        ten_split.append(lkey)
        ten_split.append("globals")
        correct = [x for x in ten_split]
        shuffle(ten_split)
        vars = {Anthropic.randvar(): x for x in ten_split}
        script = ",".join(vars.keys()) + '=' + ",".join(vars.values()) + '\n'
        all_correct = []
        for x in correct:
            if x not in (lexec, lkey, "globals"):
                all_correct.append(Anthropic.get_key_by_value(vars, x))
        l1, l2, l3 = Anthropic.randvar(), Anthropic.randvar(), Anthropic.randvar()
        glob = f"{Anthropic.get_key_by_value(vars, 'globals')}()[{l1}({l2}={Anthropic.get_key_by_value(vars, lexec)})]"
        print(stage("Creating random vars..."))
        lambdas = [fr"{l1}=lambda {l2}:''.join(chr(int({l3})-int({lkey}))for {l3} in {l2}.decode().split('\x00'))",
                   f"(lambda {l3}:{glob}(''.join({l1}({l2}={l2})for {l2} in {l3}),{Anthropic.get_key_by_value(vars, 'globals')}()))([{','.join(all_correct)}])",]
        script = "from builtins import *\n" + script + '\n'.join(lambdas)
        return script

    def layer_2(script: str) -> str:
        print(stage("Compiling and dumping code with marshal..."))
        return dumps(compile(script, 'Anthropic', 'exec'))

    def layer_3(script: str) -> str:
        split = []
        splitting = 2000
        while True:
            if len(script) >= splitting:
                split.append(script[:splitting])
                script = script[splitting:]
            else:
                split.append(script)
                break
        vars = {Anthropic.randvar(): x for x in split}
        codevars = "\n".join(f"{a} = Func.calculate({randint(1,9)}){' ' * 500},Func.define('{a}', {b})" for a, b in vars.items())
        print(stage("Camouflation of the obfuscated code..."))
        script = fr"""
Any = (...,)

class Anthropic:
    def __init__(self, code: str) -> None:
        self.code = code
        self.execute(...)
        return None
    def execute(self, code: str = ...) -> None:
        return exec(str(code))
    
class Func:
    def calculate(num: int) -> int:
        return num*2
    def define(key, value: Any) -> Any:
        globals()[key] = value
        return globals()[key]

{codevars}


if __name__ == '__main__':
    Anthropic("Anthropic"){' ' * 500},exec(__import__('marshal').loads({"+".join(var + "[1]" for var in vars)}),globals())"""[1:]
        return script


def main():
    System.Size(150, 40)
    os.system("cls")
    os.system("title ᴀɴᴛʜʀᴏᴘɪᴄ")
    Cursor.HideCursor()
    print()
    print(Colorate.Vertical(Colors.purple_to_blue, Center.XCenter(art + '\n\n')))

    file = input(stage(f"Drag the file you want to obfuscate {Col.blue}-> {Col.reset}", "?")).replace('"','').replace("'","")
    print('\n')

    try:
        with open(file, mode='rb') as f:
            script = f.read().decode('utf-8')
        filename = file.split('\\')[-1]
    except:
        input(f""" {Col.Symbol('!', Col.light_red, Col.blue)} {Col.light_red}Invalid file!{Col.reset}""")
        exit()

    script = Anthropic.specterize(script=script)

    with open(f'obf-{filename}', mode='wb') as f:
        f.write(script.encode('utf-8'))
    
    print('\n')
    input(stage("Done!", '!'))


main()
