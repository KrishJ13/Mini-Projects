CREATE TABLE IF NOT EXISTS urls (
    id  SERIAL PRIMARY KEY,
    short_code  VARCHAR(16) UNIQUE NOT NULL,
    long_url    VARCHAR(2048) NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Creating an index here reduces lookup time to O(logn) instead of sequential search by short code O(n)
CREATE INDEX IF NOT EXISTS idx_urls_short_code ON urls (short_code);


