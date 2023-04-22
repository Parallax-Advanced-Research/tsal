# Author: Dustin Dannenhauer
# Email: dustin.dannenhauer@parallaxresearch.org

# This file is part of tsal-translator, an extension of pypddl-parser

class Equation(object):

    """
    An equation consists of an expression with one or more free variables
    """

    def __init__(self, variables=[], expression=None):
        self._variables = variables
        self._expression = expression

        if len(self._variables) == 0:
            raise Exception("ERROR in creating equation: no variables given")

    @property
    def variables(self):
        return self._variables

    @property
    def expression(self):
        return self._expression

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{} with free variables: {}".format(self._expression, self._variables)

    def __hash__(self):
        return hash(str(self))


