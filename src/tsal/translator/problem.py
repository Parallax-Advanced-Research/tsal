# This file is part of pypddl-parser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.

import itertools

from tsal.translator.predicate import Predicate
from tsal.translator.term import Term
from tsal.translator.fluent import Fluent
from tsal.translator.expression import Expression


class Problem(object):

    def __init__(self, problem_name=None, domain_name=None, objects=[], init=[], timed_init=[], goal=[], metric=("minimize", Fluent(name="PLAN-LENGTH"))):
        """

        :param name: string name of the planning problem (e.g., 'BLOCKS-4-1')
        :param domain: string name of the planning domain (e.g., 'blocks')
        :param objects: dictionary, from type --> object names (e.g., {'block': ['d', 'b'], 'door': ['h']})
        :param objects: list of terms instantiated in the state
        :param init: a list of Predicate objects (what is true)
        :param goal: list of Literal objects (what has to be true or false)
        """
        self._name = problem_name
        self._domain = domain_name
        self._objects = {}  # empty dictionary
        for obj in objects:
            self._objects[obj.type] = self._objects.get(obj.type, [])
            self._objects[obj.type].append(str(obj.value))
        self._init = init
        s = [x for x in self.init if isinstance(x, Predicate) and len(x.args) > 0 and x.args[0].name == 'self']
        if not s:
            print("BADLY FORMED INITS, NO SELF DEFINED")  # TODO:Raise exception
        self.self = s[0].args[1]
        self._timed_init = timed_init
        self._goal = self.set_goal(goal)
        self._metric = metric

    def set_goal(self, goal):
        goals ={'self': [], 'others': {}}
        for g in goal:
            ag = [x for x in g if isinstance(x, Expression) and x.left_child.name == "self"]
            if not ag:
                print("BADLY FORMED GOALS, NO DEFINED AGENT")  #TODO:Raise exception
            ag = ag[0].right_child.value
            if ag == self.self:
                goals['self'] = g
            else:
                goals['others'][ag] = g
        return goals

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def domain(self):
        return self._domain

    @property
    def objects(self):
        return self._objects

    @property
    def init(self):
        return self._init

    @property
    def timed_init(self):
        return self._timed_init

    @property
    def metric(self):
        return self._metric

    @property
    def goal(self):
        return self._goal

    @init.setter
    def init(self, init):
        self._init = init

    @goal.setter
    def goal(self, goal):
        self._goal = goal


    def __str__(self):
        problem_str = '@ Problem: {0}\n'.format(self._name)
        problem_str += '>> domain: {0}\n'.format(self._domain)
        problem_str += '>> objects:\n'
        for type, objects in self._objects.items():
            problem_str += '{0} -> {1}\n'.format(type, ', '.join(sorted(objects)))
        problem_str += '>> init:\n{0}\n'.format(', '.join(sorted(map(str, self._init))))
        problem_str += '>> timed-init:\n{0}\n'.format(', '.join(sorted(map(str, self._timed_init))))
        problem_str += '>> goal:\n{0}\n'.format(self._goal)
        return problem_str

    def __repr__(self):
        #a = list(self._objects.keys())[0]
        objects_txt = None
        if len(self.objects) > 0:
            if len(self._objects) > 1 or not list(self._objects.keys())[0] == None:
                objects_txt = ' '.join('{} - {}'.format(' '.join(self._objects[o]), o) for o in self._objects.keys())
            else:
                objects_txt = ' '.join(self._objects[None])

        goal_str = ''
        if not isinstance(self.goal[0], tuple): #normal goal definition
            goal_str = '\n\t\t'.join(repr(pred) for pred in self.goal)
        else: #labeled goal definition
            for g in self.goal:
                goal_str += '(' + g[0] + ' (and ' + ' '.join(repr(pred[1]) for pred in g[1][0]) + '))\n\t\t'



        pddl_str = '(define (problem {problem_name})\n' \
                   '\t(:domain {domain})\n' \
                   '\t(:objects {objects})\n' \
                   '\t(:init\n' \
                   '\t\t{init})\n' \
                   '\t(:timed-init\n' \
                   '\t\t{timed_init}\n' \
                   '\t)\n' \
                   '\t(:goal (and \n' \
                   '\t\t{goal}))\n' \
                   ')'. \
            format(problem_name=self._name,
                   domain=self._domain,
                   objects=objects_txt,
                   init='\n\t\t'.join(repr(pred) for pred in self._init),
                   timed_init='\n\t\t'.join(repr(timed_pred) for timed_pred in self._timed_init),
                   goal=goal_str
                   )

        pddl_str_cleaned = pddl_str.replace('\t(:objects None)\n','') # Delete the object definition line if there are no objects
        return pddl_str_cleaned


    def add_object(self, name_obj, type_obj):
        if type_obj in self._objects:
            self._objects[type_obj].append(name_obj)
        else:
            self._objects[type] = [name_obj]

    def add_to_init(self, pred):
        self._init.append(pred)
    def add_to_init_text(self, name, constants_args):
        """
        Adds a predicate (positive literal) to the init set
            e.g.,   problem.add_to_init('open', ['1', '2', 'c'])


        :param name: name of the predicate to add (will be converted to Predicate)
        :param constants_args: list of arguments of the predicate (will be converted into Terms)
        :return: nothing but modifies the init property
        """
        args2 = []
        for a in constants_args:
            args2.append(Term(value=a))
        self._init.append(Predicate(name, args2))



    def add_to_goal(self, literal):
        self._goal.append(literal)
    def add_to_goal_text(self, name, constants_args):
        """
        Adds a predicate (positive literal) to the goal set
            e.g.,   problem.add_to_init('open', ['1', '2', 'c'])


        :param name: name of the predicate to add (will be converted to Predicate)
        :param constants_args: list of arguments of the predicate (will be converted into Terms)
        :return: nothing but modifies the goal property
        """
        args2 = []
        for a in constants_args:
            args2.append(Term(value=a))
        self._goal.append(Predicate(name, args2))
