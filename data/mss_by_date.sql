select * 
from online_helper__chats.messages m join online_helper__chats.chats c on m.chat_id = c.id   
WHERE  c.created >= '2025-3-10'::date AND c.created <= '2025-3-16'::date and m.text not like '%AUTOTEST%' 
and m.discriminator  in ('UserMessage', 'UserNewsPositiveReactionMessage', 'UserMobileMessage', 'UserFileMessage', 
'AutoGoodbyeMessage', 'AutoHello2Message',  'AutoHelloMessage', 'AutoHelloNewsMessage', 'AutoHelloOfflineMessage', 
'AutoRateMessage', 'HotlineNotificationMessage', 'MLRoboChatMessage', 'NewsAutoMessage', 'OperatorMessage')
