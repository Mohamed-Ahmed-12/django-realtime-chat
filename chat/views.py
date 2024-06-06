from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import ChatRoom , VideoCall
from django.db.models import Value , CharField

@login_required(redirect_field_name='login',login_url='/auth/login/')
def room(request , room_name=None):
    if room_name is not None:
        room_type = 'dm'
        try:
            room_ = ChatRoom.objects.get(type = room_type , name = room_name)
            if request.user in room_.member.all():
                for mem in room_.member.all():
                    if not mem == request.user :
                        user = mem
                
                '''
                annotate add msg_type attribute to the queryset to identify the type of object in template
                ex in template:
                    {% for message in messages %}
                        <p>{{ message }}</p>
                        <p>From model: {{ message.msg_type }}</p>
                    {% endfor %}
                '''
                text_msg =  room_.chat_chatmessage_related.all().annotate(message_type=Value('text', output_field=CharField()))
                audio_msg = room_.chat_audiovideo_related.all().annotate(message_type=Value('audio_video', output_field=CharField()))
                messages = text_msg.union(audio_msg).order_by('timestamp')
                
                return render(request, "room.html", {"room_name": room_name, 'user':user , 'messages':messages})
        except:
            return render(request, "room.html")
    return render(request, "room.html")

def video_call(request ,room_name):
    try:
        room = ChatRoom.objects.get(name = room_name)
        if VideoCall.objects.filter(room = room , is_active = True).exists():
            call = VideoCall.objects.get(room = room , is_active = True)
        else:
            call = VideoCall.objects.create(room = room ,caller = request.user , is_active = True)
            call.save()
        return render(request , 'video.html' , {"room_name": room_name, "call":call}) 
    except:
        return render(request , 'room.html') 

