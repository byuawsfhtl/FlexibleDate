#!/usr/bin/env node
interface TestRequest {
    method: string;
    args: any[];
}
interface TestResponse {
    success: boolean;
    result?: any;
    error?: string;
}
declare function processRequest(request: TestRequest): TestResponse;
export { processRequest, TestRequest, TestResponse };
//# sourceMappingURL=test_bridge.d.ts.map