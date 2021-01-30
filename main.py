# coding : utf8
# !/usr/bin/env python

import subprocess
from typing import List

import agent as ag
import random as rd
import copy
import sys

STUDENT_ID = 11608160

NB_AGENT = 100
MAX_GEN = 300  # -1: until solution is found
VERBOSE = False
ALLOW_LOOP = False

conf = dict()


def check(student_id: int, passwords: List[str]) -> List[float]:
    """
    Execute unlock with the given numbers and returns the results.
    :param student_id: the student id used to generate the password.
    :param passwords: list of passwords.
    :return: list of the results.
    """
    target = "./unlock64.exe"
    sep = "\\r\\n"
    if sys.platform == "linux":
        target = "./unlock"
        sep = "\\n"

    proc = subprocess.Popen([target, str(student_id)]
                            + passwords, stdout=subprocess.PIPE)
    results = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        results.append(float(str(line).split("\\t")[1].split(sep)[0]))
    return results


def config(path: str) -> None:
    """
    Load the configuration file.
    :param path: path of the configuration file.
    :return: None
    """
    with open(path, "r") as conf_file:
        for line in conf_file.readlines():
            words = line.split()
            if len(line) > 1 and words[0] != "#" and words[0][0] != '#':
                if len(words) < 3:
                    words = "".join(line.split("=")).split(" ")
                    key = words[0]
                    value = words[1].replace("\n", "")
                else:
                    key = words[0]
                    value = words[2]

                if key == "allow_loop":
                    value = value.lower()
                    if value == "0" or value == "false":
                        conf[key] = False
                    else:
                        conf[key] = True

                elif key == "nb_agents":
                    conf[key] = int(value)

                elif key == "max_iterations":
                    conf[key] = int(value)

                elif key == "seed":
                    if value == "\"\"":
                        value = None
                    conf[key] = value

                elif key == "student_id":
                    conf[key] = int(value)

                elif key == "verbose":
                    value = value.lower()
                    if value == "0" or value == "false":
                        conf[key] = False
                    else:
                        conf[key] = True

    print(conf)


# Algo Gen functions

def step_run(agents: List[ag.Agent]) -> None:
    """
    Run unlock64.exe for each agent and attribute the resulting fitness.
    :param agents: list of agents.
    :return: None
    """
    to_run = []
    for a in agents:
        to_run.append(a.value)

    result = check(STUDENT_ID, to_run)

    for i in range(len(result)):
        agents[i].fitness = result[i]


def step_mutate(agents: List[ag.Agent]) -> List[ag.Agent]:
    """
    Mutate each agent.
    :param agents: list of agents.
    :return: list of mutated agents.
    """
    for a in agents:
        a.mutate()
    return agents


def step_generate_rank(agents: List[ag.Agent]) -> List[ag.Agent]:
    """
    Generate a new population according to the fitness ranking of the only 10%
    best elements.
    :param agents: list of agents.
    :return: the new agent list.
    """
    agents = sorted(agents, key=lambda x: x.fitness)
    best_agents = agents[-(len(agents) // 10):]
    best_agent = agents[-1]
    new_agents = []
    total_score = (len(best_agents) * (len(best_agents) + 1)) // 2
    for _ in range(len(agents)):
        score = rd.randint(1, total_score)
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


def heavy_mutation(agents: List[ag.Agent]) -> List[ag.Agent]:
    """
    Does 4 more mutations on 5% of the population to diversify the phenotype.
    :param agents: list of agents.
    :return: list of agents containing the heavily mutated ones.
    """
    for i in range(rd.randint(0, len(agents) // 20)):
        agent_index = rd.randint(0, len(agents) - 1)
        for j in range(4):
            agents[agent_index].mutate()
    return agents


def get_best_children(agents: List[ag.Agent]) -> List[ag.Agent]:
    """
    Use the best 10% elements of the population to generate an equal amount
    of children.
    These children replace randomly the value of others elements.
    :param agents: list of agents.
    :return: the list of agents containing generated children.
    """
    count = len(agents) // 10
    best_agents = sorted(agents, key=lambda x: x.fitness)[-count:]
    new_agents = []

    for _ in range(count):
        dad = best_agents[rd.randint(0, count - 1)]
        mum = best_agents[rd.randint(0, count - 1)]
        new = ag.Agent()
        for i in range(min(len(dad.value), len(mum.value))):
            if rd.randint(0, 1) == 0:
                new.value += dad.value[i]
            else:
                new.value += mum.value[i]
        new_agents.append(new)

    for i in range(len(new_agents)):
        agents[rd.randint(0, len(agents) - 1)] = new_agents[i]
    return agents


def step(agents: List[ag.Agent]) -> List[ag.Agent]:
    """
    Execute one step of the algorithm and print occasionally the best element.
    :param agents: list of agents.
    :return: modified list of agents.
    """
    step_run(agents)

    if VERBOSE and rd.randint(0, 50) == 0:
        print_best(agents)

    agents = step_generate_rank(agents)
    best_agent = copy.deepcopy(agents[-1])
    get_best_children(agents)
    agents = step_mutate(agents)
    agents = heavy_mutation(agents)
    agents[-1] = best_agent

    return agents


def print_agents(agents: List[ag.Agent]) -> None:
    """
    Print all the agents.
    :param agents: list of agents.
    :return: None
    """
    for a in agents:
        print(str(a))


def print_best(agents: List[ag.Agent]) -> None:
    """
    Print the agent with the best fitness.
    :param agents: list of agents.
    :return: None
    """
    best = None
    best_value = None
    for a in agents:
        if best is None or best < a.fitness:
            best = a.fitness
            best_value = a.value
    print(best, best_value)


def init(agents: List[ag.Agent]) -> None:
    """
    Randomly initialize the agents.
    :param agents: list of agents.
    :return: None.
    """
    for a in agents:
        a.set_random()


if __name__ == "__main__":

    # good password for 11608160 is XD54BLA1RE4U68
    # good password for 11603130 is XDR4PA5D3P1C08

    config("config.conf")

    seed = conf["seed"]
    STUDENT_ID = conf["student_id"]
    MAX_GEN = conf["max_iterations"]
    NB_AGENT = conf["nb_agents"]
    VERBOSE = conf["verbose"]
    ALLOW_LOOP = conf["allow_loop"]

    success = False
    agent_list = []

    while ALLOW_LOOP and not success:

        agent_list = []
        for _ in range(NB_AGENT):
            agent_list.append(ag.Agent())

        init(agent_list)

        if seed is not None:
            agent_list[-1].value = seed

        iteration = 0

        while MAX_GEN == -1 or iteration < MAX_GEN:
            if VERBOSE:
                print(iteration)
            iteration += 1
            agent_list = step(agent_list)
            if agent_list[-1].fitness >= 1.0:
                if VERBOSE:
                    print("Done")
                success = True
                break
        if not success:
            print("Time out! Limit of", MAX_GEN, "iterations reached.")
        if ALLOW_LOOP and not success:
            print("Restarting...")
    # print all agents with their fitness
    step_run(agent_list)
    print_best(agent_list)
