import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func import *

built_in_cmds = {}

def register_command(name, func):
    """
    注册命令，使命令与相应的处理函数建立映射关系
    @param name: 命令名
    @param func: 函数名
    """
    built_in_cmds[name] = func


def init():
    """
    注册所有的命令
    """
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("getenv", getenv)
    register_command("history", history)


def shell_loop():
    status = SHELL_STATUS_RUN

    while status == SHELL_STATUS_RUN:
        # 打印命令提示符，形如 `[<user>@<hostname> <base_dir>]$`
        display_cmd_prompt()

        # 忽略 Ctrl-Z 或者 Ctrl-C 信号
        ignore_signals()

        try:
            # 读取命令
            cmd = sys.stdin.readline()

            # 解析命令
            # 将命令进行拆分，返回一个列表
            cmd_tokens = tokenize(cmd)

            # 预处理函数
            # 将命令中的环境变量使用真实值进行替换
            # 比如将 $HOME 这样的变量替换为实际值
            cmd_tokens = preprocess(cmd_tokens)

            # 执行命令，并返回 shell 的状态
            status = execute(cmd_tokens)
        except:
            # sys.exc_info 函数返回一个包含三个值的元组(type, value, traceback)
            # 这三个值产生于最近一次被处理的异常
            # 而我们这里只需要获取中间的值
            _, err, _ = sys.exc_info()
            print(err)

def main():
    # 在执行 shell_loop 函数进行循环监听之前，首先进行初始化
    # 即建立命令与函数映射关系表
    init()

    # 处理命令的主程序
    shell_loop()

if __name__ == "__main__":
    main()




