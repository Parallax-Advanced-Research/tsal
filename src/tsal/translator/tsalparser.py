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

# Extended by Dustin Dannenhauer and Noah Reifsnyder to support TSAL

import sys
from tsal.ply import lex, yacc
from tsal.translator.term import Term
from tsal.translator.literal import Literal
from tsal.translator.predicate import Predicate
from tsal.translator.action import Action
from tsal.translator.event import Event
from tsal.translator.domain import Domain
from tsal.translator.problem import Problem
from tsal.translator.fluent import Fluent
from tsal.translator.derived_predicate import DerivedPredicate
from tsal.translator.expression import Expression
from tsal.translator.process import Process
from tsal.translator.equation import Equation
from tsal.translator.timedliteral import TimedLiteral
from tsal.translator.distribution import FrequencyDistribution

Debug = False
# turn on for debugging
# logging.basicConfig(
#     level=logging.DEBUG,  # change this to increase or decrease debug messages
#     filename="parselog.txt",
#     filemode="w",
#     format="%(filename)10s:%(lineno)4d:%(message)s"
# )
# log = logging.getLogger()

tokens = (
    'NAME',
    'VARIABLE',
    'PROBABILITY',
    'DECIMAL',
    'NEG_INTEGER',
    'POS_INTEGER',
    'PLUS',
    # 'MINUS',  # HYPHEN is used instead
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'HYPHEN',
    'EQUALS',
    'NEQ',
    'GT',
    'GTEQ',
    'LT',
    'LTEQ',
    'MOD',
    'AT_KEY',
    'DEFINE_KEY',
    'DOMAIN_KEY',
    'REQUIREMENTS_KEY',
    'TYPES_KEY',
    'CONSTANTS_KEY',
    'PREDICATES_KEY',
    'DERIVED_KEY',
    'DERIVED_PREDICATES_KEY',
    'ACTION_KEY',
    'ACTIONS_KEY',
    'EVENT_KEY',
    'EVENTS_KEY',
    'PARAMETERS_KEY',
    'PRECONDITION_KEY',
    'EFFECT_KEY',
    'AND_KEY',
    'NOT_KEY',
    'ONEOF_KEY',
    'PROBABILISTIC_KEY',
    'PROBLEM_KEY',
    'OBJECTS_KEY',
    'INIT_KEY',
    'GOAL_KEY',
    'METRIC_KEY',
    'FORALL_KEY',
    'WHEN_KEY',
    'OR_KEY',
    'FLUENTS_KEY',
    'BOUNDS_KEY',
    'DURATION_KEY',
    'PROCESSES_KEY',
    'TIMED_INIT_KEY',
    'INTERARRIVAL_KEY',
)

t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_HYPHEN = r'\-'
t_EQUALS = r'='
t_NEQ = r'!='
t_GT = r'>'
t_GTEQ = r'>='
t_LTEQ = r'<='
t_LT = r'<'
t_MOD = r'%'


t_ignore = ' \t'

reserved = {
    'define': 'DEFINE_KEY',
    'domain': 'DOMAIN_KEY',
    ':requirements': 'REQUIREMENTS_KEY',
    ':types': 'TYPES_KEY',
    ':predicates': 'PREDICATES_KEY',
    ':action': 'ACTION_KEY',
    ':actions': 'ACTIONS_KEY',
    ':event': 'EVENT_KEY',
    ':events': 'EVENTS_KEY',
    ':fluents': 'FLUENTS_KEY',
    ':bounds': 'BOUNDS_KEY',
    ':parameters': 'PARAMETERS_KEY',
    ':precondition': 'PRECONDITION_KEY',
    ':effect': 'EFFECT_KEY',
    'and': 'AND_KEY',
    'not': 'NOT_KEY',
    'oneof': 'ONEOF_KEY',
    'forall': 'FORALL_KEY',
    'when': 'WHEN_KEY',
    'or': 'OR_KEY',
    'probabilistic': 'PROBABILISTIC_KEY',
    'problem': 'PROBLEM_KEY',
    ':domain': 'DOMAIN_KEY',
    ':objects': 'OBJECTS_KEY',
    ':constants': 'CONSTANTS_KEY',
    ':init': 'INIT_KEY',
    ':timed-init': 'TIMED_INIT_KEY',
    ':goal': 'GOAL_KEY',
    ':metric': 'METRIC_KEY',
    ':derived-predicates': 'DERIVED_PREDICATES_KEY',
    ':derived': 'DERIVED_KEY',
    ':duration': 'DURATION_KEY',
    ':processes': 'PROCESSES_KEY',
    ':at': 'AT_KEY',
    ':interarrival': 'INTERARRIVAL_KEY',
}


def t_KEYWORD(t):
    r':?[a-zA-z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'NAME')
    return t


def t_NAME(t):
    r'[a-zA-z_][a-zA-Z_0-9\-]*'
    return t


def t_VARIABLE(t):
    r'\??[a-zA-z_][a-zA-Z_0-9\-]*'
    return t


def t_PROBABILITY(t):
    r'[0-1]\.\d+'
    t.value = float(t.value)
    return t


def t_DECIMAL(t):
    r'[+-]?\d*\.\d+?'
    t.value = float(t.value)
    return t

def t_NEG_INTEGER(t):
    r'[-]\d+'
    t.value = int(t.value)
    return t

def t_POS_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)


def t_error(t):
    print("Error: illegal character '{0}'".format(t.value[0]))
    t.lexer.skip(1)


# build the lexer
lex.lex(debug=Debug)
#lex.lex(debug=True, debuglog=log, )  # turn this on to debug


def p_tsal(p):
    '''tsal : domain
            | problem
            | domain problem'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = (p[1], p[2])


###################################################3
# Rules for PLANNING DOMAIN
###################################################3
#
#               |
#def p_domain(p):
#    '''domain : LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_def predicates_def derived_predicates_def processes_def actions_def events_def RPAREN '''
#    p[0] = Domain(name=p[3], requirements=[4], types=p[5][1], constants=p[6][1], predicates=p[8], operators=p[11],
#                  fluents=p[7], derived_predicates=p[9], events=p[12], processes=p[10])
start = 'tsal'
def p_domain(p):
    '''domain : LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def derived_predicates_def processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def derived_predicates_def processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def  processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def derived_predicates_def  actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def derived_predicates_def  actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def actions_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def derived_predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def derived_predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def  processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def derived_predicates_def  actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def fluents_predicates_def derived_predicates_def  actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def fluents_predicates_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def actions_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def derived_predicates_def processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def derived_predicates_def processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def  processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def processes_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def derived_predicates_def  actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def derived_predicates_def  actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def  actions_def events_def RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def derived_predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def derived_predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def processes_def actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def derived_predicates_def  actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def predicates_def derived_predicates_def  actions_def  RPAREN
              | LPAREN DEFINE_KEY domain_def requirements_def types_def constants_def predicates_def actions_def  RPAREN'''
    global new_predicates
    global new_events
    kwargs = {'domain_name': None,
                   'requirements': [],
                   'types': {},
                   'constants': {},
                   'predicates': new_predicates,
                   'fluents': [],
                   'operators': [],
                   'events': new_events,
                   'derived_predicates': [],
                   'processes': []}
    for i in p:
        if i and type(i) == list:
            for j in i:
                if j and type(j) == tuple:
                    kwargs[j[0]] = kwargs[j[0]] + j[1]
        if i and type(i) == tuple:
            kwargs[i[0]] = i[1]
    p[0] = Domain(**kwargs)
    pass

def p_domain_def(p):
    '''domain_def : LPAREN DOMAIN_KEY NAME RPAREN'''
    p[0] = ('domain_name', p[3])

def p_requirements_def(p):
    '''requirements_def : LPAREN REQUIREMENTS_KEY requirements_lst RPAREN
                        | LPAREN REQUIREMENTS_KEY RPAREN'''
    if len(p) == 4:
        p[0] = ("requirements", [])
    else:
        p[0] = ("requirements", p[3])

def p_requirements_lst(p):
    '''requirements_lst :  requirement_def requirements_lst
                        |  requirement_def'''
    if len(p) == 3:
        p[0] = p[2] + [p[1]]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_requirement_def(p):
    '''requirement_def : NAME'''
    p[0] = p[1]

def p_types_def(p):
    '''types_def : LPAREN TYPES_KEY typed_names_lst RPAREN'''
    p[0] = ("types", p[3])


def p_constants_def(p):
    '''constants_def : LPAREN CONSTANTS_KEY typed_names_lst RPAREN
                     | LPAREN CONSTANTS_KEY RPAREN'''

    if len(p) == 5:
        constants = {}
        for key in p[3]:
            constants[key] = []
            for val in p[3][key]:
                constants[key].append(Term(value=val, type=key))
        p[0] = ("constants", constants)
    else:
        p[0] = ("constants", {})


# Used for processing :types and :constants
#   list of names, possibly typed using hyphen -
def p_typed_names_lst(p):
    '''typed_names_lst : names_lst HYPHEN type typed_names_lst
                       | names_lst HYPHEN type
                       | names_lst'''

    if len(p) == 2:
        p[0] = dict({'': p[1]})
    elif len(p) == 4:
        p[0] = dict({p[3]: p[1]})
    elif len(p) == 5:
        if p[3] in p[4]:
            p[4][p[3]] = p[4][p[3]] + p[1]
        else:
            p[4][p[3]] = p[1]
        p[0] = p[4]  # p[4] is already a dictionary, add one entry more

def p_fluents_predicates_def(p):
    '''fluents_predicates_def : fluents_def predicates_def
                              | predicates_def fluents_def'''
    p[0] = p[1:]

def p_fluents_def(p):
    '''fluents_def : LPAREN FLUENTS_KEY fluent_def_lst RPAREN'''
    # todo - allow fluents def to be empty
    p[0] = ("fluents", p[3])


def p_fluent_def_lst(p):
    '''fluent_def_lst : fluent_def fluent_def_lst
                      | fluent_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_fluent_def(p):
    '''fluent_def : LPAREN NAME typed_variables_lst RPAREN
                  | LPAREN NAME variables_lst RPAREN
                  | LPAREN NAME RPAREN
                  | fluent_def HYPHEN type
                  |  LPAREN NAME typed_variables_lst bounds_def RPAREN'''

    if len(p) == 4:
        if isinstance(p[1], Fluent):
            p[0] = Fluent(name=p[1].name, args=p[1].args, bounds=p[1].bounds, typ=p[3])
        else:
            p[0] = Fluent(name=p[2])
    elif len(p) == 5:
        p[0] = Fluent(name=p[2], args=p[3])
    elif len(p) == 6:
        p[0] = Fluent(name=p[2], args=p[3], bounds=list(p[4]))

def p_bounds_def(p):
    '''bounds_def : BOUNDS_KEY num num POS_INTEGER'''
    p[0] = (p[2], p[3], p[4])

def p_num(p):
    '''num : POS_INTEGER
            | NEG_INTEGER'''
    p[0] = p[1]

def p_predicates_def(p):
    '''predicates_def : LPAREN PREDICATES_KEY predicate_def_lst RPAREN'''
    p[0] = ("predicates", p[3])


def p_predicate_def_lst(p):
    '''predicate_def_lst : predicate_def predicate_def_lst
                         | predicate_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_predicate_def(p):
    '''predicate_def : LPAREN NAME typed_variables_lst RPAREN
                     | LPAREN NAME variables_lst RPAREN
                     | LPAREN NAME RPAREN'''

    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])


def p_derived_predicates_def(p):
    '''derived_predicates_def : LPAREN DERIVED_PREDICATES_KEY derived_def_lst RPAREN
                               | LPAREN DERIVED_PREDICATES_KEY RPAREN'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 4:
        p[0] = []

def p_derived_def_lst(p):
    '''derived_def_lst :
                       | derived_def derived_def_lst
                       | derived_def'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_derived_def(p):
    '''derived_def : LPAREN DERIVED_KEY predicate_def derived_def_body RPAREN
                    | LPAREN DERIVED_KEY fluent_def derived_def_body RPAREN'''

    p[0] = DerivedPredicate(p[3].name, p[3].args, p[4])


def p_derived_def_body(p):
    '''derived_def_body : LPAREN AND_KEY fluent_predicate_def_lst RPAREN'''


    p[0] = p[3]

def p_fluent_predicate_def_lst(p):
    '''fluent_predicate_def_lst :
                                | expression fluent_predicate_def_lst
                                | literal fluent_predicate_def_lst'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_processes_def(p):
    '''processes_def : LPAREN PROCESSES_KEY processes_def_lst RPAREN'''
    p[0] = p[3]


def p_processes_def_lst(p):
    '''processes_def_lst :
                         | process_def processes_def_lst
                         | process_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_process_def(p):
    '''process_def : LPAREN EQUALS NAME expression RPAREN'''

    expression = p[4]
    p[0] = Process(fluent=p[3], equation=Equation(expression=expression, variables=expression.get_variables()))


def p_actions_def(p):
    '''actions_def : LPAREN ACTIONS_KEY action_def_lst RPAREN'''
    p[0] = ("operators", p[3])


def p_action_def_lst(p):
    '''action_def_lst :
                      | action_def action_def_lst
                      | action_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

forall_counter = 0
new_predicates = []
new_events = []
def p_action_def(p):
    '''action_def : LPAREN ACTION_KEY NAME parameters_def action_def_body RPAREN
                  | LPAREN ACTION_KEY NAME parameters_def duration_def action_def_body RPAREN'''
    global forall_counter
    raw_eff_lst = []
    eff_lst = []
    if len(p) == 7:
        raw_eff_lst = p[5][1]
    elif len(p) == 8:
        raw_eff_lst = p[6][1]
    for eff in raw_eff_lst:
        if eff[0] == 'FORALL':
            params = []
            params_l = []
            for pred in eff[2][1]:
                if isinstance(pred, Literal):
                    for t in pred.predicate.args:
                        t_l = [x for x in [x for x in p[4] if x not in eff[1]] if x.name == t and x not in params] #not full params
                        t = [x for x in p[4] + eff[1] if x.name == t and x not in params]
                        if t:
                            params.append(t[0])
                        if t_l:
                            params_l.append(t_l[0])
                elif isinstance(pred, Expression):
                    l_c = pred.left_child.value
                    r_c = pred.right_child.value
                    params_l = params_l + [x for x in [x for x in p[4] if x not in eff[1]] if (x.name.name == l_c or x.name.name == r_c) and x not in params_l] #not full params
                    params = params + [x for x in p[4] + eff[1] if (x.name.name == l_c or x.name.name == r_c) and x not in params]
            pred_args = None
            for i in range(len(eff[2][2])):
                eff[2][2][i] = (1.0, eff[2][2][i])
            new_pred = Predicate(name="FORALL"+str(forall_counter), args=params_l)
            eff_pred = Predicate(name=new_pred.name, args=[x.name for x in new_pred.args])
            new_event = Event(name=str(forall_counter)+"FORALL", params=params, precond=eff[2][1] + [Literal(eff_pred, True)], effects=[eff[2][2] + [(1.0, Literal(eff_pred, False))]])
            forall_counter = forall_counter + 1
            new_predicates.append(new_pred)
            new_events.append(new_event)
            eff_lst.append((1.0, Literal(Predicate(name=new_pred.name, args=[x.name for x in new_pred.args]), True)))
        elif eff[0] == 'WHEN':
            pass
        else:
            eff_lst.append(eff)
    if len(p) == 7:  # no dura
        p[0] = Action(p[3], p[4], p[5][0], [eff_lst])
    elif len(p) == 8:  # duration given
        p[0] = Action(p[3], p[4], p[6][0], [eff_lst], duration=p[5])


def p_event_def(p):
    '''event_def : LPAREN EVENT_KEY NAME parameters_def event_def_body RPAREN
                 | LPAREN EVENT_KEY NAME parameters_def duration_def event_def_body RPAREN'''
    if len(p) == 7:  # no duration
        p[0] = Event(p[3], p[4], p[5][0], p[5][1])
    elif len(p) == 8:  # duration given
        if len(p[6]) == 2:  # no freq. dist. given
            p[0] = Event(p[3], p[4], p[6][0], p[6][1], duration=p[5])
        elif len(p[6]) == 3:  # freq. dist. given
            p[0] = Event(p[3], p[4], p[6][0], p[6][1], duration=p[5], distribution=p[6][2])


def p_events_def(p):
    '''events_def : LPAREN EVENTS_KEY event_def_lst RPAREN'''
    p[0] = ("events", p[3])


def p_event_def_lst(p):
    '''event_def_lst :
                     | event_def event_def_lst
                     | event_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_parameters_def(p):
    '''parameters_def : PARAMETERS_KEY LPAREN typed_variables_lst RPAREN
                      | PARAMETERS_KEY LPAREN variables_lst RPAREN
                      | PARAMETERS_KEY LPAREN RPAREN'''
    if len(p) == 4:
        p[0] = []
    elif len(p) == 5:
        p[0] = p[3]


def p_action_def_body(p):
    '''action_def_body : precond_def effects_def'''
    p[0] = (p[1], p[2])


def p_event_def_body(p):
    '''event_def_body : precond_def effects_def
                      | precond_def frequency_def effects_def'''
    if len(p) == 3:  # no frequency distribution given
        p[0] = (p[1], p[2])
    elif len(p) == 4:  # frequency distibution given
        p[0] = (p[1], p[3], p[2])  # put freq. dist. at the end


def p_precond_def(p):
    '''precond_def : PRECONDITION_KEY LPAREN AND_KEY literals_lst RPAREN
                   | PRECONDITION_KEY literal
                   | PRECONDITION_KEY expression
                   | PRECONDITION_KEY LPAREN RPAREN'''
    if len(p) == 3:
        p[0] = [p[2]]
    elif len(p) == 6:
        p[0] = p[4]
    elif len(p) == 4:
        p[0] = []


def p_effects_def(p):
    '''effects_def : EFFECT_KEY effect_body
                    | EFFECT_KEY forall
                    | EFFECT_KEY when_body
                    | EFFECT_KEY LPAREN AND_KEY forall_body RPAREN '''
    if len(p) == 3:
        if isinstance(p[2], list):
            p[0] = p[2]
        else:
            p[0] = [p[2]]
    elif len(p) == 6:
        p[0] = p[4]


def p_effect_body(p):
    '''effect_body : LPAREN RPAREN
                    | LPAREN NAME unlabeled_effect RPAREN
                    | effect_body LPAREN NAME unlabeled_effect RPAREN
                    | unlabeled_effect'''
    if len(p) == 5:
        p[0] = [(p[2], p[3])]
    elif len(p) == 6:
        p[0] = p[1] + [(p[3], p[4])]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = []

def p_forall_body(p):
    '''forall_body : forall forall_body
                   | forall
                   | effect forall_body
                   | effect'''
    if len(p) == 3:
        p[0] = p[2] + [p[1]]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_when_body(p):
    '''when_body : LPAREN WHEN_KEY when_pre when_eff RPAREN'''
    p[0] = ('WHEN', p[3], p[4])


def p_forall(p):
    '''forall : LPAREN FORALL_KEY LPAREN typed_variables_lst RPAREN when_body RPAREN'''
    p[0] = ('FORALL', p[4], p[6])

def p_when_pre(p):
    '''when_pre : LPAREN AND_KEY literals_lst RPAREN
                | literal'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = [p[1]]

def p_when_eff(p):
    '''when_eff : LPAREN AND_KEY literals_lst RPAREN
                | literal'''

    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_frequency_def(p):
    '''frequency_def : INTERARRIVAL_KEY LPAREN NAME NAME DECIMAL RPAREN
                     | INTERARRIVAL_KEY LPAREN RPAREN'''
    if len(p) == 6:
        p[0] = FrequencyDistribution(name=p[3], qualifier=p[4], value=p[5])
    elif len(p) == 4:
        p[0] = None

def p_unlabeled_effect(p):
    '''unlabeled_effect : LPAREN ONEOF_KEY effect_body RPAREN
                        | deterministic_effect unlabeled_effect
                        | deterministic_effect'''
    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    #TODO:This is where double nested effects occur. Check with dustin

def p_deterministic_effect(p):
    '''deterministic_effect : LPAREN AND_KEY effects_lst RPAREN
                            | effects_lst'''
    if len(p) == 2:
        p[0] = p[1]  # effect is just on literal, no AND
    elif len(p) == 5:
        p[0] = p[3]  # effect description has an AND

def p_when_effects(p):
    '''when_effects : when_if when_then '''
    p[0] = [p[1],
            p[2]]  # it is a list, with the element in [0] being the conditions and the element in [1] being the effects


def p_when_if(p):
    '''when_if : simple_effect
                | LPAREN AND_KEY simple_effects_lst RPAREN'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        p[0] = p[3]


def p_when_then(p):
    '''when_then : simple_effect
                 | LPAREN AND_KEY simple_effects_lst RPAREN'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 5:
        p[0] = p[3]


def p_effects_lst(p):
    '''effects_lst :
                   | effect effects_lst
                   | effect'''

    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_simple_effects_lst(p):
    '''simple_effects_lst : simple_effect simple_effects_lst
                          | simple_effect'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

def p_effect(p):
    '''effect : literal
              | expression
              | LPAREN PROBABILISTIC_KEY PROBABILITY literal RPAREN
              | LPAREN WHEN_KEY when_effects RPAREN'''
    if len(p) == 2:
        p[0] = (1.0, p[1])
    elif len(p) == 6:
        p[0] = (p[3], p[4])
    elif len(p) == 5:
        p[0] = p[3]

def p_simple_effect(p):
    '''simple_effect : literal'''
    if len(p) == 2:
        p[0] = (1.0, p[1])


def p_duration_def(p):
    '''duration_def : DURATION_KEY LPAREN expression RPAREN
                    | DURATION_KEY LPAREN RPAREN'''

    if len(p) == 5:
        p[0] = p[3]
    elif len(p) == 4:
        p[0] = None

precedence = (
    ('left', 'PLUS', 'HYPHEN'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_expression_body(p):
    '''expression_body : fluent_def
                       | expression'''
    p[0] = p[1]

def p_expression_body_list(p):
    '''expression_body_list : expression_body expression_body'''
    p[0] = [p[1], p[2]]

def p_expression(p):
    # ADDED FLUENT
    '''expression : PLUS expression_body_list
                  | HYPHEN expression_body_list
                  | TIMES expression_body_list
                  | DIVIDE expression_body_list
                  | GT expression_body_list
                  | GTEQ expression_body_list
                  | LT expression_body_list
                  | LTEQ expression_body_list
                  | EQUALS expression_body_list
                  | NEQ expression_body_list
                  | MOD expression_body_list
                  | LPAREN expression RPAREN
                  | DECIMAL
                  | PROBABILITY
                  | VARIABLE
                  | POS_INTEGER
                  | NEG_INTEGER
                  | NAME'''

    if len(p) == 3:
        p[0] = Expression(value=None, operator=p[1], left_child=p[2][0], right_child=p[2][1])
    elif len(p) == 4:
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = Expression(value=p[1])


def p_literals_lst(p):
    # ADDED EXPRESSION
    '''literals_lst : literal literals_lst
                    | expression literals_lst
                    | literal
                    | expression
                    | or_literal literals_lst
                    | or_literal'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_or_literal(p):
    '''or_literal : LPAREN OR_KEY literals_lst RPAREN'''

    if len(p) == 5:
        p[0] = p[3]


def p_literal(p):
    '''literal : LPAREN NOT_KEY predicate RPAREN
               | predicate'''
    if len(p) == 2:
        p[0] = Literal.positive(p[1])
    elif len(p) == 5:
        p[0] = Literal.negative(p[3])


def p_ground_predicates_lst(p):
    '''ground_predicates_lst : ground_predicate ground_predicates_lst
                             | ground_predicate'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_ground_predicate(p):
    '''ground_predicate : LPAREN NAME constants_lst RPAREN
                        | LPAREN NAME RPAREN
                        | ground_fluent'''
    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])
    else:
        p[0] = p[1]



def p_ground_fluent(p):
    '''ground_fluent : LPAREN EQUALS ground_fluent_def NAME RPAREN
                     | LPAREN EQUALS ground_fluent_def POS_INTEGER RPAREN
                     | LPAREN EQUALS ground_fluent_def NEG_INTEGER RPAREN'''

    p[0] = Predicate(p[2], [p[3], p[4]])

def p_ground_fluent_def(p):
    '''ground_fluent_def : LPAREN NAME constants_lst RPAREN
                         | LPAREN NAME RPAREN'''
    if len(p) == 5:
        p[0] = Fluent(p[2], p[3])
    elif len(p) == 4:
        p[0] = Fluent(p[2])

def p_predicate(p):
    '''predicate : LPAREN NAME variables_lst RPAREN
                 | LPAREN EQUALS VARIABLE VARIABLE RPAREN
                 | LPAREN NAME RPAREN
                 | LPAREN NAME constants_lst RPAREN'''

    if len(p) == 4:
        p[0] = Predicate(p[2])
    elif len(p) == 5:
        p[0] = Predicate(p[2], p[3])
    elif len(p) == 6:
        p[0] = Predicate('=', [p[3], p[4]])




def p_typed_constants_lst(p):
    '''typed_constants_lst : constants_lst HYPHEN type typed_constants_lst
                           | constants_lst HYPHEN type'''
    if len(p) == 4:
        p[0] = [Term.constant(value, p[3]) for value in p[1]]
    elif len(p) == 5:
        p[0] = [Term.constant(value, p[3]) for value in p[1]] + p[4]


def p_typed_variables_lst(p):
    '''typed_variables_lst : variables_lst HYPHEN type typed_variables_lst
                           | variables_lst HYPHEN type'''
    if len(p) == 4:
        p[0] = [Term.variable(name, p[3]) for name in p[1]]
    elif len(p) == 5:
        p[0] = [Term.variable(name, p[3]) for name in p[1]] + p[4]


def p_constants_lst(p):
    '''constants_lst : constant constants_lst
                     | constant'''
    if len(p) == 2:
        p[0] = [Term.constant(p[1])]
    elif len(p) == 3:
        p[0] = [Term.constant(p[1])] + p[2]


def p_variables_lst(p):
    '''variables_lst : variable variables_lst
                     | variable
                     | NAME
                     | NAME variables_lst'''
    if len(p) == 2:
        p[0] = [Term.variable(p[1])]
    elif len(p) == 3:
        p[0] = [Term.variable(p[1])] + p[2]


def p_names_lst(p):
    '''names_lst : NAME names_lst
                 | NAME'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]


def p_type(p):
    '''type : NAME'''
    p[0] = p[1]


def p_constant(p):
    '''constant : NAME
                | POS_INTEGER
                | NEG_INTEGER'''
    p[0] = p[1]


def p_variable(p):
    '''variable : VARIABLE'''
    p[0] = p[1]


###################################################3
# Rules for PLANNING PROBLEM
###################################################3
def p_problem(p):
    '''problem : plan_problem'''
    p[0] = p[1]


def p_plan_problem(p):
    '''plan_problem : LPAREN DEFINE_KEY plan_problem_def domain_def objects_def init_def timed_inits_def goal_def metric_def RPAREN
                    | LPAREN DEFINE_KEY plan_problem_def domain_def objects_def init_def goal_def metric_def RPAREN
                    | LPAREN DEFINE_KEY plan_problem_def domain_def objects_def init_def timed_inits_def goal_def  RPAREN
                    | LPAREN DEFINE_KEY plan_problem_def domain_def objects_def init_def goal_def  RPAREN'''

    kwargs = {'problem_name': None,
              'domain_name': None,
              'objects': [],
              'init': [],
              'timed_init': [],
              'goal': [],
              'metric': ("minimize", Fluent(name="plan-length"))}  # default metric is to minimize plan length
    for i in p:
        if i and type(i)==tuple:
            kwargs[i[0]] = i[1]
    p[0] = Problem(**kwargs)


def p_plan_problem_def(p):
    '''plan_problem_def : LPAREN PROBLEM_KEY NAME RPAREN'''
    p[0] = ('problem_name', p[3])


def p_objects_def(p):
    '''objects_def : LPAREN OBJECTS_KEY typed_constants_lst RPAREN
                   | LPAREN OBJECTS_KEY constants_lst RPAREN'''
    p[0] = ('objects', p[3])


def p_init_def(p):
    '''init_def : LPAREN INIT_KEY LPAREN AND_KEY ground_predicates_lst RPAREN RPAREN
                | LPAREN INIT_KEY ground_predicates_lst RPAREN
                | LPAREN INIT_KEY RPAREN'''

    if len(p) == 4:
        p[0] = []
    elif len(p) == 5:
        p[0] = p[3]
    elif len(p) == 8:
        p[0] = p[5]
    p[0] = ('init', p[0])


def p_timed_inits_def(p):
    '''timed_inits_def : LPAREN TIMED_INIT_KEY timed_init_lst RPAREN'''
    p[0] = ('timed_init', p[3])


def p_timed_init_lst(p):
    '''timed_init_lst :
                      | timed_init_def timed_init_lst
                      | timed_init_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_timed_init_def(p):
    '''timed_init_def : LPAREN AT_KEY DECIMAL literal RPAREN'''
    # todo add a check on time being positive as part of error checking
    time = p[3]
    p[0] = TimedLiteral(predicate=p[4].predicate, positive=p[4].positive, time=time)


def p_goal_body_def(p):
    '''goal_body_def : LPAREN AND_KEY literals_lst RPAREN'''
    p[0] = p[3]

def p_goal_body_def_lst(p):
    '''goal_body_def_lst : goal_body_def goal_body_def_lst
                         | goal_body_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
def p_goal_def(p):
    '''goal_def : LPAREN GOAL_KEY goal_body_def RPAREN
                | LPAREN GOAL_KEY literal RPAREN
                | LPAREN GOAL_KEY LPAREN ONEOF_KEY effect_body RPAREN RPAREN
                | LPAREN GOAL_KEY LPAREN OR_KEY goal_body_def_lst RPAREN RPAREN'''
    if len(p) == 8:
        p[0] = p[5]
    elif len(p) == 5:
        if not isinstance(p[3], list):
            p[0] = [p[3]]
        else:
            p[0] = p[3]
    elif len(p) == 14:
        p[0] = (p[6], p[9])
    p[0] = ('goal', p[0])

def p_metric_def(p):
    '''metric_def : LPAREN METRIC_KEY NAME fluent_def RPAREN''' #TODO: Decide if wanted in tsal, thinking no
    if p[3] == 'minimize':
        p[0] = ("minimize", p[4])
    elif p[3] == 'maximize':
        p[0] = ("maximize", p[4])
    else:
        p_error(p)
    p[0] = ('metric', p[0])

def p_error(p):
    print("Error: syntax error when parsing '{}'".format(p))


# build parser
yacc.yacc(debug=Debug)
#yacc.yacc(debug=True, debuglog=log)  # turn on for debugging


class TSALParser(object):

    @classmethod
    def parse(cls, filename):
        data = cls.__read_input(filename)
        return yacc.parse(data, debug=Debug, tracking=True)

    @classmethod
    def __read_input(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = ''
            for line in file:
                line = line.rstrip().lower()
                line = cls.__strip_comments(line)
                data += '\n' + line
        return data

    @classmethod
    def __strip_comments(cls, line):
        pos = line.find(';')
        if pos != -1:
            line = line[:pos]
        return line
