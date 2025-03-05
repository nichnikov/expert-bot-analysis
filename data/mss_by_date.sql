select * from online_helper__chats.messages m
WHERE  m.created >= '2025-1-1'::date and text not like '%AUTOTEST%'
limit 25000

