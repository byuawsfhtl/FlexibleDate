from pydantic import BaseModel, field_validator
from typing import Optional
from dateutil.parser import parse
from datetime import datetime
from unidecode import unidecode
import re
from collections import Counter

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
        if v is not None and (v < -100_000 or v > 100_000):
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
        if v is not None and (v < 1 or v > 12):
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
        if v is not None and (v < 1 or v > 31):
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
    """Parses a string (or None) to create a FlexibleDate object.

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
        raise ValueError("likelyDate must be str or None")
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

def _getCleanedDateAndNumFields(date:str) -> tuple[datetime, int]:
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
    date = unidecode(date)
    date = date.replace("/"," ")
    date = date.replace(","," ")
    date = date.replace("."," ")
    date = date.replace("\""," ")
    date = date.replace("-"," ")
    date = " ".join(date.split())
    
    # Fallback values to overwrite
    parsedDate = parse('1-1-0001')
    numFields = 0
    
    # Try to parse the initial string
    try:
        parsedDate = parse(date, default=datetime(9999, 1, 1))
        numFields = len(date.split())
        if parsedDate.year == 9999:
            numFields += 1
        success = True
    except:
        success = False
    if success:
        return parsedDate, numFields
    
    # Clearn the data by filtering out words that are not months of the year or ints
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    date = re.sub(r'[^\w\s]', ' ', date) # Gets rid of anything not letters or numbers
    date = date.replace('  ', ' ') # No double spaces
    date = re.sub(r'(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])', ' ', date) # Adds spaces when letters and numbers are next to each other
    date = re.sub(r'(' + '|'.join(months) + r')', r' \1 ', date, flags=re.IGNORECASE) #Adds space between words and their substrings if the substrings are months
    date = re.sub(r"\b(?!\d|\b" + "|".join(months) + r"\b)\w+\b", "", date, flags=re.IGNORECASE)

    # Tries again after the removing anything not numbers or months
    try:
        parsedDate = parse(date, default=datetime(9999, 1, 1))
        numFields = len(date.split())
        if parsedDate.year == 9999:
            numFields += 1
        success = True
    except:
        success = False
    if success:
        return parsedDate, numFields

    # Parse using numbers and month words
    options = _parseNumbers(date)
    bestOption = max(
        options,
        key=lambda t: (
            sum(len(str(x)) for x in t if x is not None),  # Primary ranking: total characters in non-None elements
            sum(1 for x in t if x is not None)  # Secondary ranking: count of non-None elements
        )
    )
    year, month, day = bestOption

    # If hopeless, just return defaults
    if year is None:
        return parsedDate, numFields
    
    # Construct the date
    date = f'{year} {month} {day}'.replace('None', '')

    # Try again to parse
    try:
        parsedDate = parse(date, default=datetime(9999, 1, 1))
        numFields = len(date.split())
        if parsedDate.year == 9999:
            numFields += 1
    except:
        pass

    # Return no matter what
    return parsedDate, numFields


def _parseNumbers(text:str) -> list[tuple[str|None, str|None, str|None]]:
    """Helper function for getCleanDateAndNumFields.

    Args:
        text (str): a string

    Returns:
        list[tuple[str|None, str|None, str|None]]: the options of year, month, day
    """    
    def getStringsAndInstances(strings:list) -> list[tuple[str, int]]:
        """Gets the strings and instances.

        Args:
            strings (list): input string

        Returns:
            list[tuple[str, int]]: the list of strings and instances
        """        
        countDict = {}
        result = []
        for s in strings:
            if countDict.get(s) is None:
                countDict[s] = 0
            countDict[s] += 1
            result.append((s, countDict[s] - 1))
        return result

    def substituteIthInstance(text:str, pattern:str, replacement:str, i:int) -> str:
        """Replaces the ith instance of a substring and returns the full string.

        Args:
            text (str): the input full string
            pattern (str): the pattern we will use to find all instances of substring
            replacement (str): the replacement
            i (int): the specified instance to replace.

        Returns:
            str: _description_
        """        
        def replaceCount(match:re.Match) -> str:
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
        result = re.sub(pattern, replaceCount, text)
        return result
    
    def findAllMatches(string:str, regexPatterns:list) -> list:
        """Finds all matches of various patterns in a string

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

    # Acceptable combos
    acceptableCombos = set()

    # Add nothing, in case nothing is found
    combo = (None, None, None)
    acceptableCombos.add(combo)

    validYears = [match for match in re.findall(r'(?=(\d{4}))', text) if 1000 <= int(match) <= datetime.now().year] # overlapping 4 digits between 1000 and current year
    validYearsAndInstances = getStringsAndInstances(validYears)
    for year, i in validYearsAndInstances:
        # Add the acceptable year in case no valid months are found
        combo = (year, None, None)
        acceptableCombos.add(combo)

        # Find valid months (after removing year)
        textA = substituteIthInstance(text, year, ' ', i).strip().replace('  ', ' ')
        validMonths = findAllMatches(textA, ['[1-9]', '0[1-9]', '1[0-9]', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        validMonthsAndInstances = getStringsAndInstances(validMonths)

        # Loop over valid months
        for month, i in validMonthsAndInstances:
            # Add the acceptable year month combo in case no valid days are found
            combo = (year, month, None)
            acceptableCombos.add(combo)

            # Find valid days (after removing days)
            textB = substituteIthInstance(textA, month, ' ', i).strip().replace('  ', ' ')
            validDays = findAllMatches(textB, ['[1-9]', '0[1-9]', '1[0-9]', '2[0-9]', '3[01]'])
            for day in validDays:
                # Append date combo if valid
                combo = (year, month, day)
                try:
                    parse(f'{year}-{month}-{day}')
                    acceptableCombos.add(combo)
                except:
                    pass

    return acceptableCombos