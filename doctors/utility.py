from django.core.mail import EmailMessage
from userprofile.models import User, UserMain, UserDoctor, Service, Specialty, SpecialtyList
from doctors.models import Meeting, Calendar
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def decl_of_num(n, es):
  n = n % 100
  if n >= 11 and n <= 19:
      s = es[2]
  else:
      i = n % 10
      if i == 1:
          s = es[0]
      elif i in [2, 3, 4]:
          s = es[1]
      else:
          s = es[2]
  return s


def send_notify(to, msg, subject):
    _from = settings.DEFAULT_FROM_EMAIL

    email = EmailMessage(
        subject,
        msg,
        _from,
        to,
        headers={'Reply-To': _from}
    )

    email.content_subtype = 'html'
    email.send()


def get_email(id):
    emails = list()
    email = User.objects.get(pk=id).email
    emails.append(email)
    return emails


def get_doctor_list(request, slug):
    page = request.GET.get('page')

    if slug == '':
        object_list = User.objects.filter(groups__name='doctors')
        title = 'Все специалисты'
        all_flag = 'y'
    else:
        specialty_title = SpecialtyList.objects.filter(slug=slug).values('name')[0]['name']
        object_list = User.objects.filter(groups__name='doctors', specialty__title=specialty_title)
        title = specialty_title
        all_flag = 'n'

    count = len(object_list)
    paginator = Paginator(object_list, 1)
    doctors = list()

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    for user in users:
        doctor_main = UserMain.objects.get(user=user)
        doctor = UserDoctor.objects.get(user=user)
        services = Service.objects.filter(content=user.id)
        user_spec = ', '.join([str(i) for i in Specialty.objects.filter(content=user.id).order_by('?')[:4]])

        count_meeting = len(Meeting.objects.filter(doctor_id=user.id))

        total_service_price = 0
        count_service_item = len(services)
        average_price = 0

        for service in services:
            total_service_price = total_service_price + int(service.price)

        if count_service_item != 0:
            average_price = round(total_service_price / count_service_item)

        if doctor.experience_years != '':
            words = ['год', 'года', 'лет']
            num = int(doctor.experience_years)
            years = decl_of_num(num, words)
            experience = 'Стаж: ' + str(num) + ' ' + years
        else:
            experience = ''

        patients = ''
        if doctor.patient_grown:
            patients = patients + 'взрослые, '

        if doctor.patient_children:
            patients = patients + 'дети, '

        meet = ''
        if doctor.meet_online:
            meet = meet + 'online, '

        if doctor.meet_offline:
            meet = meet + 'offline, '

        _doctor = {
            'id': user.id,
            'fio': doctor_main.fio,
            'city': doctor_main.city,
            'phone': doctor_main.phone,
            'avatar': doctor_main.avatar,
            'specialty': user_spec,
            'experience_years': experience,
            'services': services,
            'average_price': average_price,
            'count_meeting': count_meeting,
            'patient_grown': doctor.patient_grown,
            'patient_children': doctor.patient_children,
            'patients': patients[:-2],
            'meet': meet[:-2],
        }

        doctors.append(_doctor)

    data = {
        'doctors': doctors,
        'page': page,
        'users': users,
        'title': title,
        'count': count,
        'all': all_flag,
        'slug': slug,
    }

    return data
