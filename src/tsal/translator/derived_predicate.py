# Author: Dustin Dannenhauer
# Email: dustin.dannenhauer@parallaxresearch.org

# This file is part of tsal-translator, an extension of pypddl-parser


class DerivedPredicate(object):

    class_name = 'derivedpredicates'

    def __init__(self, name, args=[], parent_predicates=[]):
        """
            Construct a Predicate object

        :param name: string with the name of the predicate
        :param args: list of Term objects
        :param parent_predicates: list of DerivedPredicate or Predicate objects
        """

        self._name = name
        self._args = args
        self._parent_predicates = parent_predicates

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args[:]

    @property
    def arity(self):
        return len(self._args)

    def parent_predicates(self):
        return self._parent_predicates

    def __str__(self):
        if self._name == '=':
            return '{0} = {1}'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return self._name
        else:
            return '{0}({1}) derived from (and {2})'.format(self._name, ', '.join(map(str, self._args)), ', '.join(map(str, self._parent_predicates)))

    # def __repr__(self):
    #     return "Predicate(name = %s, args = %s)" % (self._name, self._args)

    def __repr__(self):
        if self._name == '=':
            return '(= {0} {1})'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return '({})'.format(self._name)
        else:
            return '({0} {1}) (and {2})'.format(self._name, ' '.join(map(str, self._args)), ' '.join(map(str, self._parent_predicates)))

    def __eq__(self, other):
        if self.name == other.name \
                and self.args == other.args:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.name,str(self.args)))