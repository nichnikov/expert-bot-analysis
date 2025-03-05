select date_trunc('month', c.created) AS txn_month, c.product_id as pub, count(distinct(c.user_id)) as u_count from online_helper__chats.chats c
group by txn_month, pub
