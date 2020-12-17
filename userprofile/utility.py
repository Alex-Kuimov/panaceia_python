import re


class UserFieldUtility():
    # add
    def add(obj, OBJ, request, pref1, pref2):
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
                    instance = OBJ.objects.create(years=request.POST[pref2+'[' + index + ']'],
                                                            name=request.POST[pref1+'[' + index + ']'],
                                                            content_id=request.user.id)
                    obj.user = instance

    # update
    def update(obj, request, fields):

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
    def remove(obj, OBJ, request, pref):
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
                instance = OBJ.objects.get(id=index)
                instance.delete()