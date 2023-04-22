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


class Process(object):

    """
    Represents an equation that changes the value of a fluent over time
    """

    def __init__(self, fluent=None, equation=None):
        self._fluent = fluent
        self._equation = equation

    @property
    def fluent(self):
        return self._fluent

    @property
    def equation(self):
        return self._equation

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "(= {} {})".format(self._fluent, self._equation)

    def __hash__(self):
        #print(hash(str(self)))
        return hash(str(self))


