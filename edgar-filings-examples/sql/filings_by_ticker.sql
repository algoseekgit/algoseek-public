-- @block : reports per entity_ticker
-- Purpose: This query returns the reports for a list of entities.
SELECT DISTINCT r.source_report_identifier as accession_number,
    r.properties ['document_type'] as document_type,
    r.reporting_period_end_date as period_date
FROM reports r
    JOIN entities e ON e.entity_id = r.entity_id
WHERE e.entity_ticker in (:tickers)
ORDER BY r.reporting_period_end_date DESC;