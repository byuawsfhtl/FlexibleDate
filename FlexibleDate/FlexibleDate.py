from pydantic import BaseModel, field_validator
from typing import Optional
from unidecode import unidecode
from dateutil.parser import parse, ParserError
from datetime import datetime
from collections import Counter
from edtf import parse_edtf
import re
import math

class FlexibleDate(BaseModel):
    """Represents a date.
    """
    likely_year: Optional[int] = None
    likely_month: Optional[int] = None
    likely_day: Optional[int] = None

    @field_validator('likely_year')
    def validate_likely_year(cls, v:int) -> int: 
        """Validates the likely_year parameter before object initialization.

        Args:
            v (int): the parameter likely_year in FlexibleDate

        Raises:
            ValueError: raises if year is too large or small. BC is represented by negatives.

        Returns:
            int: the validated parameter 
        """        
        if (v is not None) and (v < -100_000 or v > 100_000):
            raise ValueError(f'likely_year must be between -100,000 BC and 100,000 AD')
        return v

    @field_validator('likely_month')
    def validate_likely_month(cls, v:int) -> int:
        """Validates the likely_month parameter before object initialization.

        Args:
            v (int): the parameter likely_month in FlexibleDate

        Raises:
            ValueError: raises if month not in 1 through 12

        Returns:
            int: the validated parameter
        """
        if (v is not None) and (v < 1 or v > 12):
            raise ValueError('likely_month must be between 1 and 12')
        return v

    @field_validator('likely_day')
    def validate_likely_day(cls, v:int) -> int:
        """Validates the likely_day parameter before object initialization.

        Args:
            v (int): the parameter likely_day in FlexibleDate

        Raises:
            ValueError: raises if day not in 1 through 31. This means you can initialize objects 
            with illegal dates, such as Feb 31. Initializing using the createFlexibleDate function 
            will not allow this to happen, and will decipher only valid day-month combos, or None, 
            for each of those attributes

        Returns:
            int: the validated parameter
        """
        if (v is not None) and (v < 1 or v > 31):
            raise ValueError('likely_day must be between 1 and 31')
        return v
    
    def __bool__(self) -> bool:
        """Checks if the date is not null.

        Returns:
            bool: true if the date is not null, false otherwise
        """
        is_null = lambda x: x is None or isinstance(x, float) and math.isnan(x)
        return not (is_null(self.likely_year) and is_null(self.likely_month) and is_null(self.likely_day))
    
    def __str__(self) -> str:
        """Defines the string representation of the object (which is international format).

        Returns:
            str: the string
        """        
        months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return ((str(self.likely_day) if self.likely_day else "") + 
            (" " if self.likely_day and self.likely_month else "") +
            (str(months[self.likely_month]) if self.likely_month else "") +
            (" " if (self.likely_day or self.likely_month) and self.likely_year else "") +
            (str(self.likely_year) if self.likely_year else ""))
        
    def __repr__(self) -> str:
        """Defines the representation of the object (which is international format).

        Returns:
            str: the representation
        """
        if self.likely_year is None: 
            year_conversion = "XXXX"
        else: 
            year_conversion = f'{abs(self.likely_year)}'

            while (len(year_conversion) < 4):
                year_conversion = '0' + year_conversion
            if self.likely_year > 0:
                year_conversion = f'+{year_conversion}'
            elif self.likely_year < 0:
                year_conversion = f'-{year_conversion}'

        
        if self.likely_day and self.likely_month:
            return f'{year_conversion}-{"0" if self.likely_month < 10 else ""}{self.likely_month}-{"0" if self.likely_day < 10 else ""}{self.likely_day}'
        elif self.likely_month:
            return f'{year_conversion}-{"0" if self.likely_month < 10 else ""}{self.likely_month}'
        else:
            return f'{year_conversion}'
    
def compare_two_dates(date1:FlexibleDate, date2:FlexibleDate) -> float | int:
    """Compares two flexible dates and gives the comparison a score.

    Args:
        date1 (FlexibleDate): a FlexibleDate object
        date2 (FlexibleDate): a FlexibleDate object

    Returns:
        float | int: the score
    """    
    score = 100

    both_years = date1.likely_year and date2.likely_year
    both_months = date1.likely_month and date2.likely_month
    both_days = date1.likely_day and date2.likely_day

    if date1 and date2:
        shared_non_null_count = 0
        if both_years:
            shared_non_null_count += 1
        if both_months:
            shared_non_null_count += 1
        if both_days:
            shared_non_null_count += 1
        
        weight = 1 / shared_non_null_count if shared_non_null_count > 0 else 1

        scores = []

        if both_days:
            max_diff = 15
            diff = abs(date1.likely_day - date2.likely_day)
            scores.append(max(0, 1 - diff / max_diff) * weight)
        if both_months:
            max_diff = 6
            diff = abs(date1.likely_month - date2.likely_month)
            scores.append(max(0, 1 - diff / max_diff) * weight)
        if both_years:
            max_diff = 20
            diff = abs(date1.likely_year - date2.likely_year)
            if diff >= max_diff:
                return 0
            scores.append(max(0, 1 - diff / max_diff) * weight)
        score = sum(scores) * 100

    # Return int if whole number, float otherwise
    rounded_score = round(score, 5)
    return int(rounded_score) if rounded_score == int(rounded_score) else rounded_score

def combine_flexible_dates(dates: list[FlexibleDate]) -> FlexibleDate:
    """Combines multiple flexible dates to find the most accurate representation of the event.

    Args:
        dates (list[FlexibleDate]): a list of FlexibleDates for a specific event

    Returns:
        FlexibleDate: the combined FlexiblDate that best represents the date of the event.
    """
    all_years = [date.likely_year for date in dates]
    all_months = [date.likely_month for date in dates]
    all_days = [date.likely_day for date in dates]
    year = _choose_most_resonable_value(all_years)
    month = _choose_most_resonable_value(all_months)
    day = _choose_most_resonable_value(all_days)
    return FlexibleDate(likely_year=year, likely_month=month, likely_day=day)

def _choose_most_resonable_value(values: list[Optional[int]]) -> int | None:
    """Chooses the best value. Can compromise for a middle value.

    Args:
        values (list[Optional[int]]): either a list of the years, a list of the months, or a list of the days

    Returns:
        int: the chosen year, month, or day
    """        
    filtered_values = [v for v in values if v is not None]
    if not filtered_values:
        return None
    counter = Counter(filtered_values)
    total_count = sum(counter.values())
    scores = {}
    for value, count in counter.items():
        confidence = count / total_count
        for other_value, other_count in counter.items():
            if value != other_value:
                confidence += 1.2 * (other_count / total_count) / (1 + abs(value - other_value))
        scores[value] = confidence
    return max(scores, key=scores.get)

def create_flexible_date_from_formal_date(formal_date: str) -> FlexibleDate:
    """Creates a FlexibleDate object from a formal date string.
    
    Args:
        formal_date (str): an EDTF (Extended Date/Time Format) string.
    
    Raises:
        ValueError: raised if input is not a valid EDTF string
        
    Returns:
        FlexibleDate: the FlexibleDate object parsed from the EDTF string
    """
    if not isinstance(formal_date, str):
        raise ValueError('formal_date must be a string') # should never happen
    
    try:
        # Clean the input - remove '+' signs which aren't standard EDTF
        cleaned_date = formal_date.replace('+', '')
        # Remove time and timezone info (e.g., T00:00:00Z) to keep only the date
        cleaned_date = re.sub(r'T\d{2}:\d{2}:\d{2}Z', '', cleaned_date)
        
        edtf_obj = parse_edtf(cleaned_date)
        
        lower_date = edtf_obj.lower_strict()
        
        likely_year = lower_date.tm_year if lower_date.tm_year != 9999 else None
        likely_month = lower_date.tm_mon if lower_date.tm_mon != 1 or len(cleaned_date.split('-')) > 1 else None
        likely_day = lower_date.tm_mday if lower_date.tm_mday != 1 or len(cleaned_date.split('-')) > 2 else None
        
        if '/' in cleaned_date and len(parts := cleaned_date.split('/')) == 2:
            start_part = parts[0]
            end_part = parts[1]
            if len(start_part) == 4 and len(end_part) == 4 and start_part.isdigit() and end_part.isdigit():
                likely_month = None
                likely_day = None
        
        return FlexibleDate(likely_year=likely_year, likely_month=likely_month, likely_day=likely_day)
        
    except Exception as e:
        raise ValueError(f'Unable to parse EDTF string "{formal_date}": {str(e)}')

def create_flexible_date(likely_date:str|None) -> FlexibleDate:
    """Parses a string (or None) to create a FlexibleDate object. Attempts 
    to parse international format first, then American format, then European.

    Args:
        likely_date (str | None): the input

    Raises:
        ValueError: raised if input not str or None

    Returns:
        FlexibleDate: the FlexibleDate object parsed from the input string
    """    
    # validate input
    if likely_date is None or likely_date.strip() == "":
        return FlexibleDate(likely_day=None, likely_month=None, likely_year=None)
    elif not isinstance(likely_date, str):
        raise ValueError('likely_date must be str or None')
    
    # Defaults
    likely_day = None
    likely_month = None
    likely_year = None
    # Overwrite defaults if data is found
    parsed_date, num_fields = _get_cleaned_date_and_num_fields(likely_date)
    if num_fields >= 1:
        if parsed_date.year != 9999:
            likely_year = parsed_date.year
    if num_fields >= 2:
        likely_month = parsed_date.month
    if num_fields == 3:
        likely_day = parsed_date.day
    # Initializing and return the fd
    try:
        fd = FlexibleDate(likely_day=likely_day, likely_month=likely_month, likely_year=likely_year)
    except:
        fd = FlexibleDate(likely_day=None, likely_month=None, likely_year=None)
    return fd

class AncientDateTime(BaseModel):
    """Represents an ancient date because datetime objects can't have negative years.
    """    
    year: int
    month: Optional[None] = None
    day: Optional[None] = None

def _get_cleaned_date_and_num_fields(date:str) -> tuple[datetime|AncientDateTime, int]:
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
    date = _clean_date(date)

    # Check if we are dealing with a date between 9999 BC to 99 AD
    if bool(re.match(r'^-?[0-9]{1,4}$', date)):
        return AncientDateTime(year=int(date)), 1
    
    # Attempt to parse using dateutil
    parsed_date, num_fields = _parse_with_date_util(date)
    if num_fields != 0:
        return parsed_date, num_fields

    # Glean any year, month, or day we can find
    year, month, day = glean_year_month_day(date)
    if year is None:
        return parsed_date, num_fields
    
    # Attempt to parse using dateutil using what we gleaned 
    date = f'{year} {month} {day}'.replace('None', '')
    parsed_date, num_fields = _parse_with_date_util(date)
    return parsed_date, num_fields

def _clean_date(date:str) -> str:
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
    
    protected_words = ['bc', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    date = re.sub(r'(' + '|'.join(protected_words) + r')', r' \1 ', date, flags=re.IGNORECASE) # Add spaces between all other substrings and the protected words
    date = re.sub(r'\b(?!\d|\b' + '|'.join(protected_words) + r'\b)\w+\b', '', date, flags=re.IGNORECASE) # Remove all substrings that are not protected word or number
    date = ' '.join(date.split())
    if bool(re.match(r'^[0-9]( bc)?$', date)):
        date = f'000{date}'
    elif bool(re.match(r'^[0-9]{2}( bc)?$', date)):
        date = f'00{date}'
    elif bool(re.match(r'^[0-9]{3}( bc)?$', date)):
        date = f'0{date}'
    if bool(re.match(r'[0-9]{1,4} bc', date)):
        date = f'-{date}'
    date = date.replace('bc', '')
    date = ' '.join(date.split())
    return date

def _parse_with_date_util(date:str) -> tuple[datetime, int]:
    """Tries to parse with dateutil.

    Args:
        date (str): the (possibly messy) date string

    Returns:
        tuple[datetime, int]: the parsed date, and the number of useful fields in the parsed date
    """    
    parsed_date = parse('1-1-0001')
    num_fields = 0
    try:
        date = date.strip()
        if bool(re.match(r'^0{0,2}[0-9]{2}$', date)):
            raise ParserError('datetime.parser.parse does not work for years 0000 and 0099')
        if 'bc' in date:
            raise ParserError('datetime.parser.parse does not work for negative years')
        parsed_date = parse(date, default=datetime(9999, 1, 1))
        num_fields = len(date.split())
        if parsed_date.year == 9999:
            num_fields += 1
    except ParserError:
        pass
    return parsed_date, num_fields

def glean_year_month_day(text:str) -> tuple[str|None, str|None, str|None]:
    """Helper function for getCleanDateAndNumFields.

    Args:
        text (str): a string

    Returns:
        list[tuple[str|None, str|None, str|None]]: the options of year, month, day
    """

    months_as_ints = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    valid_years = [match for match in re.findall(r'[-]?(?=(\d{4}))', text) if int(match) <= datetime.now().year] # overlapping 4 digits between 1000 and current year
    valid_years_and_instances = _get_strings_and_instances(valid_years)
    acceptable_combos = _get_acceptable_combos(text, valid_years_and_instances)
    key_func = lambda t: (
        sum(len(str(x)) for x in t if x is not None),  # Primary ranking: total characters in non-None elements
        sum(1 for x in t if x is not None)             # Secondary ranking: count of non-None elements
    )
    scores:dict[tuple[str|None, str|None, str|None], tuple[int, int]] = {option: key_func(option) for option in acceptable_combos}
    max_score = max(scores.values())
    best_options = [option for option, score in scores.items() if score == max_score]
    best_years = []
    best_months = []
    best_days = []

    for year, month, day in best_options:
        if year is not None:
            best_years.append(int(year))
        if month is not None:
            best_months.append(months_as_ints[month])
        if day is not None:
            best_days.append(int(day))
        
    best_year = str(_choose_most_resonable_value(best_years)) if best_years else None
    best_month = str(_choose_most_resonable_value(best_months)) if best_months else None
    best_day = str(_choose_most_resonable_value(best_days)) if best_days else None
    return (best_year, best_month, best_day)

def _get_acceptable_combos(text:str, valid_years_and_instances:list[tuple[str, int]]) -> set[tuple[str|None, str|None, str|None]]:
    """Gets the acceptable combos.

    Args:
        text (str): the text to search within
        valid_years_and_instances (list[tuple[str, int]]): the valid years and instances

    Returns:
        set[tuple[str|None, str|None, str|None]]: the acceptable combos
    """
    acceptable_combos = set()
    acceptable_combos.add((None, None, None))
    for year, i in valid_years_and_instances:
        # Add the acceptable year in case no valid months are found
        combo = (year, None, None)
        acceptable_combos.add(combo)

        # Find valid months (after removing year)
        text_a = _substitute_ith_isntance(text, year, ' ', i).strip().replace('  ', ' ')
        valid_months = _find_all_matches(text_a, [r'\b[1-9]\b', r'\b0[1-9]\b', r'\b1[0-2]\b', r'jan', r'feb', r'mar', r'apr', r'may', r'jun', r'jul', r'aug', r'sep', r'oct', r'nov', r'dec'])
        valid_months_and_instances = _get_strings_and_instances(valid_months)

        _add_month_and_day_combos(year, text_a, acceptable_combos, valid_months_and_instances)
    
    return acceptable_combos

def _add_month_and_day_combos(year:str, text_a:str, acceptable_combos:set[tuple[str|None, str|None, str|None]], valid_months_and_instances:list[tuple[str, int]]) -> None:
    """Adds the month and day combos to the acceptable combos.

    Args:
        year (str): the year
        text_a (str): the text to search within
        acceptable_combos (set[tuple[str|None, str|None, str|None]]): the acceptable combos
        valid_months_and_instances (list[tuple[str, int]]): the valid months and instances

    Returns:
        set[tuple[str|None, str|None, str|None]]: the acceptable combos
    """
    # Loop over valid months
    for month, i in valid_months_and_instances:
        # Add the acceptable year month combo in case no valid days are found
        combo = (year, month, None)
        acceptable_combos.add(combo)

        # Find valid days (after removing days)
        text_b = _substitute_ith_isntance(text_a, month, ' ', i).strip().replace('  ', ' ')
        valid_days = _find_all_matches(text_b, [r'\b[1-9]\b', r'\b0[1-9]\b', r'\b1[0-9]\b', r'\b2[0-9]\b', r'\b3[01]\b'])
        for day in valid_days:
            # Append date combo if valid
            combo = (year, month, day)
            try:
                parse(f'{year}-{month}-{day}')
                acceptable_combos.add(combo)
            except ParserError:
                pass

def _get_strings_and_instances(strings:list[str]) -> list[tuple[str, int]]:
    """Gets the strings and instances.

    Args:
        strings (list): input string

    Returns:
        list[tuple[str, int]]: the list of strings and instances
    """        
    count_dict = {}
    result = []
    for string in strings:
        if count_dict.get(string) is None:
            count_dict[string] = 0
        count_dict[string] += 1
        result.append((string, count_dict[string] - 1))
    return result

def _substitute_ith_isntance(text:str, pattern:str, replacement:str, i:int) -> str:
    """Replaces the ith instance of a substring and returns the full string.

    Args:
        text (str): the input full string
        pattern (str): the pattern we will use to find all instances of substring
        replacement (str): the replacement
        i (int): the specified instance to replace

    Returns:
        str: _description_
    """        
    def _replace_count(match:re.Match) -> str:
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
    result = re.sub(pattern, _replace_count, text)
    return result

def _find_all_matches(string:str, regex_patterns:list) -> list:
    """Finds all matches of a regex pattern in a string.

    Args:
        string (str): the string to search within
        regex_patterns (list): the list of regex patterns

    Returns:
        list: the list of matches
    """        
    all_matches = []
    for pattern in regex_patterns:
        all_matches += re.findall(pattern, string, flags=re.IGNORECASE)
    return all_matches