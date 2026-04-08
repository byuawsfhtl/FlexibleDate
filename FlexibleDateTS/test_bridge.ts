#!/usr/bin/env node

import FlexibleDate from './FlexibleDateTS';
import { PyScriptTestBridge } from 'pyscripttestutils';

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

const bridge = new PyScriptTestBridge(serializeFlexibleDate, deserializeFlexibleDate);

bridge.addMethod('createFlexibleDate', (args: any[]) => {
    const [dateString] = args;
    return new FlexibleDate(dateString);
});

bridge.addMethod('createFlexibleDateFromFormalDate', (args: any[]) => {
    const [formalDateString] = args;
    const fdFromFormal = new FlexibleDate(null, null, null);
    return fdFromFormal.createFlexibleDateFromFormalDate(formalDateString);
});

bridge.addMethod('compareDates', (args: any[]) => {
    const [date1, date2] = args;
    return date1.compareDates(date2);
});

bridge.addMethod('combineFlexibleDates', (args: any[]) => {
    const [dates] = args;
    const fd_temp = new FlexibleDate(null, null, null);
    return fd_temp.combineFlexibleDates(dates);
});

bridge.addMethod('toString', (args: any[]) => {
    const [fd] = args;
    return fd.toString();
});

bridge.addMethod('inspect', (args: any[]) => {
    const [fd] = args;
    return fd.inspect();
});

bridge.addMethod('valueOf', (args: any[]) => {
    const [fd] = args;
    return fd.valueOf();
});

bridge.addMethod('equals', (args: any[]) => {
    const [date1, date2] = args;
    return date1.equals(date2);
});

bridge.addMethod('testValidator', (args: any[]) => {
    const [fd] = args;
    return deserializeFlexibleDate(fd);
});

// Main execution
if (require.main === module) {
    bridge.runCli();
}
