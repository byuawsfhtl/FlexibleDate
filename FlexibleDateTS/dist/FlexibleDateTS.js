"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const date_fns_1 = require("date-fns");
const edtf = __importStar(require("edtf"));
class AncientDateTime {
    constructor(year, month = null, day = null) {
        this.year = year;
        this.month = month;
        this.day = day;
    }
    getFullYear() {
        return this.year;
    }
    getMonth() {
        return this.month;
    }
    getDate() {
        return this.day;
    }
}
class FlexibleDate {
    constructor(arg1, arg2, arg3) {
        if (typeof arg1 === "string") {
            const date = this.createFlexibleDate(arg1);
            this.likelyDay = date.likelyDay;
            this.likelyMonth = date.likelyMonth;
            this.likelyYear = date.likelyYear;
        }
        else {
            this.likelyDay = arg1 ?? null;
            this.likelyMonth = arg2 ?? null;
            this.likelyYear = arg3 ?? null;
        }
    }
    toString() {
        const hasDay = this.likelyDay !== undefined && !isNaN(this.likelyDay) && this.likelyDay !== null;
        const hasMonth = this.likelyMonth !== undefined && !isNaN(this.likelyMonth) && this.likelyMonth !== null;
        const hasYear = this.likelyYear !== undefined && !isNaN(this.likelyYear) && this.likelyYear !== null;
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return (hasDay ? this.likelyDay : "") +
            (hasDay && hasMonth ? " " : "") +
            (hasMonth ? months[this.likelyMonth] : "") +
            ((hasDay || hasMonth) && hasYear ? " " : "") +
            (hasYear ? this.likelyYear : "");
    }
    inspect() {
        let yearConversion = `${this.likelyYear}`;
        while (yearConversion.length < 4) {
            yearConversion = `0${yearConversion}`;
        }
        if (this.likelyDay && this.likelyMonth) {
            return `+${yearConversion}-${this.likelyMonth < 10 ? '0' : ''}${this.likelyMonth}-${this.likelyDay < 10 ? '0' : ''}${this.likelyDay}`;
        }
        else if (this.likelyMonth) {
            return `+${yearConversion}-${this.likelyMonth < 10 ? '0' : ''}${this.likelyMonth}`;
        }
        else {
            return `+${yearConversion}`;
        }
    }
    createFlexibleDate(likelyDate) {
        if (likelyDate == null || likelyDate == undefined || likelyDate == "") {
            return new FlexibleDate(null, null, null);
        }
        else if (typeof likelyDate != "string") {
            throw new Error("likelyDate must be a string or null");
        }
        let likelyDay = null;
        let likelyMonth = null;
        let likelyYear = null;
        const [parsedDate, numFields] = this.getCleanedDateAndNumFields(likelyDate);
        if (numFields >= 1) {
            if (parsedDate instanceof AncientDateTime) {
                likelyYear = parsedDate.getFullYear();
                likelyMonth = parsedDate.getMonth();
                likelyDay = parsedDate.getDate();
            }
            else {
                if (parsedDate.getFullYear() !== 9999) {
                    likelyYear = parsedDate.getFullYear();
                }
                if (numFields >= 2) {
                    likelyMonth = parsedDate.getMonth() + 1; // Convert from 0-indexed to 1-indexed
                }
                if (numFields === 3) {
                    likelyDay = parsedDate.getDate();
                }
            }
        }
        return new FlexibleDate(likelyDay, likelyMonth, likelyYear);
    }
    /**Creates a FlexibleDate object from a formal date string.
    *
    * @param formalDate (str): an EDTF (Extended Date/Time Format) string such as:
            "+1526-01-01T00:00:00Z/+2020-12-31T23:59:59Z" (date range)
            "+1910/+1910" (year range)
            "+1910-01-01T00:00:00Z/+1910-12-31T23:59:59Z" (date range within year)
    * @throws ValueError: raised if input is not a valid EDTF string
    * @returns FlexibleDate: the FlexibleDate object parsed from the EDTF string
    */
    createFlexibleDateFromFormalDate(formalDate) {
        if (typeof formalDate !== 'string') {
            throw new Error('formalDate must be a string'); // should never happen
        }
        try {
            // Clean the input - remove '+' signs which aren't standard EDTF
            const cleanedDate = formalDate.replace(/\+/g, '');
            const edtfObj = edtf.parse(cleanedDate);
            // Extract year, month, day from the edtf object
            // The edtf package returns { type: 'Date', level: 0, values: [year, month-1, day] }
            // Note: month is 0-indexed in JavaScript, but we want 1-indexed like Python
            let likelyYear = null;
            let likelyMonth = null;
            let likelyDay = null;
            if (edtfObj && edtfObj.values && Array.isArray(edtfObj.values)) {
                const [year, month, day] = edtfObj.values;
                // Handle year (same logic as Python version)
                likelyYear = (year !== undefined && year !== 9999) ? year : null;
                // Handle month (convert from 0-indexed to 1-indexed, same logic as Python)
                likelyMonth = (month !== undefined && (month !== 0 || cleanedDate.split('-').length > 1)) ? month + 1 : null;
                // Handle day (same logic as Python version)
                likelyDay = (day !== undefined && (day !== 1 || cleanedDate.split('-').length > 2)) ? day : null;
            }
            // Handle date ranges - if it's a year range like "1910/1920", only keep year
            if (cleanedDate.includes('/')) {
                const parts = cleanedDate.split('/');
                if (parts.length === 2) {
                    const startPart = parts[0];
                    const endPart = parts[1];
                    if (startPart.length === 4 && endPart.length === 4 && !isNaN(parseInt(startPart)) && !isNaN(parseInt(endPart))) {
                        likelyMonth = null;
                        likelyDay = null;
                    }
                }
            }
            return new FlexibleDate(likelyYear, likelyMonth, likelyDay);
        }
        catch (error) {
            throw new Error(`Unable to parse EDTF string "${formalDate}": ${error}`);
        }
    }
    compareDates(dateToCompare) {
        let score = 100;
        if (this.valueOf() && dateToCompare.valueOf()) {
            const thisDateValues = [this.likelyYear, this.likelyMonth, this.likelyDay];
            const dateToCompareValues = [dateToCompare.likelyYear, dateToCompare.likelyMonth, dateToCompare.likelyDay];
            const sharedNonNullCount = thisDateValues.reduce((count, val, index) => (val !== null && val !== undefined && dateToCompareValues[index] !== null && dateToCompareValues[index] !== undefined) ? count + 1 : count, 0);
            const weight = sharedNonNullCount > 0 ? 1 / sharedNonNullCount : 1;
            let allScores = [];
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
            score = Math.round((allScores.reduce((sum, score) => sum + score, 0)) * 100);
        }
        return score;
    }
    chooseMostReasonableValue(values) {
        const filteredValues = values.filter((v) => v !== null && v !== undefined && !isNaN(v));
        if (filteredValues.length === 0) {
            return null;
        }
        const counter = new Map();
        filteredValues.forEach(value => {
            counter.set(value, (counter.get(value) || 0) + 1);
        });
        const totalCount = Array.from(counter.values()).reduce((sum, count) => sum + count, 0);
        const scores = new Map();
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
    combineFlexibleDates(dates) {
        // If there's only one date, return it as is
        if (dates.length === 1) {
            return dates[0];
        }
        const allYears = dates.map(date => date.likelyYear);
        const allMonths = dates.map(date => date.likelyMonth);
        const allDays = dates.map(date => date.likelyDay);
        const year = allYears.length > 0 ? this.chooseMostReasonableValue(allYears) : null;
        const month = allMonths.length > 0 ? this.chooseMostReasonableValue(allMonths) : null;
        const day = allDays.length > 0 ? this.chooseMostReasonableValue(allDays) : null;
        return new FlexibleDate(day, month, year);
    }
    parseWithDateUtil(likelyDate) {
        let parsedDate = new Date('0001-01-01');
        let numFields = 0;
        try {
            const date = likelyDate.trim();
            if (/^0{0,2}[0-9]{2}$/.test(date)) {
                throw new Error('Date does not work for years 0000 and 0099');
            }
            if (date.toLowerCase().includes('bc')) {
                throw new Error('Date does not work for negative years');
            }
            parsedDate = new Date(date);
            if (parsedDate.getFullYear() === 9999) {
                numFields += 1;
            }
            numFields += date.split(/\s+/).length;
        }
        catch (error) {
            if (error instanceof Error) {
                console.error(error.message);
            }
        }
        return [parsedDate, numFields];
    }
    gleanYearMonthDay(text) {
        const acceptableCombos = new Set();
        acceptableCombos.add([null, null, null]);
        // Find valid years (4-digit years up to the current year)
        const currentYear = new Date().getFullYear();
        const validYears = (text.match(/[-]?(?=(\d{4}))/g) || [])
            .filter(year => parseInt(year) <= currentYear);
        const validYearsAndInstances = this.getStringsAndInstances(validYears);
        for (const [year, i] of validYearsAndInstances) {
            acceptableCombos.add([year, null, null]);
            // Remove the year and find valid months
            const textA = this.substituteIthInstance(text, year, ' ', i).trim().replace(/\s{2,}/g, ' ');
            const validMonths = this.findAllMatches(textA, ['[1-9]', '0[1-9]', '1[0-9]', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']);
            const validMonthsAndInstances = this.getStringsAndInstances(validMonths);
            for (const [month, i] of validMonthsAndInstances) {
                acceptableCombos.add([year, month, null]);
                // Remove the month and find valid days
                const textB = this.substituteIthInstance(textA, month, ' ', i).trim().replace(/\s{2,}/g, ' ');
                const validDays = this.findAllMatches(textB, ['[1-9]', '0[1-9]', '1[0-9]', '2[0-9]', '3[01]']);
                for (const day of validDays) {
                    const combo = [year, month, day];
                    try {
                        (0, date_fns_1.parse)(`${year}-${month}-${day}`, 'yyyy-M-d', new Date());
                        acceptableCombos.add(combo);
                    }
                    catch (error) {
                        // Ignore invalid dates
                        console.log(error);
                    }
                }
            }
        }
        // Scoring function
        const keyFunc = (t) => [
            t.reduce((sum, x) => sum + (x ? x.length : 0), 0), // Primary ranking: total characters in non-null elements
            t.filter(x => x !== null).length // Secondary ranking: count of non-null elements
        ];
        const scores = new Map([...acceptableCombos].map(option => [option, keyFunc(option)]));
        const maxScore = Math.max(...Array.from(scores.values()).map(s => s[0]));
        const bestOptions = [...scores.entries()]
            .filter(([, score]) => score[0] === maxScore)
            .map(([option]) => option);
        // Merging best options
        for (let i = 0; i < bestOptions.length; i++) {
            for (let j = i + 1; j < bestOptions.length; j++) {
                let [yearA, monthA, dayA] = bestOptions[i];
                const [yearB, monthB, dayB] = bestOptions[j];
                yearA = yearA === yearB ? yearA : null;
                if (monthA !== monthB || dayA !== dayB) {
                    monthA = null;
                    dayA = null;
                }
                bestOptions[i] = [yearA, monthA, dayA];
                bestOptions[j] = [yearA, monthA, dayA];
            }
        }
        return bestOptions[0];
    }
    getStringsAndInstances(stringList) {
        const countDict = {};
        const result = [];
        for (const str of stringList) {
            countDict[str] = (countDict[str] || 0) + 1;
            result.push([str, countDict[str] - 1]);
        }
        return result;
    }
    substituteIthInstance(text, pattern, replacement, i) {
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
    findAllMatches(text, regexPatterns) {
        let allMatches = [];
        for (const pattern of regexPatterns) {
            allMatches = allMatches.concat(text.match(new RegExp(pattern, 'gi')) || []);
        }
        return allMatches;
    }
    getCleanedDateAndNumFields(dateString) {
        const date = this.cleanDate(dateString);
        if (/^-?[0-9]{4}$/.test(date)) {
            return [new AncientDateTime(parseInt(date, 10)), 1];
        }
        let [parsedDate, numFields] = this.parseWithDateUtil(date);
        if (numFields !== 0) {
            return [parsedDate, numFields];
        }
        const [year, month, day] = this.gleanYearMonthDay(date);
        if (year == null) {
            return [parsedDate, numFields];
        }
        const reconstructedDate = `${year} ${month || ""} ${day || ""}`.trim();
        [parsedDate, numFields] = this.parseWithDateUtil(reconstructedDate);
        return [parsedDate, numFields];
    }
    cleanDate(dateString) {
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
        date = date.replace('/', ' ');
        date = date.replace(',', ' ');
        date = date.replace('.', ' ');
        date = date.replace('"', ' ');
        date = date.replace("'", ' ');
        date = date.replace('-', ' ');
        date = date.replace('_', ' ');
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
        }
        else if (/^[0-9]{2}( bc)?$/.test(date)) {
            date = `00${date}`;
        }
        else if (/^0[0-9]{2}( bc)?$/.test(date)) {
            date = `0${date}`;
        }
        if (/[0-9]{4} bc/.test(date)) {
            date = `-${date}`;
        }
        date = date.replace('bc', '').trim();
        return date;
    }
    valueOf() {
        //eslint-disable-next-line
        const isNull = (val) => val === null || (typeof val === 'number' && isNaN(val));
        return !(isNull(this.likelyDay) && isNull(this.likelyMonth) && isNull(this.likelyYear));
    }
}
exports.default = FlexibleDate;
//# sourceMappingURL=FlexibleDateTS.js.map