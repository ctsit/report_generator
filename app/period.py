"""
Helper class for generating pairs of datetimes
delimiting a week or a month relative to a reference

@author: Andrei Sura
"""

from datetime import date
from datetime import datetime
from datetime import timedelta

class Period(object):
    def __init__(self, ptype='curr_week', reference=date.today()):
        # assert ptype in ['curr_week', 'prev_week', 'curr_month', 'prev_month']
        assert ptype in ['curr_week', 'prev_week']
        assert type(reference) is date
        self._type = ptype

        # set the time for the begin/end of the reference date
        dt_begin = datetime.combine(reference, datetime.min.time())
        dt_end = datetime.combine(reference, datetime.max.time())

        # Based on period type set the offset
        if "curr_week" == ptype:
            weeks = 0
        elif "prev_week" == ptype:
            weeks = 1
        else:
            #@TODO: add support for '-x week' or '+y month'
            weeks = 0

        delta_begin = timedelta(dt_begin.weekday() + 1 + 7*weeks)
        delta_end = timedelta(5 - 7*weeks - dt_begin.weekday() )
        self._begin = dt_begin - delta_begin
        self._end   = dt_end + delta_end
 
    def get_begin_date(self):
        return self._begin.strftime('%m-%d-%Y')

    def get_end_date(self):
        return self._end.strftime('%m-%d-%Y')

    def get_begin_datetime(self):
        return self._begin.strftime('%m-%d-%Y %H:%M:%S')

    def get_end_datetime(self):
        return self._end.strftime('%m-%d-%Y %H:%M:%S')
