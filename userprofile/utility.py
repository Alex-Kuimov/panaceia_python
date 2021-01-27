import re


class OneInputField():
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


class TwoInputField():
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


class ThreeInputField():
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


class CheckboxField():

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
