"""
various instantOS tools/bindings for python
"""

import subprocess
from itertools import tee
from collections.abc import Iterable
import os

def instantmenu(prompt: str, items: Iterable[str], assist:bool=False, flags:Iterable[str]=None, encoding:str="utf8"):
    """
    Launches an instantmenu to prompt the user for input,
    and returns the index of the selected item.
    """
    cmd = ["instantmenu"]
    cmd.append("-p")
    cmd.append(prompt)
    if flags != None:
        cmd.extend(flags)
    if assist:
        cmd.append("-n")
        cmd.append("-F")
        cmd.append("-ct")
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    items, items2 = tee(items)
    process.stdin.writelines(map(lambda x: (x+'\n').encode(encoding), items))
    process.stdin.close()
    result = process.stdout.readline().decode(encoding)
    process.kill()
    for i, v in enumerate(items2):
        if result[:-1] == v:
            return i
    return None

def instantassist(assists: list):
    """
    prompts the user with an instantassist-like tree of keys to 
    example:
    instantassist([
        ['f run foo software', 'st -e foo'],
        ['s subsection/folder',
            ['a sub a', 'echo a'],
            ['b sub b', 'echo b'],
        ],
    ])
    """
    choice = instantmenu('instantassist',
            map(lambda item: item[0], assists),
            assist=True)
    if choice != None:
        result = assists[choice][1]
        if isinstance(result, str):
            os.system(result)
        elif isinstance(result, Iterable):
            instantassist(assists[choice][1:])

def instantwmctrl(property:str, value):
    """
    works the same as `instantwmctrl` on the command line.
    
    Examples:
        instantwmctrl('animated', 0) # toggle animated
        instantwmctrl('animated', 1) # disable animations
        instantwmctrl('animated', 2) # enable animations
    """
    os.system("instantwmctrl " + property + " " + str(value))
