# Author: Dustin Dannenhauer
# Email: dustin.dannenhauer@parallaxresearch.org

# This file is part of tsal-translator, an extension of pypddl-parser


class TimedLiteral(object):

    def __init__(self, predicate, positive, time):
        self._predicate = predicate
        self._positive  = positive
        self._time = time

    @property
    def predicate(self):
        return self._predicate

    def is_positive(self):
        return self._positive

    def is_negative(self):
        return not self._positive

    @property
    def time(self):
        return self._time

    def __repr__(self):
        if self.is_positive():
            return '(at {} {})'.format(repr(self._predicate), self._time)
        elif self.is_negative():
            return '(at (not {}) {})'.format(repr(self._predicate), self._time)

    def __str__(self):
        if self.is_positive():
            return "{} @ {}".format(str(self._predicate),self._time)
        if self.is_negative() and self._predicate.name == '=':
            lhs = str(self._predicate.args[0])
            rhs = str(self._predicate.args[1])
            return '{0} != {1} @ {2}'.format(lhs, rhs, self._time)
        if self.is_negative():
            return 'not {} @ {}'.format(str(self._predicate), self._time)

    def __eq__(self, other):
        try:
            if self._predicate.name == other._predicate.name \
                    and self._predicate.args == other._predicate.args \
                    and self._positive == other._positive\
                    and self._time == other._time:
                return True
            else:
                return False
        except:
            if self._predicate.name == other:
                return True

    def __hash__(self):
        #print(hash(str(self)))
        return hash((self.predicate, self.is_positive(), self._time))


