#!/usr/bin/env node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.processRequest = processRequest;
const FlexibleDateTS_1 = __importDefault(require("./FlexibleDateTS"));
function serializeFlexibleDate(fd) {
    return {
        likelyYear: fd.likelyYear,
        likelyMonth: fd.likelyMonth,
        likelyDay: fd.likelyDay
    };
}
function deserializeFlexibleDate(data) {
    return new FlexibleDateTS_1.default(data.likelyDay, data.likelyMonth, data.likelyYear);
}
function processRequest(request) {
    try {
        switch (request.method) {
            case 'createFlexibleDate':
                const [dateString] = request.args;
                const fd = new FlexibleDateTS_1.default(dateString);
                return {
                    success: true,
                    result: serializeFlexibleDate(fd)
                };
            case 'createFlexibleDateFromFormalDate':
                const [formalDateString] = request.args;
                const fdFromFormal = new FlexibleDateTS_1.default(null, null, null);
                const result = fdFromFormal.createFlexibleDateFromFormalDate(formalDateString);
                return {
                    success: true,
                    result: serializeFlexibleDate(result)
                };
            case 'compareTwoDates':
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
                const dates = datesData.map((d) => deserializeFlexibleDate(d));
                const fd_temp = new FlexibleDateTS_1.default(null, null, null);
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
            default:
                return {
                    success: false,
                    error: `Unknown method: ${request.method}`
                };
        }
    }
    catch (error) {
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
        const request = JSON.parse(args[0]);
        const response = processRequest(request);
        console.log(JSON.stringify(response));
    }
    catch (error) {
        const errorResponse = {
            success: false,
            error: error instanceof Error ? error.message : String(error)
        };
        console.log(JSON.stringify(errorResponse));
    }
}
//# sourceMappingURL=test_bridge.js.map