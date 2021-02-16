from django.core.mail import EmailMessage
from userprofile.models import User, UserMain, UserDoctor, Service, Specialty, SpecialtyList
from doctors.models import Meeting, Calendar, Review
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
    paginator = Paginator(object_list, 10)
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

        reviews_count_txt = get_count_reviews(Review, user.id)

        star_prof = get_star_prof(Review, user.id)
        star_pers = get_star_pers(Review, user.id)

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
            'star_prof': str(star_prof),
            'star_pers': str(star_pers),
            'patients': patients[:-2],
            'meet': meet[:-2],
            'reviews_count': reviews_count_txt,
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


def get_count_reviews(review, doctor_id):
    reviews = review.objects.filter(doctor_id=doctor_id)
    reviews_dic = ['отзыв', 'отзыва', 'отзывов']
    reviews_count = len(reviews)
    reviews_text = decl_of_num(reviews_count, reviews_dic)
    reviews_result = str(reviews_count) + ' ' + reviews_text

    return reviews_result


def get_star_prof(review, doctor_id):
    prof = 0
    review_object_list = review.objects.filter(doctor_id=doctor_id)

    for review in review_object_list:
        prof = prof + review.star_prof

    if len(review_object_list) > 0:
        star_prof = round(prof / len(review_object_list))
    else:
        star_prof = 0

    return star_prof


def get_star_pers(review, doctor_id):
    pers = 0
    review_object_list = review.objects.filter(doctor_id=doctor_id)

    for review in review_object_list:
        pers = pers + review.star_pers

    if len(review_object_list) > 0:
        star_pers = round(pers / len(review_object_list))
    else:
        star_pers = 0

    return star_pers