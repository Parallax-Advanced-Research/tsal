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


from tsal.translator.term import Term


class Fluent(object):

    class_name = 'fluents'

    def __init__(self, name, args=[], bounds=[None, None, None], typ=None):
        """
            Construct a Predicate object

        :param name: string with the name of the predicate
        :param args: list of Term objects
        """
        self._name = name
        self._args = args
        if not bounds[0]:
            bounds[0] = 0
        if not bounds[1]:
            bounds[1] = 100
        if not bounds[2]:
            bounds[2] = 2
        self._bounds = bounds
        self._min = bounds[0]
        self._max = bounds[1]
        self._precision = bounds[2]
        self._hasBounds = False
        self._type = typ
        if self._min and self._max and self._precision:
            self._hasBounds = True

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args[:]

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def bounds(self):
        return self._bounds[:]

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def arity(self):
        return len(self._args)

    def __str__(self):
        if self._name == '=':
            return '{0} = {1}'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return '({0})'.format(self._name)
        else:
            return '({0} {1})'.format(self._name, ' '.join(map(str, self._args)))

    # def __repr__(self):
    #     return "Predicate(name = %s, args = %s)" % (self._name, self._args)


    def __repr__(self):
        if self._name == '=':
            return '(= {0} {1})'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            if self.type:
                return '({0}) - {1}'.format(self._name, self._type)
            else:
                return '({0})'.format(self._name)

        else:
            if self.type:
                return '({0} {1}) - {2}'.format(self._name, ' '.join(map(str, self._args)), self._type)
            else:
                return '({0} {1})'.format(self._name, ' '.join(map(str, self._args)))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.name == other.name \
                and self.args == other.args:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.name,str(self.args)))

