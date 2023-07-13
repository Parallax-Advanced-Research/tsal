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


from tsal.translator.predicate import Predicate
from tsal.translator.term import Term
from tsal.translator.action import Action


class Domain(object):

    def __init__(self, domain_name=None, requirements=None, types=None, constants=None, predicates=None, operators=None,
                 fluents=None, derived_predicates=[], events=None, processes=None, timed_init_literals=None):
        """

        :param name: string name of the domain (e.g., blocks)
        :param requirements: list of domain requirement strings (e.g., [':strips', ':typing', ':equality'])
        :param types: dictionary from types to types ("" for non-typed types)
        :param constants: dictionary from types to list constants ("" for non-typed constants)
        :param predicates: list of Predicate objects
        :param operators: list of Action objects
        """

        self._name = domain_name.replace(":", "")
        self._requirements = requirements
        self._types = types
        if "object" not in self._types:
            self._types["object"] = []
        self._litypes = []
        [self._litypes.append(x) for x in list(types.keys()) + [x for y in types.values() for x in y] if
         x not in self._litypes]
        self._constants = constants
        self._predicates = predicates
        self._operators = operators
        self._events = events
        self._fluents = fluents
        self._derived_predicates = derived_predicates
        self._processes = processes
        self._timed_init_literals = timed_init_literals

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def requirements(self):
        return self._requirements

    @property
    def types(self):
        return self._types

    @types.setter
    def types(self, types):
        self._types = types

    @property
    def litypes(self):
        return self._litypes

    @litypes.setter
    def litypes(self, litypes):
        self._litypes = litypes

    @property
    def constants(self):
        return self._constants

    @property
    def predicates(self):
        return self._predicates

    @property
    def operators(self):
        return self._operators

    @operators.setter
    def operators(self, operators):
        self._operators = operators

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, events):
        self._events = events

    @property
    def processes(self):
        return self._processes

    @processes.setter
    def processes(self, processes):
        self._processes = processes

    @property
    def fluents(self):
        return self._fluents

    @fluents.setter
    def fluents(self, fluents):
        self._fluents = fluents

    @property
    def derivedpredicates(self):
        return self._derived_predicates

    @property
    def timed_init_literals(self):
        return self._timed_init_literals

    # TODO: out of date
    def __str__(self):
        types = []
        for x in self._types:
            types.append(x)
            types += self._types[x]
        types = list(set(types))
        domain_str = '@ Domain: {0}\n'.format(self._name)
        domain_str += '>> requirements: {0}\n'.format(', '.join(self._requirements))
        domain_str += '>> types: {0}\n'.format(', '.join([str(x) for x in types]))
        domain_str += '>> fluents: {0}\n'.format(', '.join(map(str, self._fluents)))
        domain_str += '>> predicates: {0}\n'.format(', '.join(map(str, self._predicates)))
        # domain_str += '>> timed_init_literals: {0}\n'.format(', '.join(map(str, self._timed_init_literals)))  TODO:reinstate
        domain_str += '>> processes: {0}\n'.format(', '.join(map(str, self._processes)))
        domain_str += '>> operators:\n    {0}\n'.format(
            '\n    '.join(str(op).replace('\n', '\n    ') for op in self._operators))
        domain_str += '>> events:\n    {0}\n'.format(
            '\n    '.join(str(ev).replace('\n', '\n    ') for ev in self._events))
        return domain_str

    def __repr__(self):
        types_txt = ''
        if len(self._types):  # if there are some :types defined
            types_txt = ' '.join(
                '\t\t{} - {}\n'.format(' '.join(self._types[t]), t) for t in self._types.keys() if not t == '')
        if '' in self._types.keys():
            types_txt = '\t\t{} {}\n'.format(types_txt, ' '.join(t for t in self._types['']))

        constants_txt = ''
        if len(self._constants):  # there are :constants defined
            constants_txt = ' '.join(
                '\t\t{} - {}\n'.format(' '.join([x.value for x in self._constants[t]]), t) for t in
                self._constants.keys() if not t == '')
        if '' in self._constants.keys():
            constants_txt = '\t\t{} {}\n'.format(constants_txt, ' '.join(t for t in self._constants['']))

        pddl_str = '(define (domain {domain_name})\n' \
                   '\t(:requirements {requirements})\n' \
                   '{types}' \
                   '{constants}' \
                   '\t(:fluents\n' \
                   '\t\t{fluents}\n' \
                   '\t)\n' \
                   '\t(:predicates\n' \
                   '\t\t{predicates}\n' \
                   '\t)\n' \
                   '\t(:derived\n' \
                   '\t\t{derivedpredicates}\n' \
                   '\t)\n' \
                   '\t(:processes\n' \
                   '\t\t{processes}\n' \
                   '\t)\n' \
                   '\t(:actions\n' \
                   '\t\t{actions}\n' \
                   '\t)\n' \
                   '\t(:events\n' \
                   '\t\t{events}\n' \
                   '\t)\n' \
                   ')'. \
            format(domain_name=self._name,
                   requirements=' '.join(self._requirements),
                   types='\t(:types \n{}\t)\n'.format(types_txt) if types_txt else '',
                   constants='\t(:constants \n{}\t)\n'.format(constants_txt) if constants_txt else '',
                   fluents='\n\t\t'.join(repr(fluent) for fluent in self._fluents),
                   predicates='\n\t\t'.join(repr(pred) for pred in self._predicates),
                   derivedpredicates='\n\t\t'.join(repr(dp) for dp in self._derived_predicates),
                   processes='\n\t\t'.join(repr(proc) for proc in self._processes),
                   actions='\n\t\t'.join(x for xs in [repr(act).splitlines() for act in self._operators] for x in xs),
                   events='\n\t\t'.join(x for xs in [repr(ev).splitlines() for ev in self._events] for x in xs),
                   )

        return pddl_str

    def add_type(self, type, type_type=''):
        if type_type in self._types:
            self._types[type_type].append(type)
        else:
            self._types[type_type] = [type]

    def del_type(self, type_type=''):
        if type_type in self._types:
            self._types[type_type].remove(type)

    def add_pred(self, pred):
        self._predicates.append(pred)

    # domain.add_pred('open', [('?x', 'boxes'), ('y', 'block'))
    def add_pred(self, name, args):
        args2 = []
        for a in args:
            if type(a) is tuple:  # name of variable with type
                arg = Term(name=a[0], type=a[1])
            elif type(a) is str:  # a constant value
                arg = Term(value=a[0])
            else:
                print('ERROR: something went wrong, incorrect argument for predicate {}'.format(name))
            args2.append(arg)
        self._predicates.append(Predicate(name, args2))

    # domain.del_pred('handempty', 0)
    def del_pred(self, name, arity):
        for pred in self._predicates:
            if pred.name == name and len(pred.args) == arity:
                self._predicates.remove(pred)

    def add_action(self, action):
        self._operators.append(action)

    def add_action(self, name, params, precond, effects):
        self._operators.append(Action(name, params, precond, effects))

    def get_pddl(self, version):
        print(version)
        version = str(version).replace(".","_")
        return get_attr(self, version)

    def get_pddl2_1(self):
        pass