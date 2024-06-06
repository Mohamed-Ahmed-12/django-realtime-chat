'''
this file used to run inside all templates 
note : there is config in settings.py in templates > options > context_processor
'''

from . models import ChatRoom

def my_variable_context_processor(request):
    my_chats = ChatRoom.objects.filter(member = request.user.id).order_by('last_update')
    msg = []
    count_unread = []
    for i in my_chats:
        msg.append(i.chat_chatmessage_related.last())
        count_unread.append(i.chat_chatmessage_related.filter(read=False).count)
    my_chats = zip(my_chats , msg , count_unread)
    return {'chats':my_chats}