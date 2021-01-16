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

iteration = 0


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
        old = a.value
        for _ in range(rd.randint(1, 1)):
            a.mutate()
        # print(old, "to", a.value)
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
    best_agents = agents[-(len(agents) // 10):]
    best_agent = agents[-1]
    new_agents = []
    offset = 0  # set to zero for basic approach
    total_score = (len(best_agents) * (len(best_agents) + 1)) // 2 - offset
    for _ in range(len(agents)):
        score = rd.randint(1, total_score) + offset
        index = 0
        current_agent = ag.Agent()
        delta = 0
        while score > 0:
            delta += 1
            current_agent = best_agents[index]
            index += 1
            score -= delta
        new_agents.append(ag.Agent())
        new_agents[-1] = copy.deepcopy(current_agent)
    new_agents[-1] = best_agent
    return new_agents


def random_mutation(agents):
    for i in range(rd.randint(0, len(agents) // 20)):
        agent_index = rd.randint(0, len(agents) - 1)
        agents[agent_index].set_random()
    return agents


def heavy_mutation(agents):
    for i in range(rd.randint(0, len(agents) // 20)):
        agent_index = rd.randint(0, len(agents) - 1)
        for j in range(4):
            agents[agent_index].mutate()
    return agents


def get_children(agents):
    done = []
    for _ in range(int(len(agents) / 10)):
        target = rd.randint(0, len(agents) - 1)
        while target in done:
            target = rd.randint(0, len(agents) - 1)
        dad = agents[target]
        # mum = agents[i + 1]
        done.append(target)
        target_2 = rd.randint(0, len(agents) - 1)
        while target_2 in done:
            target_2 = rd.randint(0, len(agents) - 1)
        mum = agents[target_2]
        dad_percent = dad.fitness / (dad.fitness + mum.fitness)
        # print(str(dad), str(mum))
        new_agent = ag.Agent(POOL)
        for k in range(max(len(dad.value), len(mum.value))):
            if rd.uniform(0., 1.) < dad_percent:
                if len(dad.value) > k:
                    new_agent.value += dad.value[k]
            else:
                if len(mum.value) > k:
                    new_agent.value += mum.value[k]
        agents[target] = new_agent
        # print("gives", new_agent)

    return agents


def get_best_children(agents):
    count = len(agents) // 10
    best_agents = sorted(agents, key=lambda x: x.fitness)[-count:]
    new_agents = []

    for _ in range(count):
        dad = best_agents[rd.randint(0, count - 1)]
        mum = best_agents[rd.randint(0, count - 1)]
        new = ag.Agent(POOL)
        for i in range(min(len(dad.value), len(mum.value))):
            if rd.randint(0, 1) == 0:
                new.value += dad.value[i]
            else:
                new.value += mum.value[i]
        new_agents.append(new)

    for i in range(len(new_agents)):
        agents[rd.randint(0, len(agents) - 1)] = new_agents[i]
    return agents


def step(agents):
    step_run(agents)

    if rd.randint(0, 100) == 0:
        print("---")
        # print_agents(agents)
        print_best(agents)

    # agents = step_generate(agents)
    agents = step_generate_rank(agents)
    best_agent = copy.deepcopy(agents[-1])
    # agents = get_children(agents)
    get_best_children(agents)
    agents = step_mutate(agents)
    # agents = random_mutation(agents)
    agents = heavy_mutation(agents)
    agents[-1] = best_agent

    return agents


def print_agents(agents):
    for a in agents:
        print(str(a))


def print_best(agents):
    best = None
    best_value = None
    for a in agents:
        if best is None or best < a.fitness:
            best = a.fitness
            best_value = a.value
    print(best, best_value)


def init(agents):
    for a in agents:
        a.set_random()


if __name__ == "__main__":

    # good password for 11608160 is XD54BLA1RE4U68

    seed = None
    # seed = "XD54BLA1RE4U6"

    agent_list = []
    for _ in range(NB_AGENT):
        agent_list.append(ag.Agent(POOL))

    init(agent_list)

    if seed is not None:
        agent_list[-1].value = seed

    iteration = 0
    while MAX_GEN == -1 or iteration < MAX_GEN:
        print(iteration)
        iteration += 1
        agent_list = step(agent_list)
        if agent_list[-1].fitness >= 1.0:
            print("Done")
            break

    # print all agents with their fitness
    step_run(agent_list)
    print_agents(agent_list)
    print_best(agent_list)
