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
>>> import sunset_sunrise
>>> ro = sunset_sunrise.SunsetSunrise(datetime.datetime.now(), latitude=46.805,
longitude=-71.2316)
>>> set_time, rise_time = ro.calculate()
>>> print set_time, rise_time
2015-12-18 20:57:00 2015-12-18 12:25:00
>>> # Or you can specify the current time zone, like so
>>> ro = sunset_sunrise.SunsetSunrise(datetime.datetime.now(), latitude=46.805,
longitude=-71.2316, localOffset=-5)
>>> set_time, rise_time = ro.calculate()
>>> print set_time, rise_time
2015-12-18 15:57:00 2015-12-18 07:25:00
```

Finally, don't forget to modify the offset for the timezone. Best is to leave it at 0 to get UTC.
