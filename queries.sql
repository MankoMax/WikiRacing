-- Топ 5 найпопулярніших статей (ті що мають найбільшу кількість посилань на себе)
SELECT title, COUNT(title) as links_to_self
FROM wiki
GROUP BY title
ORDER BY links_to_self DESC
LIMIT 5;


-- Топ 5 статей з найбільшою кількістю посилань на інші статті
WITH cte as (
  SELECT parent_id, COUNT(title) as outbound_links, ROW_NUMBER() OVER (ORDER BY COUNT(title) DESC) AS rn
  FROM wiki
  GROUP BY parent_id
)
SELECT title, outbound_links FROM cte
JOIN wiki w ON cte.parent_id = w.id
WHERE rn <= 5
ORDER BY outbound_links DESC;


--  Для заданної статті знайти середню кількість потомків другого рівня
WITH RECURSIVE descendants(id, title, parent_id) AS (
    SELECT id, title, parent_id FROM wiki WHERE title = 'Україна'
    UNION
    SELECT w.id, w.title, w.parent_id FROM wiki w
    JOIN descendants d ON d.id = w.parent_id
)
SELECT AVG(avg_second_level_children) as avg_second_level_children
FROM (
  SELECT parent_id, COUNT(*) as avg_second_level_children
  FROM descendants
  GROUP BY parent_id
) as temp;