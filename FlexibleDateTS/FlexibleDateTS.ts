import { parse } from 'date-fns';
import * as edtf from 'edtf';

type YearMonthDay = [string | null, string | null, string | null]

class AncientDateTime {
    year: number;
    month: number | null;
    day: number | null;

    constructor(year: number, month: number | null = null, day: number | null = null) {
        this.year = year;
        this.month = month;
        this.day = day;
    }

    public getFullYear(): number{
        return this.year
    }

    public getMonth(): number | null{
        return this.month
    }

    public getDate(): number | null{
        return this.day
    }
}

export enum DateModifier {
    ABOUT = "about",
    BEFORE = "before", 
    AFTER = "after"
}


export default class FlexibleDate {
    likelyYear?: number | null = null;
    likelyMonth?: number | null = null;
    likelyDay?: number | null = null;
    modifier?: DateModifier | null = null;

    static readonly ABOUT_ALIASES = ["about", "abt", "circa", "cir", "ca.", "ca ", "c.", "late", "early", "approx", "approximately", "est", "estimated", "cal", "calc", "calculated", "say", "around", "sometime"] as const;

    constructor(likelyDate: string | null);
    constructor(likelyDay: number | null, likelyMonth: number | null, likelyYear: number | null, modifier?: DateModifier | null);
    constructor(arg1: string | number | null, arg2?: number | null, arg3?: number | null, arg4?: DateModifier | null) {
      if (typeof arg1 === "string") {
        const date = FlexibleDate.createFlexibleDate(arg1);
        this.likelyDay = date.likelyDay;
        this.likelyMonth = date.likelyMonth;
        this.likelyYear = date.likelyYear;
        this.modifier = date.modifier;
      } 
      else {
        this.likelyDay = arg1 ?? null;
        this.likelyMonth = arg2 ?? null;
        this.likelyYear = arg3 ?? null;
        this.modifier = arg4 ?? null
      }

      this.validateFields();
    }

    private validateFields(): void {

        const monthsWith31Days = [1, 3, 5, 7, 8, 10, 12];
        const monthsWith30Days = [4, 6, 9, 11];
        const monthsWith29Days = [2];

        // Validate year
        if (this.likelyYear !== null && this.likelyYear !== undefined) {
            if (this.likelyYear < -100000 || this.likelyYear > 100000) {
                throw new Error('likely_year must be between -100,000 BC and 100,000 AD');
            }
        }
        
        // Validate month
        if (this.likelyMonth !== null && this.likelyMonth !== undefined) {
            if (this.likelyMonth < 1 || this.likelyMonth > 12) {
                throw new Error('likely_month must be between 1 and 12');
            }
        }
        
        // Validate day
        if (this.likelyDay !== null && this.likelyDay !== undefined) {
            if (this.likelyMonth !== null && this.likelyMonth !== undefined) {
                const maxDaysInMonth = monthsWith31Days.includes(this.likelyMonth) ? 31 : monthsWith30Days.includes(this.likelyMonth) ? 30 : monthsWith29Days.includes(this.likelyMonth) ? 29 : 31;
                if (this.likelyDay < 1 || this.likelyDay > maxDaysInMonth) {
                    throw new Error('likely_day must be between 1 and ' + maxDaysInMonth);
                }
            }
            if (this.likelyDay < 1 || this.likelyDay > 31) {
                throw new Error('likely_day must be between 1 and 31');
            }
        }
    }

    public toString() {  
        const hasDay = this.likelyDay !== undefined && !isNaN(this.likelyDay as number) && this.likelyDay !== null;
        const hasMonth = this.likelyMonth !== undefined && !isNaN(this.likelyMonth as number) && this.likelyMonth !== null;
        const hasYear = this.likelyYear !== undefined && !isNaN(this.likelyYear as number) && this.likelyYear !== null;
        const hasModifier = this.modifier !== undefined && this.modifier !== null;

        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return (hasModifier ? this.modifier?.valueOf() : "") +
        (hasModifier && (hasDay || hasMonth || hasYear) ? " " : "") +
        (hasDay ? this.likelyDay : "") +
        (hasDay && hasMonth ? " " : "") +
        (hasMonth ? months[this.likelyMonth! - 1] : "") +
        ((hasDay || hasMonth) && hasYear ? " " : "") +
        (hasYear ? this.likelyYear : "");
    }

    public inspect(): string {
        let yearConversion = "XXXX";
        if (this.likelyYear !== null && this.likelyYear !== undefined) {
            yearConversion = `${Math.abs(this.likelyYear)}`;
            while (yearConversion.length < 4) {
                yearConversion = `0${yearConversion}`;
            }
            if (this.likelyYear > 0) {
                yearConversion = `+${yearConversion}`;
            }
            else if (this.likelyYear < 0) {
                yearConversion = `-${yearConversion}`;
            }
        }

        let beforeModifier = "";
        let afterModifier = "";
        if (this.modifier == DateModifier.ABOUT) {
            beforeModifier = "A";
        } 
        else if (this.modifier == DateModifier.BEFORE) {
            beforeModifier = "/";
        } 
        else if (this.modifier == DateModifier.AFTER) {
            afterModifier = "/";
        }

        if (this.likelyDay && this.likelyMonth) {
            return `${beforeModifier}${yearConversion}-${this.likelyMonth < 10 ? '0' : ''}${this.likelyMonth}-${this.likelyDay < 10 ? '0' : ''}${this.likelyDay}${afterModifier}`;
        }
        else if (this.likelyMonth) {
            return `${beforeModifier}${yearConversion}-${this.likelyMonth < 10 ? '0' : ''}${this.likelyMonth}${afterModifier}`;
        }
        else {
            return `${beforeModifier}${yearConversion}${afterModifier}`;
        }
    }

    valueOf(): boolean {
        //eslint-disable-next-line
        const isNull = (val: any) => val === null || (typeof val === 'number' && isNaN(val));
        return !(isNull(this.likelyDay) && isNull(this.likelyMonth) && isNull(this.likelyYear));
    }

    public equals(obj: object): boolean {
        if (!obj || !(obj instanceof FlexibleDate)) {
            return false;
        }
        return this.likelyDay === obj.likelyDay && this.likelyMonth === obj.likelyMonth && this.likelyYear === obj.likelyYear && this.modifier === obj.modifier;
    }

    public static createFlexibleDate(likelyDate : string | null | undefined){
        if( likelyDate == null || likelyDate == undefined || likelyDate.trim() == ""){
            return new FlexibleDate(null, null, null, null);
        }
        else if(typeof likelyDate != "string"){
            throw new Error("likelyDate must be a string or null");
        }

        let likelyDay: number | null = null;
        let likelyMonth: number | null = null;
        let likelyYear: number | null = null;

        const modifier = FlexibleDate.getModifier(likelyDate);

        const  [parsedDate, numFields]  = FlexibleDate.getCleanedDateAndNumFields(likelyDate);

        if (numFields >= 1) {
            if (parsedDate instanceof AncientDateTime) {
                likelyYear = parsedDate.getFullYear();
                likelyMonth = parsedDate.getMonth();
                likelyDay = parsedDate.getDate();
            } else {
                if (parsedDate.getUTCFullYear() !== 9999) {
                    likelyYear = parsedDate.getUTCFullYear();
                }
                if (numFields >= 2) {
                    likelyMonth = parsedDate.getUTCMonth() + 1; // Convert from 0-indexed to 1-indexed
                }
                if (numFields === 3) {
                    likelyDay = parsedDate.getUTCDate();
                }
            }
        }
    
        return new FlexibleDate(likelyDay, likelyMonth, likelyYear, modifier);
    }

    /**Creates a FlexibleDate object from a formal date string.
    *
    * @param formalDate (str): an EDTF (Extended Date/Time Format) string such as:
            - "+1526-01-01T00:00:00Z/+2020-12-31T23:59:59Z" (date range)
            - "+1910/+1910" (year range)
            - "/+1887-03" (open-ended before date range)
            - "+1976-07-11/" (open-ended after date range)
            - "+1910-01-01T00:00:00Z/+1910-12-31T23:59:59Z" (date range within year)
            - "A+2014-08" (approximate date)
    * @throws ValueError: raised if input is not a valid EDTF (Extended Date/Time Format) string      
    * @returns FlexibleDate: the FlexibleDate object parsed from the GEDCOMX date format string
    */
    public static createFlexibleDateFromFormalDate(formalDate: string): FlexibleDate {

        if (typeof formalDate !== 'string') {
            throw new Error('formalDate must be a string') // should never happen
        }
        
        try {
            let modifier = null;
            if (formalDate.includes('A')) {
                modifier = DateModifier.ABOUT;
            }
            let cleanedDate = formalDate.replace(/A/g, '');
            // Remove '+' signs which aren't standard EDTF
            cleanedDate = cleanedDate.replace(/\+/g, '');
            // Remove time and timezone info (e.g., T00:00:00Z) to keep only the date
            cleanedDate = cleanedDate.replace(/T\d{2}:\d{2}:\d{2}Z?/g, '');
            // Remove repetition info (e.g. R; /R10; R10/)
            cleanedDate = cleanedDate.replace(/\/?R\d*\/?/g, '');
            // Remove duration info (e.g. P; /P12Y; P/)
            cleanedDate = cleanedDate.replace(/\/?P\w*\/?/g, '');

            // Check if includes syntax for after or before (e.g. 1900/; /1900; 1900/2000)
            const hasAfter = /\d+\//.test(cleanedDate);
            const hasBefore = /\/-?\d+/.test(cleanedDate);
            if (hasAfter && !hasBefore) {
                modifier = DateModifier.AFTER;
            }
            if (hasBefore && !hasAfter) {
                modifier = DateModifier.BEFORE;
            }
            //Remove leading and trailing '/'
            cleanedDate = cleanedDate.replace(/^\//g, '');
            cleanedDate = cleanedDate.replace(/\/$/g, '');
            
            let edtfObj = edtf.parse(cleanedDate) as {
                type: string;
                level: number;
                values: number[] | Object[];
            }
            let lowerDate;
            let upperDate;
            
            // Extract year, month, day from the edtf object
            // The edtf package returns { type: 'Date', level: 0, values: [year, month-1, day] }
            // Note: month is 0-indexed in JavaScript, but we want 1-indexed like Python
            let likelyYear: number | null = null
            let likelyMonth: number | null = null  
            let likelyDay: number | null = null

            if (edtfObj && edtfObj.type === 'Interval' && Array.isArray(edtfObj.values) && edtfObj.values[0]) {
                lowerDate = edtfObj.values[0] as {
                    type: string;
                    level: number;
                    values: number[];
                };
                upperDate = edtfObj.values[1] as {
                    type: string;
                    level: number;
                    values: number[];
                };
            }
            else {
                lowerDate = edtfObj as {
                    type: string;
                    level: number;
                    values: number[];
                };
            }
            
            if (lowerDate && lowerDate.values && Array.isArray(lowerDate.values)) {
                const [year, month, day] = lowerDate.values
                
                likelyYear = (year !== undefined && year !== 9999) ? year : null
                likelyMonth = (month !== undefined && (month !== 0 || cleanedDate.split('-').length > 1)) ? month + 1 : null
                likelyDay = (day !== undefined && (day !== 1 || cleanedDate.split('-').length > 2)) ? day : null
            }
            
            // Handle date ranges - check for year/month span collapsing
            if (upperDate) {
                const [startPart, endPart] = cleanedDate.split('/')
                const lower = (edtfObj.values[0] as { values: number[] })?.values ?? []
                const upper = (edtfObj.values[1] as { values: number[] })?.values ?? []
                const [lowerYear, lowerMonth, lowerDay] = lower
                const [upperYear, upperMonth, upperDay] = upper

                // Note: months are 0-indexed here (0=Jan, 11=Dec), unlike Python's 1-indexed tm_mon
                const getUpperMonthRange = (month: number): number =>
                    month === 1 ? 28 : [3, 5, 8, 10].includes(month) ? 30 : 31

                const isYearRange = (
                    (startPart.length === 4 && endPart.length === 4 && !isNaN(parseInt(startPart)) && !isNaN(parseInt(endPart))) ||
                    (lowerMonth === 0 && upperMonth === 11 && lowerYear === upperYear)
                )
                const isMonthRange = (
                    startPart.length === 6 && endPart.length === 6 &&
                    lowerYear === upperYear &&
                    lowerMonth === upperMonth &&
                    lowerDay === 1 &&
                    upperDay !== undefined && upperDay >= getUpperMonthRange(upperMonth)
                )

                if (isYearRange) {
                    likelyMonth = null
                    likelyDay = null
                } else if (isMonthRange) {
                    likelyDay = null
                }
            }

            return new FlexibleDate(likelyDay, likelyMonth, likelyYear, modifier)
        } catch (error) {
            throw new Error(`Unable to parse EDTF string "${formalDate}": ${error}`)
        }
    }

    public compareDates(dateToCompare : FlexibleDate): number {
        let score: number = 100;

        if (this.valueOf() && dateToCompare.valueOf()) {
            const thisDateValues: (number | null | undefined)[] = [this.likelyYear, this.likelyMonth, this.likelyDay];
            const dateToCompareValues: (number | null | undefined)[] = [dateToCompare.likelyYear, dateToCompare.likelyMonth, dateToCompare.likelyDay];
            const sharedNonNullCount: number = thisDateValues.reduce((count: number, val, index) => 
                (val !== null && val !== undefined && dateToCompareValues[index] !== null && dateToCompareValues[index] !== undefined) ? count + 1 : count, 0);
            
            const weight: number = sharedNonNullCount > 0 ? 1 / sharedNonNullCount : 1;

            let allScores: number[] = [];
            

            if (this.likelyDay && dateToCompare.likelyDay) {
                const maxDiff = 15;
                const diff = Math.abs(this.likelyDay - dateToCompare.likelyDay);
                allScores.push(Math.max(0, 1 - diff / maxDiff) * weight);
            }
            if (this.likelyMonth && dateToCompare.likelyMonth) {
                const maxDiff = 6;
                const diff = Math.abs(this.likelyMonth - dateToCompare.likelyMonth);
                allScores.push(Math.max(0, 1 - diff / maxDiff) * weight);
            }
            if (this.likelyYear && dateToCompare.likelyYear) {
                const maxDiff = 20;
                const diff = Math.abs(this.likelyYear - dateToCompare.likelyYear);
                if (diff >= maxDiff) {
                    return 0;
                }
                allScores.push(Math.max(0, 1 - diff / maxDiff) * weight);
            }
            
            score = (allScores.reduce((sum, score) => sum + score, 0)) * 100;
        }

        if (Number.isInteger(score)) {
            return score;
        }
        return Number(score.toFixed(5));
    }

    private static chooseMostReasonableValue(values: (number | null | undefined)[]){
        const filteredValues = values.filter((v): v is number => v !== null && v !== undefined && !isNaN(v));
        if (filteredValues.length === 0) {
            return null;
        }

        const counter = new Map<number, number>();
        filteredValues.forEach(value => {
            counter.set(value, (counter.get(value) || 0) + 1);
        });

        const totalCount = Array.from(counter.values()).reduce((sum, count) => sum + count, 0);
        const scores = new Map<number, number>();

        for (const [value, count] of counter.entries()) {
            let confidence = count / totalCount;
            for (const [otherValue, otherCount] of counter.entries()) {
                if (value !== otherValue) {
                    confidence += (1.2 * (otherCount / totalCount)) / (1 + Math.abs(value - otherValue));
                }
            }
            scores.set(value, confidence);
        }

        return Array.from(scores.entries()).reduce((best, curr) => curr[1] > best[1] ? curr : best)[0];
    }

    public static combineFlexibleDates(dates: FlexibleDate[]) : FlexibleDate {
        // If there's only one date, return it as is
        if (dates.length === 1) {
            return dates[0];
        }
        
        const bestYear = FlexibleDate._chooseBestValue("likelyYear", dates);
        let remainingDates = dates.filter(date => date.likelyYear === bestYear || date.likelyYear === null);

        const bestMonth = FlexibleDate._chooseBestValue("likelyMonth", remainingDates);
        remainingDates = remainingDates.filter(date => date.likelyMonth === bestMonth || date.likelyMonth === null);

        const bestDay = FlexibleDate._chooseBestValue("likelyDay", remainingDates);

        return new FlexibleDate(bestDay, bestMonth, bestYear);
    }

    private static getModifier(date: string): DateModifier | null {
        const normalizedDate = date.trim().toLowerCase();

        const ABOUT_ALIASES = [
            "about", "abt", "circa", "cir ", "cir.", "ca.", "ca ", "c.",
            "late", "early", "approx ", "approx. ", "approximately", 
            "estimated", "cal ", "cal.", "calc ",
            "calc.", "calculated", "say", "around", "sometime in"
        ];
        const BEFORE_ALIASES = [
            "before", "bef ", "bef.", "prior", "pre ", "earlier",
            "no later than", "not later than", "ante ", "previous to", 
            "by", "sometime before"
        ];
        const AFTER_ALIASES = [
            "after", "aft ", "aft.", "following", "later than",
            "subsequent to", "since", "post", "not before", "sometime after"
        ];

        let modifier: DateModifier | null = null;
        if (ABOUT_ALIASES.some(alias => normalizedDate.startsWith(alias))) {
            modifier = DateModifier.ABOUT;
        }
        if (BEFORE_ALIASES.some(alias => normalizedDate.startsWith(alias))) {
            modifier = DateModifier.BEFORE;
        }
        if (AFTER_ALIASES.some(alias => normalizedDate.startsWith(alias))) {
            modifier = DateModifier.AFTER;
        }

        return modifier;
    }

    private static _chooseBestValue(valueType: "likelyYear" | "likelyMonth" | "likelyDay", dates: FlexibleDate[]): number | null {
        const SIGNIFICANT_VALUE_DIFFERENCE = 3;
        const SIGNIFICANT_FREQUENCY_GAP = 0.25;

        const frequenciesAndSpecificities = FlexibleDate._buildFrequencyMap(valueType, dates);
        if (frequenciesAndSpecificities.length === 0) {
            return null;
        }

        const bestFrequencyInitVal = frequenciesAndSpecificities.reduce((best: { frequency: number, specificity: number }, curr: { frequency: number, specificity: number }) => {
            return curr.frequency > best.frequency ? curr
                : best;
        }, { frequency: 0, specificity: 0 });
        const mostFrequentValues = frequenciesAndSpecificities.filter((x: { frequency: number, specificity: number }) => x.frequency === bestFrequencyInitVal.frequency && x.specificity >= bestFrequencyInitVal.specificity);
        const mostFrequentValue = mostFrequentValues.sort((a: { attribute: number }, b: { attribute: number }) => a.attribute - b.attribute)[Math.floor((mostFrequentValues.length - 1) / 2)];

        const bestSpecificityInitVal = frequenciesAndSpecificities.reduce((best: { frequency: number, specificity: number }, curr: { frequency: number, specificity: number }) => {
            return curr.specificity > best.specificity ? curr 
            : curr.specificity === best.specificity && curr.frequency > best.frequency ? curr
            : best;
        }, { frequency: 0, specificity: 0 });
        const mostSpecificValues = frequenciesAndSpecificities.filter((x: { frequency: number, specificity: number }) => x.specificity === bestSpecificityInitVal.specificity && x.frequency >= bestSpecificityInitVal.frequency);
        const mostSpecificValue = mostSpecificValues.sort((a: { attribute: number }, b: { attribute: number }) => a.attribute - b.attribute)[Math.floor((mostSpecificValues.length - 1) / 2)];

        const difference = Math.abs(mostSpecificValue.attribute - mostFrequentValue.attribute);

        let bestValue = mostSpecificValue;
        if (mostSpecificValue.frequency < mostFrequentValue.frequency * SIGNIFICANT_FREQUENCY_GAP && difference > SIGNIFICANT_VALUE_DIFFERENCE) {
            bestValue = mostFrequentValue;
        }

        return bestValue.attribute;
    }

    private static _buildFrequencyMap(valueType: "likelyYear" | "likelyMonth" | "likelyDay", dates: FlexibleDate[]): { attribute: number, frequency: number, specificity: number }[] {
        const frequencyMap = new Map<number, number>();
        const specificityMap = new Map<number, number>();
        for (const date of dates) {
            const attr = date[valueType];
            if (attr === null || attr === undefined) continue;

            const dateSpecificity = date.inspect().split('-').length;

            if (!frequencyMap.has(attr)) {
                frequencyMap.set(attr, 1);
                specificityMap.set(attr, dateSpecificity);
            } else {
                const knownSpecificity = specificityMap.get(attr)!;
                if (dateSpecificity > knownSpecificity) {
                    specificityMap.set(attr, dateSpecificity);
                }
                frequencyMap.set(attr, frequencyMap.get(attr)! + 1);
            }
        }

        const frequenciesAndSpecificities = Array.from(frequencyMap.entries()).map(([attribute, frequency]) => ({ attribute, frequency, specificity: specificityMap.get(attribute)! }));
        return frequenciesAndSpecificities;
    }

    private static parseWithDateUtil(likelyDate: string): [Date, number] {
        let parsedDate = new Date('9999-01-01');
        let numFields = 0;

        try {
            const date = likelyDate.trim();

            if (/^0{0,2}[0-9]{2}$/.test(date)) {
                throw new Error('Date does not work for years 0000 and 0099');
            }

            if (date.toLowerCase().includes('bc')) {
                throw new Error('Date does not work for negative years');
            }

            const monthsToInt: Record<string, number> = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12};
            const parts = date.split(/\s+/).map(part => monthsToInt[part] || parseInt(part));
            const monthStringsInDate = date.split(/\s+/).filter(part => Object.keys(monthsToInt).includes(part));

            const newDate = new Date(date);
            if (isNaN(newDate.getTime()) || monthStringsInDate.length > 1) { // Setting up this block to mimic Python's ParserError and other unique behavior.
                if (Object.keys(monthsToInt).includes(date)) { // Python parser handled just a single month string, but we don't so we do it manually here.
                    parsedDate.setUTCMonth(monthsToInt[date] - 1);
                    numFields = 2;
                }
                throw new Error('ParsingError: Date is invalid');
            }
            parsedDate = newDate;
            numFields = date.split(/\s+/).length;
            
            const parsedDayCorrectly = parts.includes(parsedDate.getUTCDate());
            const parsedMonthCorrectly = parts.includes(parsedDate.getUTCMonth() + 1);
            const parsedYearCorrectly = parts.includes(parsedDate.getUTCFullYear());
            if (numFields === 3 && parsedYearCorrectly && !(parsedMonthCorrectly && parsedDayCorrectly)) { // Check for rolover. (e.i. new Date('02-31-2000') -> '03-02-2000')
                parsedDate.setUTCMonth(parsedDate.getUTCMonth() - 1);
                numFields = 2; // Drop the day, keep only month and year
            }

            if (0 < numFields && numFields < 3 && parts.every(val => typeof val === "number" && val < 1000)) { // If we have a date/month but no year, set the year to 9999
                parsedDate.setUTCFullYear(9999)
                numFields += 1;

            }

        } catch (error) {}

        return [parsedDate, numFields];
    }

    public static gleanYearMonthDay(text: string): YearMonthDay {
        const acceptableCombos = new Set<YearMonthDay>();

        acceptableCombos.add([null, null, null]);

        // Find valid years (overlapping 4-digit years up to the current year)
        const currentYear = new Date().getFullYear();
        const validYears = Array.from(text.matchAll(/[-]?(?=(\d{4}))/g))
            .map(match => match[1])
            .filter(year => parseInt(year) <= currentYear);

        const validYearsAndInstances = FlexibleDate.getStringsAndInstances(validYears);

        for (const [year, i] of validYearsAndInstances) {
            acceptableCombos.add([year, null, null]);

            // Remove the year and find valid months
            const textA = FlexibleDate.substituteIthInstance(text, year, ' ', i).trim().replace(/\s{2,}/g, ' ');
            const validMonths = FlexibleDate.findAllMatches(textA, ['\\b[1-9]\\b', '\\b0[1-9]\\b', '\\b1[0-2]\\b', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']);
            const validMonthsAndInstances = FlexibleDate.getStringsAndInstances(validMonths);

            for (const [month, i] of validMonthsAndInstances) {
                acceptableCombos.add([year, month, null]);

                // Remove the month and find valid days
                const textB = FlexibleDate.substituteIthInstance(textA, month, ' ', i).trim().replace(/\s{2,}/g, ' ');
                const validDays = FlexibleDate.findAllMatches(textB, ['\\b[1-9]\\b', '\\b0[1-9]\\b', '\\b1[0-9]\\b', '\\b2[0-9]\\b', '\\b3[01]\\b']);

                for (const day of validDays) {
                    const monthNum = parseInt(month);
                    const dayNum = parseInt(day);
                    
                    // Validate range and ensure no date overflow
                    if (monthNum < 1 || monthNum > 12 || dayNum < 1 || dayNum > 31) continue;
                    
                    try {
                        const parsedTest = parse(`${year}-${month}-${day}`, 'yyyy-M-d', new Date());
                        if (parsedTest.getFullYear() === parseInt(year) &&
                            parsedTest.getMonth() + 1 === monthNum &&
                            parsedTest.getDate() === dayNum) {
                            acceptableCombos.add([year, month, day]);
                        }
                    } catch (error) {
                        // Ignore invalid dates
                        //console.log(error);
                    }
                }
            }
        }

        // Scoring function
        const keyFunc = (t: YearMonthDay): [number, number] => [
            t.reduce((sum, x) => sum + (x ? x.length : 0), 0),  // Primary ranking: total characters in non-null elements
            t.filter(x => x !== null).length                    // Secondary ranking: count of non-null elements
        ];

        const scores = new Map<YearMonthDay, [number, number]>(
            [...acceptableCombos].map(option => [option, keyFunc(option)])
        );

        const maxScore = Math.max(...Array.from(scores.values()).map(s => s[0]));
        const bestOptions = [...scores.entries()]
            .filter(([, score]) => score[0] === maxScore)
            .map(([option]) => option);

        const monthsToInt: Record<string, number> = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12};

        const bestYears: number[] = [];
        const bestMonths: number[] = [];
        const bestDays: number[] = [];
        bestOptions.forEach(([year, month, day]) => {
            if (year !== null) {
                bestYears.push(parseInt(year));
            }
            if (month !== null) {
                if (Object.keys(monthsToInt).includes(month)) {
                    bestMonths.push(monthsToInt[month]);
                }
                else {
                    bestMonths.push(parseInt(month));
                }
            }
            if (day !== null) {
                bestDays.push(parseInt(day));
            }
        })

        const reasonableYear = bestYears.length > 0 ? FlexibleDate.chooseMostReasonableValue(bestYears) : null;
        const reasonableMonth = bestMonths.length > 0 ? FlexibleDate.chooseMostReasonableValue(bestMonths) : null;
        const reasonableDay = bestDays.length > 0 ? FlexibleDate.chooseMostReasonableValue(bestDays) : null;

        const bestYear = reasonableYear !== null ? String(reasonableYear) : null;
        const bestMonth = reasonableMonth !== null ? String(reasonableMonth) : null;
        const bestDay = reasonableDay !== null ? String(reasonableDay) : null;
        return [bestYear, bestMonth, bestDay];
    }

    private static getStringsAndInstances(stringList: string[]){
        const countDict: Record<string, number> = {};
        const result: [string, number][] = [];

        for (const str of stringList) {
            countDict[str] = (countDict[str] || 0) + 1;
            result.push([str, countDict[str] - 1]);
        }

        return result;
    }

    private static substituteIthInstance(text: string, pattern: string, replacement: string, i: number): string {
        let count = 0;
        return text.replace(new RegExp(pattern, 'g'), (match) => {
            if (count === i) {
                count++;
                return replacement;
            }
            count++;
            return match;
        });
    }

    private static findAllMatches(text: string, regexPatterns: string[]): string[] {
        let allMatches: string[] = [];
        for (const pattern of regexPatterns) {
            allMatches = allMatches.concat(text.match(new RegExp(pattern, 'gi')) || []);
        }
        return allMatches;
    }

    private static getCleanedDateAndNumFields(dateString: string): [AncientDateTime|Date, number] {
        const date = FlexibleDate.cleanDate(dateString);

        if(/^-?[0-9]{4}$/.test(date)){
            return [new AncientDateTime(parseInt(date, 10)), 1];
        }

        let [parsedDate, numFields] = FlexibleDate.parseWithDateUtil(date);

        if (numFields !== 0){
            return [parsedDate, numFields];
        }

        const [year, month, day] = FlexibleDate.gleanYearMonthDay(date);
        if(year == null){
            return [parsedDate, numFields];
        }

        const reconstructedDate = `${year} ${month || ""} ${day || ""}`.trim();
        [parsedDate, numFields] = FlexibleDate.parseWithDateUtil(reconstructedDate)
        return [parsedDate, numFields];
    }

    private static cleanDate(dateString: string): string{
        let date = dateString.normalize("NFKD"); // Equivalent to unidecode for basic ASCII conversion
        date = date.toLowerCase().trim();
        date = date.replace(/pm|am/g, ' ');

        if (/^-[0-9]{1,4}$/.test(date)) {
            date = date.slice(1);
            date = `${date} bc`;
        }
    
        if (date.length > 9) {
            date = date.replace(/([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]/g, ' ');
        }
        if (date.length > 6) {
            date = date.replace(/([01]?[0-9]|2[0-3]):[0-5][0-9]/g, ' ');
        }
        
        date = date.replace(/\//g, ' ');
        date = date.replace(/,/g, ' ');
        date = date.replace(/\./g, ' ');
        date = date.replace(/"/g, ' ');
        date = date.replace(/'/g, ' ');
        date = date.replace(/-/g, ' ');
        date = date.replace(/_/g, ' ');

        date = date.replace(/\s{2,}/g, ' ').trim();
        date = date.replace(/[^\w\s]/g, ' ');
        date = date.replace(/(?<=[a-zA-Z])(?=\d)|(?<=\d)(?=[a-zA-Z])/g, ' ');
       
        const protectedWords = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'bc'];
        const protectedRegex = new RegExp(`(${protectedWords.join('|')})`, 'gi');
        date = date.replace(protectedRegex, ' $1 ');

        const removeUnprotectedWordsRegex = new RegExp(`\\b(?!\\d|\\b${protectedWords.join('\\b|\\b')}\\b)\\w+\\b`, 'gi');
        date = date.replace(removeUnprotectedWordsRegex, '');

        date = date.replace(/\s{2,}/g, ' ').trim();

        if (/^[0-9]( bc)?$/.test(date)) {
            date = `000${date}`;
        } else if (/^[0-9]{2}( bc)?$/.test(date)) {
            date = `00${date}`;
        } else if (/^[0-9]{3}( bc)?$/.test(date)) {
            date = `0${date}`;
        }
        if (/[0-9]{4} bc/.test(date)) {
            date = `-${date}`;
        }
    
        date = date.replace('bc', '').trim();
        return date;
    }

}