from pydantic import BaseModel, field_validator
from typing import Optional
from unidecode import unidecode
from dateutil.parser import parse, ParserError
from datetime import datetime
from collections import Counter
import re

class FlexibleDate(BaseModel):
    """Represents a date.
    """
    likelyYear: Optional[int] = None
    likelyMonth: Optional[int] = None
    likelyDay: Optional[int] = None

    @field_validator('likelyYear')
    def validateLikelyYear(cls, v:int) -> int: 
        """Validates the likelyYear parameter before object initialization.

        Args:
            v (int): the parameter likelyYear in FlexibleDate

        Raises:
            ValueError: raises if year is too large or small. BC is represented by negatives.

        Returns:
            int: the validated parameter 
        """        
        if (v is not None) and (v < -100_000 or v > 100_000):
            raise ValueError(f'likelyYear must be between -100,000 BC and 100,000 AD')
        return v

    @field_validator('likelyMonth')
    def validateLikelyMonth(cls, v:int) -> int:
        """Validates the likelyMonth parameter before object initialization.

        Args:
            v (int): the parameter likelyMonth in FlexibleDate

        Raises:
            ValueError: raises if month not in 1 through 12

        Returns:
            int: the validated parameter
        """
        if (v is not None) and (v < 1 or v > 12):
            raise ValueError('likelyMonth must be between 1 and 12')
        return v

    @field_validator('likelyDay')
    def validateLikelyDay(cls, v:int) -> int:
        """Validates the likelyDay parameter before object initialization.

        Args:
            v (int): the parameter likelyDay in FlexibleDate

        Raises:
            ValueError: raises if month not in 1 through 31. This means you can initialize objects 
            with illegal dates, such as Feb 31. Initializing using the createFlexibleDate function 
            will not allow this to happen, and will decipher only valid day-month combos, or None, 
            for each of those attributes

        Returns:
            int: the validated parameter
        """
        if (v is not None) and (v < 1 or v > 31):
            raise ValueError('likelyDay must be between 1 and 31')
        return v
    
    def __str__(self) -> str:
        """Defines the string representation of the object (which is international format).

        Returns:
            str: the string
        """        
        if self.likelyDay:
            return f'{self.likelyYear}-{self.likelyMonth}-{self.likelyDay}'
        elif self.likelyMonth:
            return f'{self.likelyYear}-{self.likelyMonth}'
        else:
            return f'{self.likelyYear}'
    
def compareTwoDates(date1:FlexibleDate, date2:FlexibleDate) -> float:
    """Compares two flexible dates and gives the comparison a score.

    Args:
        date1 (FlexibleDate): a FlexibleDate object
        date2 (FlexibleDate): a FlexibleDate object

    Returns:
        float: the score
    """    
    score = 0

    yearInBoth = (date1.likelyYear is not None) and (date2.likelyYear is not None)
    monthInBoth = (date1.likelyMonth is not None) and (date2.likelyMonth is not None)
    dayInBoth = (date1.likelyDay is not None) and (date2.likelyDay is not None)
    
    if yearInBoth:
        difYears = abs(date1.likelyYear - date2.likelyYear)
        averageDate = (date1.likelyYear + date2.likelyYear) / 2
        rangesAndMultipliers = [
            (1980, 10), (1970, 8), (1960, 6.5), (1950, 5), (1940, 4.5), (1930, 4),
            (1920, 3.5), (1910, 3), (1900, 2.5), (1890, 1), (1850, 0.6),
            (1800, 0.5), (1700, 0.45), (1600, 0.4), (1500, 0.35), (1400, 0.3),
            (1300, 0.25), (1200, 0.2), (1100, 0.15), (float('-inf'), 0.1)
        ]
        for year, multiplier in rangesAndMultipliers:
            if averageDate < year:
                continue
            score += 20 - difYears * multiplier
            break

    if monthInBoth:
        directDif = abs(date1.likelyMonth - date2.likelyMonth)
        wrapAroundDif = 12 - directDif
        min(directDif, wrapAroundDif)
        difMonths = abs(date1.likelyMonth - date2.likelyMonth)
        if difMonths == 0:
            score += 5
        elif difMonths == 1:
            score += 3
        elif difMonths == 2:
            score += 1
        elif difMonths == 3:
            pass
        else:
            score -= difMonths

    if dayInBoth:
        directDif = abs(date1.likelyDay - date2.likelyDay)
        wrapAroundDif = 30.4 - directDif
        difDays = min(directDif, wrapAroundDif)
        score += (10 - (difDays * 3)) / 2

    if monthInBoth and yearInBoth:
        if (difMonths == 0) and (difYears == 0):
            score += 20
    if dayInBoth and monthInBoth:
        if (difDays == 0) and (difMonths == 0):
            score += 20
    if dayInBoth and monthInBoth and yearInBoth:
        if (difDays == 0) and (difMonths == 0) and (difYears == 0):
            score += 20

    return score

def combineFlexibleDates(dates: list[FlexibleDate]) -> FlexibleDate:
    """Combines multiple flexible dates to find the most accurate representation of the event.

    Args:
        dates (list[FlexibleDate]): a list of FlexibleDates for a specific event

    Returns:
        FlexibleDate: the combined FlexiblDate that best represents the date of the event.
    """
    allYears = [date.likelyYear for date in dates]
    allMonths = [date.likelyMonth for date in dates]
    allDays = [date.likelyDay for date in dates]
    year = _chooseMostReasonableValue(allYears)
    month = _chooseMostReasonableValue(allMonths)
    day = _chooseMostReasonableValue(allDays)
    return FlexibleDate(likelyYear=year, likelyMonth=month, likelyDay=day)

def _chooseMostReasonableValue(values: list[Optional[int]]) -> int:
    """Chooses the best value. Can compromise for a middle value.

    Args:
        values (list[Optional[int]]): either a list of the years, a list of the months, or a list of the days

    Returns:
        int: the chosen year, month, or day
    """        
    filteredValues = [v for v in values if v is not None]
    if not filteredValues:
        return {None:1}
    counter = Counter(filteredValues)
    totalCount = sum(counter.values())
    scores = {}
    for value, count in counter.items():
        confidence = count / totalCount
        for otherValue, otherCount in counter.items():
            if value != otherValue:
                confidence += 1.2 * (otherCount / totalCount) / (1 + abs(value - otherValue))
        scores[value] = confidence
    return max(scores, key=scores.get)

def createFlexibleDate(likelyDate:str|None) -> FlexibleDate:
    """Parses a string (or None) to create a FlexibleDate object. Attempts 
    to parse international format first, then American format, then European.

    Args:
        likelyDate (str | None): the input

    Raises:
        ValueError: raised if input not str or None

    Returns:
        FlexibleDate: the FlexibleDate object parsed from the input string
    """    
    # validate input
    if likelyDate is None:
        fd = FlexibleDate(likelyDay=None, likelyMonth=None, likelyYear=None)
        return fd
    elif not isinstance(likelyDate, str):
        raise ValueError('likelyDate must be str or None')
    # Defaults
    likelyDay = None
    likelyMonth = None
    likelyYear = None
    # Overwrite defaults if data is found
    parsedDate, numFields = _getCleanedDateAndNumFields(likelyDate)
    if numFields >= 1:
        if parsedDate.year != 9999:
            likelyYear = parsedDate.year
    if numFields >= 2:
        likelyMonth = parsedDate.month
    if numFields == 3:
        likelyDay = parsedDate.day
    # Initializing and return the fd
    try:
        fd = FlexibleDate(likelyDay=likelyDay, likelyMonth=likelyMonth, likelyYear=likelyYear)
    except:
        fd = FlexibleDate(likelyDay=None, likelyMonth=None, likelyYear=None)
    return fd

class AncientDateTime(BaseModel):
    """Represents an ancient date because datetime objects can't have negative years.
    """    
    year: int
    month: Optional[None] = None
    day: Optional[None] = None

def _getCleanedDateAndNumFields(date:str) -> tuple[datetime|AncientDateTime, int]:
    """Gets the best approximation of the proper datetime, and the number
    of fields within that datetime object that should actually be considered 
    when creating a FlexibleDate object.

    Args:
        date (str): the date input string

    Returns:
        tuple[datetime, int]: the datetime object and the num fields that should 
        be considered, as sometimes datetime might specify a specific day, but 
        no day was found in the object.
    """    
    # Simple Cleaning
    date = _cleanDate(date)

    # Check if we are dealing with a date between 9999 BC to 99 AD
    if bool(re.match(r'^-?[0-9]{4}$', date)):
        return AncientDateTime(year=int(date)), 1
    
    # Attempt to parse using dateutil
    parsedDate, numFields = _parseWithDateutil(date)
    if numFields != 0:
        return parsedDate, numFields

    # Glean any year, month, or day we can find
    year, month, day = gleanYearMonthDay(date)
    if year is None:
        return parsedDate, numFields
    
    # Attempt to parse using dateutil using what we gleaned 
    date = f'{year} {month} {day}'.replace('None', '')
    parsedDate, numFields = _parseWithDateutil(date)
    return parsedDate, numFields

def _cleanDate(date:str) -> str:
    """Cleans a date string.

    Args:
        date (str): the date string

    Returns:
        str: the cleaned date string
    """    
    date = unidecode(date)
    date = date.lower()
    date = date.strip()
    date = date.replace('pm', ' ')
    date = date.replace('am', ' ')
    if bool(re.match(r'^\-[0-9]{1,4}$', date)):
        date = date[1:]
        date = f'{date} bc'
    if len(date) > 9:
        date = re.sub(r'([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]', ' ', date)
    if len(date) > 6:
        date = re.sub(r'([01]?[0-9]|2[0-3]):[0-5][0-9]', ' ', date)
    date = date.replace('/',' ')
    date = date.replace(',',' ')
    date = date.replace('.',' ')
    date = date.replace('"',' ')
    date = date.replace("'",' ')
    date = date.replace('-',' ')
    date = date.replace('_',' ')
    date = ' '.join(date.split())
    date = re.sub(r'[^\w\s]', ' ', date)
    date = date.replace('  ', ' ')
    date = re.sub(r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])', ' ', date) # Add spaces between letters and numbers to seperate them
    protectedWords = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'bc']
    date = re.sub(r'(' + '|'.join(protectedWords) + r')', r' \1 ', date, flags=re.IGNORECASE) # Add spaces between all other substrings and the protected words
    date = re.sub(r'\b(?!\d|\b' + '|'.join(protectedWords) + r'\b)\w+\b', '', date, flags=re.IGNORECASE) # Remove all substrings that are not protected word or number
    date = ' '.join(date.split())
    if bool(re.match(r'^[0-9]( bc)?$', date)):
        date = f'000{date}'
    elif bool(re.match(r'^[0-9]{2}( bc)?$', date)):
        date = f'00{date}'
    elif bool(re.match(r'^0[0-9]{2}( bc)?$', date)):
        date = f'0{date}'
    if bool(re.match(r'[0-9]{4} bc', date)):
        date = f'-{date}'
    date = date.replace('bc', '')
    date = ' '.join(date.split())
    return date

def _parseWithDateutil(date:str) -> tuple[datetime, int]:
    """Tries to parse with dateutil.

    Args:
        date (str): the (possibly messy) date string

    Returns:
        tuple[datetime, int]: the parsed date, and the number of useful fields in the parsed date
    """    
    parsedDate = parse('1-1-0001')
    numFields = 0
    try:
        date = date.strip()
        if bool(re.match(r'^0{0,2}[0-9]{2}$', date)):
            raise ParserError('datetime.parser.parse does not work for years 0000 and 0099')
        if 'bc' in date:
            raise ParserError('datetime.parser.parse does not work for negative years')
        parsedDate = parse(date, default=datetime(9999, 1, 1))
        numFields = len(date.split())
        if parsedDate.year == 9999:
            numFields += 1
    except ParserError:
        pass
    return parsedDate, numFields

def gleanYearMonthDay(text:str) -> tuple[str|None, str|None, str|None]:
    """Helper function for getCleanDateAndNumFields.

    Args:
        text (str): a string

    Returns:
        list[tuple[str|None, str|None, str|None]]: the options of year, month, day
    """    

    # Acceptable combos
    acceptableCombos = set()

    # Add nothing, in case nothing is found
    combo = (None, None, None)
    acceptableCombos.add(combo)

    validYears = [match for match in re.findall(r'[-]?(?=(\d{4}))', text) if int(match) <= datetime.now().year] # overlapping 4 digits between 1000 and current year
    validYearsAndInstances = _getStringsAndInstances(validYears)
    for year, i in validYearsAndInstances:
        # Add the acceptable year in case no valid months are found
        combo = (year, None, None)
        acceptableCombos.add(combo)

        # Find valid months (after removing year)
        textA = _substituteIthInstance(text, year, ' ', i).strip().replace('  ', ' ')
        validMonths = _findAllMatches(textA, ['[1-9]', '0[1-9]', '1[0-9]', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        validMonthsAndInstances = _getStringsAndInstances(validMonths)

        # Loop over valid months
        for month, i in validMonthsAndInstances:
            # Add the acceptable year month combo in case no valid days are found
            combo = (year, month, None)
            acceptableCombos.add(combo)

            # Find valid days (after removing days)
            textB = _substituteIthInstance(textA, month, ' ', i).strip().replace('  ', ' ')
            validDays = _findAllMatches(textB, ['[1-9]', '0[1-9]', '1[0-9]', '2[0-9]', '3[01]'])
            for day in validDays:
                # Append date combo if valid
                combo = (year, month, day)
                try:
                    parse(f'{year}-{month}-{day}')
                    acceptableCombos.add(combo)
                except ParserError:
                    pass
    keyFunc = lambda t: (
        sum(len(str(x)) for x in t if x is not None),  # Primary ranking: total characters in non-None elements
        sum(1 for x in t if x is not None)             # Secondary ranking: count of non-None elements
    )
    scores:dict[tuple[str|None, str|None, str|None], tuple[int, int]] = {option: keyFunc(option) for option in acceptableCombos}
    maxScore = max(scores.values())
    bestOptions = [option for option, score in scores.items() if score == maxScore]
    for i in range(len(bestOptions)):
        for j in range(i + 1, len(bestOptions)):
            yearA, monthA, dayA = bestOptions[i]
            yearB, monthB, dayB = bestOptions[j]
            yearA = yearA if yearA == yearB else None
            if (monthA != monthB) or (dayA != dayB):
                monthA = None
                dayA = None
            bestOptions[i] = (yearA, monthA, dayA)
            bestOptions[j] = (yearA, monthA, dayA)
    return bestOptions[0]

def _getStringsAndInstances(stringList:list[str]) -> list[tuple[str, int]]:
    """Gets the strings and instances.

    Args:
        strings (list): input string

    Returns:
        list[tuple[str, int]]: the list of strings and instances
    """        
    countDict = {}
    result = []
    for string in stringList:
        if countDict.get(string) is None:
            countDict[string] = 0
        countDict[string] += 1
        result.append((string, countDict[string] - 1))
    return result

def _substituteIthInstance(text:str, pattern:str, replacement:str, i:int) -> str:
    """Replaces the ith instance of a substring and returns the full string.

    Args:
        text (str): the input full string
        pattern (str): the pattern we will use to find all instances of substring
        replacement (str): the replacement
        i (int): the specified instance to replace

    Returns:
        str: _description_
    """        
    def _replaceCount(match:re.Match) -> str:
        """Finds the string to be replaced.

        Args:
            match (re.Match): the match object

        Returns:
            str: the string to replace
        """            
        nonlocal i
        if i == 0:
            i -= 1
            return replacement
        i -= 1
        return match.group(0)
    result = re.sub(pattern, _replaceCount, text)
    return result

def _findAllMatches(string:str, regexPatterns:list) -> list:
    """Finds all matches of a regex pattern in a string.

    Args:
        string (str): the string to search within
        regexPatterns (list): the list of regex patterns

    Returns:
        list: the list of matches
    """        
    allMatches = []
    for pattern in regexPatterns:
        allMatches += re.findall(pattern, string, flags=re.IGNORECASE)
    return allMatches