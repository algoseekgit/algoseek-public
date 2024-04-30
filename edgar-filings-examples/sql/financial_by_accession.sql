
-- @block: financials_by_accession
-- Purpose: Query financials by accession number.
SELECT f.entity_ticker AS ticker,
    f.report_document_type as document_type,
    formatDateTime(f.report_period_end_date, '%Y-%m-%d') as period_end,
    f.relationship_tree_sequence as sequence,
    f.relationship_tree_depth as depth,
    f.network_role_description as statement,
    f.relationship_target_label as label,
    f.period_fiscal_year as year,
    f.period_fiscal_period as period,
    f.fact_value as value
FROM financials f
WHERE f.report_accession IN (:accession_numbers)
ORDER BY f.network_role_description ASC,
    f.relationship_tree_sequence ASC,
    f.relationship_tree_depth ASC;