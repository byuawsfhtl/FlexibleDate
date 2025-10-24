declare module 'edtf' {
  export function parse(edtfString: string): {
    type: string;
    level: number;
    values: number[];
  };
}
