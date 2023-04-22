# Author: Dustin Dannenhauer
# Email: dustin.dannenhauer@parallaxresearch.org

# This file is part of tsal-translator, an extension of pypddl-parser
from tsal.translator.expression import Expression


class Event(object):
    counter = 1

    class_name = 'events'

    def __init__(self, name, params, precond, effects, duration=None, distribution=None):
        """

        :param name: name of the operator (e.g., 'pick-up')
        :param params:  list of Term objects (e.g., '?x' of type 'blocks')
        :param precond: list of Literals objects
        :param effects: list of Literals objects
        """
        self._name    = name
        self._params  = params
        self._precond = precond
        if isinstance(effects[0], list):
            self._effects = effects
        else:
            self._effects = [effects]
        self._duration = duration
        self._distribution = distribution
        self._id = Event.counter
        Event.counter += 1

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params[:]

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def precond(self):
        return self._precond[:]

    @property
    def effects(self):
        return self._effects[:]

    @property
    def effects0(self):
        return self._effects[:][0]

    @property
    def fluent_effects(self):
        retval = []
        for eff in self._effects[:][0]:
            if isinstance(eff[1], Expression):
                retval.append(eff[1])
        return retval

    @precond.setter
    def precond(self, precond):
        self._precond = precond

    @effects.setter
    def effects(self, effects):
        self._effects = effects

    @property
    def duration(self):
        return self._duration

    @property
    def distribution(self):
        return self._distribution

    def __str__(self):
        operator_str  = '{0}({1})\n'.format(self._name, ', '.join(map(str, self._params)))
        if self._duration:
            operator_str += '>> duration: {0}\n'.format(str, self._duration)
        operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self._precond)))
        if self._distribution:
            operator_str += '>> interarrival: {0}\n'.format(str(self._distribution))
        operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self._effects)))
        return operator_str

    @staticmethod
    def __det_effect_to_str(effect):
        if len(effect) > 1  and isinstance(effect[0][0],float): # No labeled effects
            if all(isinstance(x,tuple) for x in effect): # Conjunction of predicates as effects
                effect_str = '(and {})'.format(' '.join(repr(e[1]) for e in effect))
            else: # We have conditional effects
                effect_str = '(and '
                for x in effect:
                    if isinstance(x, tuple):  # Simple predicate
                        effect_str += repr(x[1])
                    else: # Conditional effect
                        effect_str += ' (when '
                        for set_of_pred in x:
                            effect_str += '(and {})'.format(' '.join(repr(y[1]) for y in set_of_pred))
                        effect_str += ')'

        elif len(effect) == 1:
            effect_str = ' '.join(repr(e[1]) for e in effect)
        elif len(effect) > 1 and not isinstance(effect[0][0], float):  # Labeled effects
            effect_str = '(' + effect[0] + ' (and ' + ' '.join(repr(pred[1]) for pred in effect[1][0]) + '))\n\t\t'
        else:
            print("Something very wrong, an effect is empty...")
        return effect_str

    def __repr__(self):
        effect_str = ''
        if len(self._effects) == 1 and len(self._effects[0]) == 0: # No labeled effects
            effect_str = 'None'
        elif len(self._effects) == 1 and isinstance(self.effects[0][0][0], float) : # No labeled effects
            effect_str = Event.__det_effect_to_str(self._effects[0])
        elif len(self._effects) > 1:
            effect_str = '(oneof {})'.format(' '.join(Event.__det_effect_to_str(x) for x in self._effects))
        elif len(self._effects) == 1 and isinstance(self.effects[0][0][0][0], str):  # Labeled effects
            effect_str = '(oneof {})'.format(' '.join(Event.__det_effect_to_str(x) for x in self._effects[0]))

        def_precond = ''
        for p in self._precond:
            if not isinstance(p,list):
                def_precond += ' ' + str(p)
            else:
                def_precond += ' (or {})'.format(' '.join(str(x) for x in p))
        operator_str = '\t(:event {name} \n' \
                        '\t\t:parameters ({param})\n'
        if self.duration:
            operator_str = operator_str + '\t\t:duration ({duration})\n'
        operator_str = operator_str + '\t\t:precondition (and {prec})\n'
        if self.distribution:
            operator_str = operator_str + '\t\t:interarrival {dist}\n'
        operator_str = operator_str + '\t\t:effect {effect}\n\t)'
        operator_str = operator_str.\
            format(name=self._name,
                   param=' '.join(repr(p) for p in self._params),
                   duration=str(self.duration),
                   prec=def_precond,
                   dist=self._distribution,
                   effect=effect_str
                   )
        return operator_str

    def __eq__(self, other):  #TODO:Add to git
        equality_params = ['name', 'params', 'precond', 'effects', 'duration', 'distribution']
        if hash(self) == hash(other):
            return True
        if type(self)!=type(other):
            return False
        for p in equality_params:
            if getattr(self, p) != getattr(other, p):
                return False
        return True

    def __hash__(self):
        return hash("e" + str(self._id))



