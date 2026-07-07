#!/usr/bin/env node

import FlexibleDate from './FlexibleDateTS';
import { PyScriptTestBridge } from 'pyscripttestutils';

function serializeFlexibleDate(fd: FlexibleDate): any {
    if (fd.constructor.name === "FlexibleDate") {
        return {
            likelyYear: fd.likelyYear,
            likelyMonth: fd.likelyMonth,
            likelyDay: fd.likelyDay,
        };
    }
    return fd;
}

function deserializeFlexibleDate(data: any): FlexibleDate {
    if ("likelyDay" in data &&
        "likelyMonth" in data &&
        "likelyYear" in data) {
        return new FlexibleDate(data.likelyDay, data.likelyMonth, data.likelyYear);
    }
    return data;
}

const bridge = new PyScriptTestBridge(serializeFlexibleDate, deserializeFlexibleDate);

bridge.addMethod("createFlexibleDate", (args) => new FlexibleDate(args[0]));

bridge.addMethod("createFlexibleDateFromFormalDate", (args) => {
    return FlexibleDate.createFlexibleDateFromFormalDate(args[0]);
});

bridge.addMethod("compareDates", (args) => args[0].compareDates(args[1]));

bridge.addMethod("combineFlexibleDates", (args) => {
    return FlexibleDate.combineFlexibleDates(args as FlexibleDate[]);
});

bridge.addMethod("FlexibleDate.toString", (args) => args[0].toString());

bridge.addMethod("FlexibleDate.valueOf", (args) => args[0].valueOf());

bridge.addMethod("FlexibleDate.inspect", (args) => args[0].inspect());

bridge.addMethod("FlexibleDate.equals", (args) => args[0].equals(args[1]));

bridge.addMethod("testValidator", (args) => {
    const [x] = args;
    if (x instanceof FlexibleDate) {
        return x;
    }
    return "ValueError";
});

if (require.main === module) {
    bridge.runCli(process.argv.slice(2));
}
