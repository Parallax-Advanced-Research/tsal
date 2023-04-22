import sys
import os
from tsal.translator import tsalparser
from tsal.translator.pddlToTsal import pddl_To_Tsal


class Interpreter:
    domain = None
    problem = None
    domain_file = None
    problem_file = None

    def __init__(self, domain_file=None, problem_file=None):
        if domain_file:
            domain_file_type = domain_file[-4:].lower()
            if domain_file_type == "pddl":
                domain_file = pddl_To_Tsal(domain_file, "dom")
            self.domain_file = domain_file
        if problem_file:
            problem_file_type = problem_file[-4:].lower()
            if problem_file_type == "pddl":
                problem_file = pddl_To_Tsal(problem_file, "prob")
            self.problem_file = problem_file

        self.domain = None
        self.problem = None
        self.parse()

        pass

    def parse(self):
        if self.domain_file:
            self.domain = tsalparser.TSALParser.parse(self.domain_file)
        if self.problem_file:
            self.problem = tsalparser.TSALParser.parse(self.problem_file)

    def print_domain(self):
        print(self.domain)

    def print_problem(self):
        print(self.problem)


if __name__ == '__main__':
    usage = 'python3 interpreter.py <domain> [<problem>]'
    description = 'Parse a tsal domain and problem. ' \
                  '<domain> stores a tsal domain file. ' \
                  '<problem> is optional and should contain a tsal problem.' \
                  'A problem can either be a standard planning problem or labeled planning problem (with labeled effects)'

    domain_file = "../../examples/domains/monopoly.tsal"
    problem_file = "../../examples/problems/carla_01.tsal"
    interpreter = Interpreter(domain_file=domain_file)
    interpreter.parse()
    interpreter.print_domain()
