#!/usr/bin/env node

import FlexibleDate from './FlexibleDateTS';

interface TestRequest {
    method: string;
    args: any[];
}

interface TestResponse {
    success: boolean;
    result?: any;
    error?: string;
}

function serializeFlexibleDate(fd: FlexibleDate): any {
    return {
        likelyYear: fd.likelyYear,
        likelyMonth: fd.likelyMonth,
        likelyDay: fd.likelyDay
    };
}

function deserializeFlexibleDate(data: any): FlexibleDate {
    return new FlexibleDate(data.likelyDay, data.likelyMonth, data.likelyYear);
}

function processRequest(request: TestRequest): TestResponse {
    try {
        switch (request.method) {
            case 'createFlexibleDate':
                const [dateString] = request.args;
                const fd = new FlexibleDate(dateString);
                return {
                    success: true,
                    result: serializeFlexibleDate(fd)
                };

            case 'createFlexibleDateFromFormalDate':
                const [formalDateString] = request.args;
                const fdFromFormal = new FlexibleDate(null, null, null);
                const result = fdFromFormal.createFlexibleDateFromFormalDate(formalDateString);
                return {
                    success: true,
                    result: serializeFlexibleDate(result)
                };

            case 'compareDates':
                const [date1Data, date2Data] = request.args;
                const fd1 = deserializeFlexibleDate(date1Data);
                const fd2 = deserializeFlexibleDate(date2Data);
                const score = fd1.compareDates(fd2);
                return {
                    success: true,
                    result: score
                };

            case 'combineFlexibleDates':
                const [datesData] = request.args;
                const dates = datesData.map((d: any) => deserializeFlexibleDate(d));
                const fd_temp = new FlexibleDate(null, null, null);
                const combined = fd_temp.combineFlexibleDates(dates);
                return {
                    success: true,
                    result: serializeFlexibleDate(combined)
                };

            case 'toString':
                const [fdData] = request.args;
                const fdForString = deserializeFlexibleDate(fdData);
                return {
                    success: true,
                    result: fdForString.toString()
                };

            case 'valueOf':
                const [fdDataValue] = request.args;
                const fdForValue = deserializeFlexibleDate(fdDataValue);
                return {
                    success: true,
                    result: fdForValue.valueOf()
                };

            case 'testBool':
                const [fdDataBool] = request.args;
                const fdForBool = deserializeFlexibleDate(fdDataBool);
                return {
                    success: true,
                    result: fdForBool.valueOf()
                };

            case 'testStr':
                const [fdDataStr] = request.args;
                const fdForStr = deserializeFlexibleDate(fdDataStr);
                return {
                    success: true,
                    result: fdForStr.toString()
                };

            case 'testRepr':
                const [fdDataRepr] = request.args;
                const fdForRepr = deserializeFlexibleDate(fdDataRepr);
                return {
                    success: true,
                    result: fdForRepr.inspect()
                };

            case 'testValidator':
                try {
                    const [fdDataValidator] = request.args;
                    const fdForValidator = deserializeFlexibleDate(fdDataValidator);
                    return {
                        success: true,
                        result: serializeFlexibleDate(fdForValidator)
                    };
                } catch (error) {
                    return {
                        success: true,
                        result: `ValidationError: ${error instanceof Error ? error.message : String(error)}`
                    };
                }

            default:
                return {
                    success: false,
                    error: `Unknown method: ${request.method}`
                };
        }
    } catch (error) {
        return {
            success: false,
            error: error instanceof Error ? error.message : String(error)
        };
    }
}

// Main execution
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.error('Usage: node test_bridge.js <json_request>');
        process.exit(1);
    }

    try {
        const request: TestRequest = JSON.parse(args[0]);
        const response = processRequest(request);
        console.log(JSON.stringify(response));
    } catch (error) {
        const errorResponse: TestResponse = {
            success: false,
            error: error instanceof Error ? error.message : String(error)
        };
        console.log(JSON.stringify(errorResponse));
    }
}

export { processRequest, TestRequest, TestResponse };
