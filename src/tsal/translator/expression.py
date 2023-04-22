# Author: Dustin Dannenhauer
# Email: dustin.dannenhauer@parallaxresearch.org

# This file is part of tsal-translator, an extension of pypddl-parser


class Expression(object):

    """
    Represents expressions as trees, where a node contains an operator, a left child and right child.
    """

    def __init__(self, value=None, operator=None, left_child=None, right_child=None):
        self._value = value
        self._operator = operator
        self._left_child = left_child
        self._right_child = right_child

        if self.value or self.value == 0:
            if self._operator or self._left_child or self._right_child is not None:
                raise Exception("ERROR in creating expression that has both a value and operators or children")
            else:
                # this is success condition for creating an expression object, do nothing
                pass

        elif self._operator and self._left_child and self._right_child is not None:
            if self._value:
                raise Exception("ERROR in creating expression that has both operators and children AND a value")
            else:
                # this is success condition for creating an expression object, do nothing
                pass
        else:
            print(type(value), operator, left_child, right_child)
            raise Exception("ERROR in creating expression, make sure only value or operator+children are present, can't be both")

    @property
    def value(self):
        return self._value

    @property
    def operator(self):
        return self._operator

    @property
    def left_child(self):
        return self._left_child

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, right_child):
        self._right_child = right_child

    def get_variables(self):
        variables = []
        if self._value:
            if isinstance(self._value, str):
                variables.append(self._value)

        if isinstance(self._left_child, Expression):
            variables += self._left_child.get_variables()

        if isinstance(self._right_child, Expression):
            variables += self._right_child.get_variables()

        return list(set(variables))  # remove duplicates

    def __repr__(self):
        if self._value or self._value == 0:
            return "{}".format(self._value)
        else:
            return "({} {} {})".format(self._operator, repr(self._left_child), repr(self._right_child))

    def __str__(self):

        if self._value or self._value == 0:
            return "{}".format(self._value)
        else:
            return "({} {} {})".format(self._operator, str(self._left_child), str(self._right_child))

    def __hash__(self):
        return hash(str(self))


