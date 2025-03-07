select date_trunc('year', c.created) AS txn_year, c.product_id as pub, count(distinct(c.user_id)) as u_count from online_helper__chats.chats c
WHERE c.user_id IN (SELECT online_helper__chats.chat_user_info cui WHERE cui.access_type = 1) 
group by txn_year, pub
