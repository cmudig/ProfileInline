/**
 * Provides mappings from duckdb's data types to conceptual types we use in the application:
 * CATEGORICALS, NUMERICS, and TIMESTAMPS.
 */

export const INTEGERS = new Set([
    'BIGINT',
    'HUGEINT',
    'SMALLINT',
    'INTEGER',
    'TINYINT',
    'UBIGINT',
    'UINTEGER',
    'UTINYINT',
    'INT1',
    'INT4',
    'INT',
    'SIGNED',
    'SHORT'
]);

export const FLOATS = new Set([
    'DOUBLE',
    'DECIMAL',
    'FLOAT8',
    'NUMERIC',
    'FLOAT'
]);

export const NUMERICS = new Set([...INTEGERS, ...FLOATS]);
export const BOOLEANS = new Set(['BOOLEAN', 'BOOL', 'LOGICAL']);
export const TIMESTAMPS = new Set(['TIMESTAMP', 'TIME', 'DATETIME', 'DATE']);
export const INTERVALS = new Set(['INTERVAL']);
export const CATEGORICALS = new Set([
    'BYTE_ARRAY',
    'VARCHAR',
    'CHAR',
    'BPCHAR',
    'TEXT',
    'STRING'
]);

interface IColorTokens {
    textClass: string;
    bgClass: string;
    vizFillClass: string;
    vizStrokeClass: string;
}

export const CATEGORICAL_TOKENS: IColorTokens = {
    textClass: 'text-sky-800',
    bgClass: 'bg-sky-200',
    vizFillClass: 'fill-sky-800',
    vizStrokeClass: 'fill-sky-800'
};

export const NUMERIC_TOKENS: IColorTokens = {
    textClass: 'text-red-800',
    bgClass: 'bg-red-200',
    vizFillClass: 'fill-red-300',
    vizStrokeClass: 'stroke-red-300'
};

export const TIMESTAMP_TOKENS: IColorTokens = {
    textClass: 'text-teal-800',
    bgClass: 'bg-teal-200',
    vizFillClass: 'fill-teal-500',
    vizStrokeClass: 'stroke-teal-500'
};

export const INTERVAL_TOKENS: IColorTokens = TIMESTAMP_TOKENS;

function setTypeTailwindStyles(
    list: string[],
    // a tailwind class, for now.
    colorTokens: IColorTokens
) {
    return list.reduce((acc, v) => {
        acc[v] = { ...colorTokens };
        return acc;
    }, {});
}

export const DATA_TYPE_COLORS = {
    ...setTypeTailwindStyles(Array.from(CATEGORICALS), CATEGORICAL_TOKENS),
    ...setTypeTailwindStyles(Array.from(NUMERICS), NUMERIC_TOKENS),
    ...setTypeTailwindStyles(Array.from(TIMESTAMPS), TIMESTAMP_TOKENS),
    ...setTypeTailwindStyles(Array.from(INTERVALS), INTERVAL_TOKENS),
    ...setTypeTailwindStyles(Array.from(BOOLEANS), CATEGORICAL_TOKENS)
};
