-- ================================================
-- COVID-19 Vaccination Equity Analysis
-- Data source: CDC vaccination data by demographics
-- ================================================

-- Query 1: Vaccination rates by race/ethnicity (most recent date)
SELECT 
    demographic_category,
    date,
    administered_dose1_pct_known AS dose1_pct,
    series_complete_pop_pct_known AS fully_vaxxed_pct
FROM vaccinations
WHERE demographic_category LIKE 'Race_eth_%'
    AND demographic_category NOT IN ('Race_eth_known', 'Race_eth_unknown')
    AND date = (SELECT MAX(date) FROM vaccinations)
ORDER BY fully_vaxxed_pct DESC;

-- Query 2: Vaccination gap between highest and lowest racial groups over time
SELECT 
    date,
    MAX(series_complete_pop_pct_known) AS highest_rate,
    MIN(series_complete_pop_pct_known) AS lowest_rate,
    MAX(series_complete_pop_pct_known) - MIN(series_complete_pop_pct_known) AS equity_gap
FROM vaccinations
WHERE demographic_category LIKE 'Race_eth_NH%'
    AND series_complete_pop_pct_known IS NOT NULL
    AND series_complete_pop_pct_known > 0
GROUP BY date
ORDER BY date;

-- Query 3: Age group comparison for completed vaccinations
SELECT
    demographic_category,
    date,
    series_complete_pop_pct AS fully_vaxxed_pct,
    booster_doses_vax_pct_agegroup AS booster_pct
FROM vaccinations
WHERE demographic_category LIKE 'Ages_%'
    AND demographic_category NOT IN ('Age_known', 'Age_unknown')
    AND date = (SELECT MAX(date) FROM vaccinations)
ORDER BY fully_vaxxed_pct DESC;

-- Query 4: Gender comparison
SELECT
    demographic_category,
    date,
    administered_dose1_pct AS dose1_pct,
    series_complete_pop_pct AS fully_vaxxed_pct,
    booster_doses_vax_pct_agegroup AS booster_pct
FROM vaccinations
WHERE demographic_category LIKE 'Sex_%'
    AND demographic_category NOT IN ('Sex_known', 'Sex_unknown')
    AND date = (SELECT MAX(date) FROM vaccinations);

-- Query 5: Booster uptake disparity by race
SELECT
    demographic_category,
    date,
    series_complete_pop_pct_known AS fully_vaxxed_pct,
    booster_doses_pop_pct_known AS booster_pct,
    ROUND(series_complete_pop_pct_known - booster_doses_pop_pct_known, 1) AS booster_dropoff
FROM vaccinations
WHERE demographic_category LIKE 'Race_eth_NH%'
    AND date = (SELECT MAX(date) FROM vaccinations)
ORDER BY booster_dropoff DESC;
