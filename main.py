# coding : utf8
# !/usr/bin/env python

import subprocess

import agent as ag

STUDENT_ID = 11608160

NB_AGENT = 50
MAX_GEN = -1  # -1: until solution is found
POOL = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


def check(student_id, passwords):
    proc = subprocess.Popen(["./unlock64.exe", str(student_id)]
                            + passwords, stdout=subprocess.PIPE)
    results = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        results.append(float(str(line).split("\\t")[1]
                             .split("\\r\\n")[0]))
    return results


def step_run(agents):
    pass


def step_mutate(agents):
    pass


def step_generate(agents):
    pass

def step(agents):
    step_run(agents)
    step_mutate(agents)


if __name__ == "__main__":

    agent_list = [ag.Agent(POOL)] * NB_AGENT

    print(check(STUDENT_ID, ["PASSWORD"]))
