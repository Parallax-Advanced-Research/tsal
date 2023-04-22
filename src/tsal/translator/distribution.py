# Author: Dustin Dannenhauer
# Email: dustin.dannenhauer@parallaxresearch.org

# This file is part of tsal-translator, an extension of pypddl-parser

class FrequencyDistribution(object):

    """
    An frequency distribution consists of a distribution type and a number of parameters, for example:

       - (poisson frequency 5)
       - (exponential frequency 5)
       - (exponential mean 5)

    Generally, the result of the frequency distribution refers to the interarrival time of the event occurring.
    """

    def __init__(self, name=None, qualifier=None, value=None, additional_args=[]):
        self._name = name
        self._qualifier = qualifier  #todo come up with a better name for this
        self._value = value
        self._additional_args = additional_args

    @property
    def name(self):
        return self._name

    @property
    def qualifier(self):
        return self._qualifier

    @property
    def value(self):
        return self._value

    @property
    def additional_args(self):
        return self._additional_args

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "({} {} {} {})".format(self._name, self._qualifier, self._value, self._additional_args)

    def __hash__(self):
        return hash(str(self))


