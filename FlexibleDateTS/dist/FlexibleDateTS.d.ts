type YearMonthDay = [string | null, string | null, string | null];
export default class FlexibleDate {
    likelyYear?: number | null;
    likelyMonth?: number | null;
    likelyDay?: number | null;
    constructor(likelyDate: string | null);
    constructor(likelyDay: number | null, likelyMonth: number | null, likelyYear: number | null);
    toString(): string;
    inspect(): string;
    createFlexibleDate(likelyDate: string | null | undefined): FlexibleDate;
    /**Creates a FlexibleDate object from a formal date string.
    *
    * @param formalDate (str): an EDTF (Extended Date/Time Format) string such as:
            "+1526-01-01T00:00:00Z/+2020-12-31T23:59:59Z" (date range)
            "+1910/+1910" (year range)
            "+1910-01-01T00:00:00Z/+1910-12-31T23:59:59Z" (date range within year)
    * @throws ValueError: raised if input is not a valid EDTF string
    * @returns FlexibleDate: the FlexibleDate object parsed from the EDTF string
    */
    createFlexibleDateFromFormalDate(formalDate: string): FlexibleDate;
    compareDates(dateToCompare: FlexibleDate): number;
    private chooseMostReasonableValue;
    combineFlexibleDates(dates: FlexibleDate[]): FlexibleDate;
    private parseWithDateUtil;
    gleanYearMonthDay(text: string): YearMonthDay;
    private getStringsAndInstances;
    private substituteIthInstance;
    private findAllMatches;
    private getCleanedDateAndNumFields;
    private cleanDate;
    valueOf(): boolean;
}
export {};
//# sourceMappingURL=FlexibleDateTS.d.ts.map