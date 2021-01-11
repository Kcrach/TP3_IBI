# coding : utf8
# !/usr/bin/env python

import subprocess

import agent as ag
import random as rd
import copy

STUDENT_ID = 11608160

NB_AGENT = 100
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
    return agents


def step_generate(agents):
    """Return a new agent set according to fitness."""

    new_agents = []
    total_fitness = 0.
    for a in agents:
        total_fitness += a.fitness

    for _ in range(len(agents)):
        score = rd.uniform(0., total_fitness)
        index = 0
        current_agent = None
        while score > 0.:
            score -= agents[index].fitness
            current_agent = agents[index]
            index += 1
        new_agents.append(ag.Agent())
        new_agents[-1] = current_agent

    return new_agents


def step_generate_rank(agents):
    agents = sorted(agents, key=lambda x: x.fitness)
    new_agents = []
    total_score = (len(agents) * (len(agents) + 1)) // 2
    for _ in range(len(agents)):
        score = rd.randint(1, total_score)
        index = 0
        current_agent = ag.Agent()
        delta = 0
        while score > 0:
            delta += 1
            current_agent = agents[index]
            index += 1
            score -= delta
        new_agents.append(ag.Agent())
        new_agents[-1] = copy.deepcopy(current_agent)
    return new_agents


def random_mutation(agents):
    for i in range(rd.randint(0, len(agents) // 20)):
        agent_index = rd.randint(0, len(agents) - 1)
        agents[agent_index].set_random()
    return agents


def step(agents):
    step_run(agents)
    # agents = step_generate(agents)
    agents = step_generate_rank(agents)
    agents = step_mutate(agents)
    agents = random_mutation(agents)
    return agents


def init(agents):
    for a in agents:
        a.set_random()


if __name__ == "__main__":

    agent_list = []
    for _ in range(NB_AGENT):
        agent_list.append(ag.Agent(POOL))

    init(agent_list)

    for i in range(2000):
        best = 0.
        best_value = ""
        print("---")
        for current in agent_list:
            if best < current.fitness:
                best = current.fitness
                best_value = current.value
        print(best, best_value)
        agent_list = step(agent_list)
        """for current in agent_list:
            print(current)"""

    # print all agents with their fitness
    for current in agent_list:
        print(current)
