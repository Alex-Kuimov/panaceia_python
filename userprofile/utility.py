import re


class OneInputField:
    # add
    def add(self, obj, request, pref):
        post_list = []
        model_list = []

        for key in request.POST:
            if key.find(pref + '[') != -1:
                post_list.append(key)

        for key in obj:
            name = pref + '[{}]'.format(key.id)
            model_list.append(name)

        for item in post_list:
            if not item in model_list:
                if request.POST[item] != '':
                    index = re.sub(r'[^0-9.]+', r'', item)
                    instance = self.objects.create(title=request.POST[pref+'[' + index + ']'], content_id=request.user.id)
                    obj.user = instance

    # update
    def update(self, obj, request, pref):
        for item in request.POST:
            if item.find(pref + '[') != -1:
                for i in obj:
                    name = pref + '[{}]'.format(i.id)
                    if item == name:
                        i.title = request.POST[name]
                        i.save()

    # remove
    def remove(self, obj, request, pref):
        post_list = []
        model_list = []

        for key in request.POST:
            if key.find(pref + '[') != -1:
                post_list.append(key)

        for key in obj:
            name = pref + '[{}]'.format(key.id)
            model_list.append(name)

        for item in model_list:
            if not item in post_list:
                index = re.sub(r'[^0-9.]+', r'', item)
                instance = self.objects.get(id=index)
                instance.delete()


class TwoInputField:
    # add
    def add(self, obj, request, pref1, pref2):
        post_list = []
        model_list = []

        for key in request.POST:
            if key.find(pref1 + '[') != -1:
                post_list.append(key)

        for key in obj:
            name = pref1 + '[{}]'.format(key.id)
            model_list.append(name)

        for item in post_list:
            if not item in model_list:
                if request.POST[item] != '':
                    index = re.sub(r'[^0-9.]+', r'', item)
                    instance = self.objects.create(years=request.POST[pref2+'[' + index + ']'], name=request.POST[pref1 + '[' + index + ']'], content_id=request.user.id)
                    obj.user = instance

    # update
    def update(self, obj, request, fields):

        for item in request.POST:
            for key in fields.keys():
                if item.find(key + '[') != -1:
                    for i in obj:
                        name = key + '[{}]'.format(i.id)
                        if item == name:
                            val = fields.get(key)
                            setattr(i, val, request.POST[name])
                            i.save()

    # remove
    def remove(self, obj, request, pref):
        post_list = []
        model_list = []

        for key in request.POST:
            if key.find(pref + '[') != -1:
                post_list.append(key)

        for key in obj:
            name = pref + '[{}]'.format(key.id)
            model_list.append(name)

        for item in model_list:
            if not item in post_list:
                index = re.sub(r'[^0-9.]+', r'', item)
                instance = self.objects.get(id=index)
                instance.delete()


class ThreeInputField:
    # add
    def add(self, obj, request, pref1, pref2, pref3):
        post_list = []
        model_list = []

        for key in request.POST:
            if key.find(pref1 + '[') != -1:
                post_list.append(key)

        for key in obj:
            name = pref1 + '[{}]'.format(key.id)
            model_list.append(name)

        for item in post_list:
            if not item in model_list:
                if request.POST[item] != '':
                    index = re.sub(r'[^0-9.]+', r'', item)
                    instance = self.objects.create(name=request.POST[pref1+'[' + index + ']'], time=request.POST[pref2 + '[' + index + ']'], price=request.POST[pref3 + '[' + index + ']'], content_id=request.user.id)
                    obj.user = instance

    # update
    def update(self, obj, request, fields):

        for item in request.POST:
            for key in fields.keys():
                if item.find(key + '[') != -1:
                    for i in obj:
                        name = key + '[{}]'.format(i.id)
                        if item == name:
                            val = fields.get(key)
                            setattr(i, val, request.POST[name])
                            i.save()

    # remove
    def remove(self, obj, request, pref):
        post_list = []
        model_list = []

        for key in request.POST:
            if key.find(pref + '[') != -1:
                post_list.append(key)

        for key in obj:
            name = pref + '[{}]'.format(key.id)
            model_list.append(name)

        for item in model_list:
            if not item in post_list:
                index = re.sub(r'[^0-9.]+', r'', item)
                instance = self.objects.get(id=index)
                instance.delete()


class CheckboxField:

    def save(self, name, request):
        if name in request.POST:
            print(name+' true')
            setattr(self, name, True)
        else:
            print(name + ' false')
            setattr(self, name, False)


def get_task(user_main, meeting, doctor_id, status):
    meeting_object_list = meeting.objects.filter(doctor_id=doctor_id, status=status).order_by('sort_id')
    meetings = list()

    for meeting in meeting_object_list:
        _meeting = {
            'id': meeting.id,
            'date': meeting.date,
            'time_start': str(meeting.time_start),
            'time_end': str(meeting.time_end),
            'user': user_main.objects.filter(user=meeting.user_id).values('fio')[0],
            'status': meeting.status,
            'sort_id': meeting.sort_id,
        }

        meetings.append(_meeting)

    return meetings


def get_meetings_list(meeting, spec, user_main, user_id):
    meetings = list()

    meeting_object_list = meeting.objects.filter(user_id=user_id).exclude(status='reject').exclude(status='archive').order_by(
        'id').reverse()

    for meeting in meeting_object_list:
        doctor_id = meeting.doctor_id
        specialty = ', '.join([str(i) for i in spec.objects.filter(content=doctor_id).order_by('?')[:4]])

        status_title = ''

        if meeting.status == 'new':
            status_title = 'Новая'

        if meeting.status == 'work':
            status_title = 'В работе'

        if meeting.status == 'success':
            status_title = 'Выполнено'

        _meeting = {
            'id': meeting.id,
            'date': meeting.date,
            'doctor_id': doctor_id,
            'doctor': user_main.objects.filter(user=doctor_id).values('fio')[0],
            'image': user_main.objects.filter(user=doctor_id).values('avatar')[0],
            'time_start': str(meeting.time_start),
            'time_end': str(meeting.time_end),
            'specialty': specialty,
            'status': meeting.status,
            'status_title': status_title,
        }

        meetings.append(_meeting)

    return meetings


def get_contact_list(meeting, usermain, user, doctor_id):
    contact_ids = list()
    contact_list = list()

    meetings = meeting.objects.filter(doctor_id=doctor_id)

    for meeting in meetings:
        user_id = meeting.user_id

        if user_id not in contact_ids:
            contact_ids.append(user_id)

    for contact_id in contact_ids:
        _contact = {
            'id': contact_id,
            'user': usermain.objects.filter(user=contact_id).values('fio')[0],
            'image': usermain.objects.filter(user=contact_id).values('avatar')[0],
            'phone': usermain.objects.filter(user=contact_id).values('phone')[0]['phone'],
            'whatsapp': usermain.objects.filter(user=contact_id).values('whatsapp')[0]['whatsapp'],
            'skype': usermain.objects.filter(user=contact_id).values('skype')[0]['skype'],
            'email': user.objects.get(pk=contact_id).email,
        }

        contact_list.append(_contact)

    return contact_list
