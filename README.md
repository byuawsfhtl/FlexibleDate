# FlexibleDate

This package can parse potentially dirty date data to create a FlexibleDate object. This package can also compare FlexibleDate objects to give them a score on how close they are to one another. Finally, this package can combine various FlexibleDates for the same event into a FlexibleDate that best represents all date information about that event.

## Parsing
The package can parse strings for any day, month, or year information. If any of these attributes are not found, they are set to `None`.

```python
from FlexibleDate.FlexibleDate import createFlexibleDate, FlexibleDate

fd:FlexibleDate = createFlexibleDate('Do you remember the 21st night of sep?')
print(fd) # None-9-21
print(fd.__repr__()) # FlexibleDate(likelyYear=None, likelyMonth=9, likelyDay=21)
```

## Comparing FlexibleDates
It is often very useful to check how close two dates are, especially given two dates for the same event might be written different, usually because of an accident in remembering day, month, or year. Therefore, it can be useful to check how close the dates are using a scoring system. 

Two FlexibleDate objects could potentially be describing the same event, even when they are not identical, especially in the case of birth dates on headstones, as the person who knew it best has no way to correct the relative who is ordering the engraving.

The attributes `likelyDay` and `likelyMonth` are compared using the absolute value distance between their respective counterparts in the other FlexibleDate. On the otherhand, the part of the score for `likelyYear` is based on the difference between the two years, with the score assigned logarithmically staggered based on how far back it is (as records often get less reliable the farther back you go). A positive score is generally a good indicator that the FlexibleDates are not drastically different.

```python
from FlexibleDate.FlexibleDate import compareTwoDates, FlexibleDate

fdA = FlexibleDate(likelyDay=21, likelyMonth=9, likelyYear=1900)
fdB = FlexibleDate(likelyDay=None, likelyMonth=9, likelyYear=1902)

score = compareTwoDates(fdA, fdB)
print(score) # 20.0
```

## Combining FlexibleDates
If there are various (sometimes slightly off) FlexibleDates for a specific event (someone's birth, for example), it can be useful to have a diffinitive FlexibleDate that best represents the event.
```python
from FlexibleDate.FlexibleDate import createFlexibleDate, combineFlexibleDates

fdA = createFlexibleDate('Do you remember the 21st night of sep?')
fdB = createFlexibleDate('22 September 2024')
fdC = createFlexibleDate('21 Octo')

dates = [fdA, fdB, fdC]

fdD = combineFlexibleDates(dates=dates)
print(fdD) # 2024-9-21
```

Enjoy!