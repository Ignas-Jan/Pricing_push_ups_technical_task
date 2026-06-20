SELECT *   -- for sample data
FROM public.pricing_data pd  
ORDER BY random();


SELECT *  -- checked the duplicated rows
FROM (
    SELECT *,
           COUNT(*) OVER (PARTITION BY category_3, number_of_listings, avg_listing_price_eur, revenue_from_push_ups) AS duplicate_count
    FROM public.pricing_data
) subquery
WHERE duplicate_count > 1
ORDER BY category_3, number_of_listings, avg_listing_price_eur, revenue_from_push_ups;


SELECT COUNT(*) AS total_records
FROM public.pricing_data pd;


UPDATE public.pricing_data
SET revenue_from_push_ups = 0.0
WHERE revenue_from_push_ups = 'NULL';


ALTER TABLE public.pricing_data 
ALTER COLUMN revenue_from_push_ups TYPE FLOAT
USING revenue_from_push_ups::FLOAT;


SELECT pd.category_2, 
       SUM(pd.number_of_listings) AS total_listings,
       AVG(pd.avg_listing_price_eur) AS average_category_price_eur,
       SUM(pd.revenue_from_push_ups::FLOAT) AS total_revenue
FROM public.pricing_data pd
GROUP BY pd.category_2
ORDER BY total_revenue DESC;


SELECT SUM(number_of_listings) AS total_listings
FROM public.pricing_data pd;


SELECT 
FROM public.pricing_data pd 
WHERE UPPER(pd.category_2) = 'WOMENS'
ORDER BY CAST(pd.revenue_from_push_ups AS FLOAT) DESC;

SELECT * 
FROM public.pricing_data pd 
WHERE pd.category_2 = 'NULL' OR pd.category_3 = 'NULL';

SELECT pd.number_of_listings,
	   pd.avg_listing_price_eur,
	   pd.revenue_from_push_ups,
	   ((pd.revenue_from_push_ups::FLOAT) / 2 / pd.number_of_listings * 100) AS adoption_rate
FROM public.pricing_data pd
WHERE pd.category_2 = 'GIRLS_CLOTHING' AND pd.category_3 = 'FOR_BABIES';
