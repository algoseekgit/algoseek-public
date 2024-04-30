-- @block: shares_outstanding
-- Purpose: This query returns the shares outstanding for a list of entities.
SELECT formatDateTime(t.report_period_end_date, '%Y-%m-%d') as period_date,
    t.period_fiscal_year as fiscal_year,
    t.period_fiscal_period as fiscal_period,
    t.fact_value as value
FROM (
        SELECT *,
            ROW_NUMBER() OVER(
                PARTITION BY period_fiscal_year,
                period_fiscal_period
                ORDER BY report_period_end_date DESC
            ) as rn
        FROM financials f
        WHERE f.entity_ticker IN (:entities)
            AND f.relationship_target_name = 'CommonStockSharesOutstanding'
    ) t
WHERE t.rn = 1
ORDER BY t.report_period_end_date;