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


class Term(object):
    class_name = 'litypes'

    def __init__(self, **kwargs):
        """
            Construct a Term object

            for variables ?x name is '?x'
            for typed variables like ?x - block, name is '?x' and type is 'block'
            for constants like 'e' in '(open e)', name and type are None and value is 'e'


        :param kwargs: up to three kwarg arguments that are all strings:
            name = the name of the term if variable (for example '?x' or 'table')
            type = the type of the term (for example 'blocks')
            value = the value of the term if constant
        """
        self._name  = kwargs.get('name',  None)
        self._type  = kwargs.get('type',  None)
        self._value = kwargs.get('value', None)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    def is_variable(self):
        return self._name is not None

    def is_typed(self):
        return self._type is not None

    def is_constant(self):
        return self._value is not None

    def lower(self):  #
        '''
        Allows for using .lower() in term equality, so that string name case doesn't matter.
        A term name can be a term though, so in those cases, just return the term
        '''
        return self

    @classmethod
    def variable(cls, name, type=None):
        return Term(name=name, type=type)

    @classmethod
    def constant(cls, value, type=None):
        return Term(value=value, type=type)

    def __str__(self):
        if self.is_variable() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_variable():
            return '{0}'.format(self._name)
        if self.is_constant() and self.is_typed():
            return '{0}'.format(self._value)
        if self.is_constant():
            return '{0}'.format(self._value)

    def __repr__(self):
        if self.is_variable() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_variable():
            return '{0}'.format(self._name)
        if self.is_constant() and self.is_typed():
            return '{0} - {1}'.format(self._value, self._type)
        if self.is_constant():
            return '{0}'.format(self._value)

    def __eq__(self, other):
        if not other:
            return False
        if self._type == other._type:
            if type(self._name) == type(other._name):
                if self._name:
                    if self._name.lower() == other._name.lower():
                        return True
                else:
                    if self._value == other._value:
                        return True
        return False

    def __hash__(self): # TODO: add to git
        return hash((self.name, self.type, self.value))
