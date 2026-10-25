-- Run against smartcart.db after python/analyze.py has loaded the sample CSV.

-- 1. Event volume
SELECT event_name, COUNT(*) AS event_count
FROM events
GROUP BY event_name
ORDER BY event_count DESC;

-- 2. Unique users by event (descriptive; does not guarantee ordered progression)
SELECT event_name, COUNT(DISTINCT user_id) AS unique_users
FROM events
GROUP BY event_name
ORDER BY unique_users DESC;

-- 3. Most-viewed products
SELECT product_name, COUNT(*) AS product_views
FROM events
WHERE event_name = 'view_item'
GROUP BY product_name
ORDER BY product_views DESC
LIMIT 5;

-- 4. Traffic source summary
SELECT
  source,
  COUNT(DISTINCT user_id) AS users,
  COUNT(DISTINCT CASE WHEN event_name = 'purchase' THEN user_id END) AS purchasers
FROM events
GROUP BY source
ORDER BY purchasers DESC;

-- 5. Users who added to cart but have no purchase event anywhere in this sample
-- This is an illustrative user-level query. A production query should define a session/time window.
SELECT DISTINCT c.user_id
FROM events c
WHERE c.event_name = 'add_to_cart'
AND NOT EXISTS (
  SELECT 1 FROM events p
  WHERE p.user_id = c.user_id AND p.event_name = 'purchase'
);

-- 6. Sessions reaching each funnel event
SELECT event_name, COUNT(DISTINCT session_id) AS sessions
FROM events
WHERE event_name IN ('view_item','add_to_cart','begin_checkout','purchase')
GROUP BY event_name;
