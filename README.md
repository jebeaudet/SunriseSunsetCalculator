SunriseSunsetCalculator
=======================

Calculate the sunset and sunrise time based on the date and the latitude/longitude.

Based on the algorithm found on :
http://williams.best.vwh.net/sunrise_sunset_algorithm.htm

To use, simply enter the necessary inputs at the beginning of the script. More info on the zenith parameter can be found here:
http://www.timeanddate.com/worldclock/aboutastronomy.html

To use, import the module and create an object like so:

```Python
>>> import datetime
>>> from sunrise_sunset import SunriseSunset
>>> ro = SunriseSunset(datetime.datetime.now(), latitude=46.805,
longitude=-71.2316)
>>> rise_time, set_time = ro.calculate()
>>> print rise_time, set_time
2015-12-18 12:25:00 2015-12-18 20:57:00
>>> # Or you can specify the current time zone, like so
>>> ro = SunriseSunset(datetime.datetime.now(), latitude=46.805,
longitude=-71.2316, localOffset=-5)
>>> rise_time, set_time = ro.calculate()
>>> print rise_time, set_time
2015-12-18 07:25:00 2015-12-18 15:57:00
```

Finally, don't forget to modify the offset for the timezone. Best is to leave it at 0 to get UTC.

Python 3 support
----------------

This module is compatible with Python 2 and Python 3. It has been tested under
python 2.7.10 and python 3.4.3+ on Ubuntu Linux
