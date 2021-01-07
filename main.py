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


# Algo Gen functions

def step_run(agents):
    """Run unlock64.exe for each agent and attribute the fitness."""
    to_run = []
    for a in agents:
        to_run.append(a.value)

    result = check(STUDENT_ID, to_run)

    for i in range(len(result)):
        agents[i].fitness = result[i]


def step_mutate(agents):
    """Mutate each agent."""
    for a in agents:
        a.mutate()


def step_generate(agents):
    """Return a new agent set according to fitness."""
    return agents


def step(agents):
    step_run(agents)
    agents = step_generate(agents)
    step_mutate(agents)


def init(agents):
    for a in agents:
        a.set_random()


if __name__ == "__main__":

    agent_list = []
    for _ in range(NB_AGENT):
        agent_list.append(ag.Agent(POOL))

    init(agent_list)

    step(agent_list)

    # print all agents with their fitness
    for current in agent_list:
        print(current)
