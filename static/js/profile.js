$(document).ready(function(){
    'use strict';

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    let countSpecElement = 0;
    let countElement = 0;
    let countEdElement = 0;
    let countQuElement = 0;
    let countSeElement = 0;

    let profile = {

        action: function(){
            $('.remove-avatar').on('click', profile.removeAvatar);
            $('.doctor_chk').on('change', profile.typeSpecialty);

            $('.spec-add').on('click', profile.addSpec);
            $('.as-add').on('click', profile.addAs);
            $('.ed-add').on('click', profile.addEd);
            $('.qu-add').on('click', profile.addQu);
            $('.se-add').on('click', profile.addSe);

            $('body').on('click', '.item-remove', profile.removeItem);

            $('.avatar').on('change', profile.checkFileBeforeUpload);
            $('.doc_file').on('change', profile.checkFileBeforeUpload);
            $('.passport_photo').on('change', profile.checkFileBeforeUpload);
            $('.diplom_photo').on('change', profile.checkFileBeforeUpload);
        },

        readURL: function(input, img){
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    $(img).attr('src', e.target.result);
                }
                reader.readAsDataURL(input.files[0]);
            }
        },

        removeAvatar: function(){
            let userNoneImg = '/static/img/user.png'
            $('.avatar_image').attr('src', userNoneImg);
            $('.avatar_none').val('y');

            return false;
        },

        checkFileBeforeUpload: function(){

            let file = this.files;
            let cls = $(this).attr('class');
            let useLabel = $(this).attr('use-label');

            if(typeof(file)!=='undefined'){
                let size = file[0].size;
                let type = file[0].type;
                let name = file[0].name;

                if(type == 'image/jpeg' || type == 'image/jpg' || type == 'image/png'){

                    if(size <= 1500000){
                        profile.readURL(this, '.'+cls+'_image');
                        if(useLabel == 'y'){
                            $('.'+cls+'_label').html(name);
                        }
                    } else {
                        alert('Error size!');
                    }

                } else {
                    alert('Error format!');
                }
            }

        },

        dob: function(){
           $.datepicker.setDefaults( $.datepicker.regional[ "ru" ] );
           $('.dob' ).datepicker({
                changeMonth: true,
                changeYear: true,
                yearRange: "1950:2005",
           });
        },

        typeSpecialty: function(){
            if ($(this).is(':checked')){
                $(this).val('True');
            } else {
                $(this).val('False');
            }
        },

        addSpec: function(){
            let element = '';

            countSpecElement = countSpecElement + 1;

            element += '<div class="row spec-block spec-block-'+countSpecElement+'">';
                element += '<div class="col-8">';
                    element += '<input type="text" list="list-spec" name="spec['+countSpecElement+']" value="" placeholder="специальность" required>';
                element += '</div>';
                element += '<div class="col-4">';
                    element += '<a href="#" class="spec-remove item-remove" data-id="'+countSpecElement+'" data-name="spec-block">Удалить</a>';
                element += '</div>';
            element += '</div>';

            $(this).before(element);

            return false
        },

        addAs: function(){
            let element = '';

            countElement = countElement + 1;

            element += '<div class="row as-block as-block-'+countElement+'">';
                element += '<div class="col-8">';
                    element += '<input type="text" name="as['+countElement+']" value="" placeholder="Название ассоциации" required>';
                element += '</div>';
                element += '<div class="col-4">';
                    element += '<a href="#" class="as-remove item-remove" data-id="'+countElement+'" data-name="as-block">Удалить</a>';
                element += '</div>';
            element += '</div>';

            $(this).before(element);

            return false
        },

        addEd: function(){
            let element = '';

            countEdElement = countEdElement + 1;

            element += '<div class="row ed-block ed-block-'+countEdElement+'">';
                element += '<div class="col-3">';
                    element += '<input type="text" name="edy['+countEdElement+']" value="" placeholder="Года" required>';
                element += '</div>';
                element += '<div class="col-5">';
                    element += '<input type="text" name="ed['+countEdElement+']" value="" placeholder="Название организации" required>';
                element += '</div>';
                element += '<div class="col-4">';
                    element += '<a href="#" class="ed-remove item-remove" data-id="'+countEdElement+'" data-name="ed-block">Удалить</a>';
                element += '</div>';
            element += '</div>';

            $(this).before(element);

            return false
        },

        addQu: function(){
            let element = '';

            countQuElement = countQuElement + 1;

            element += '<div class="row qu-block qu-block-'+countQuElement+'">';
                element += '<div class="col-3">';
                    element += '<input type="text" name="quy['+countQuElement+']" value="" placeholder="Года" required>';
                element += '</div>';
                element += '<div class="col-5">';
                    element += '<input type="text" name="qu['+countQuElement+']" value="" placeholder="Название организации" required>';
                element += '</div>';
                element += '<div class="col-4">';
                    element += '<a href="#" class="qu-remove item-remove" data-id="'+countQuElement+'" data-name="qu-block">Удалить</a>';
                element += '</div>';
            element += '</div>';

            $(this).before(element);

            return false
        },

        addSe: function(){
            let element = '';

            countSeElement = countSeElement + 1;

            element += '<div class="row se-block se-block-'+countSeElement+'">';
                element += '<div class="col-5">';
                    element += '<input type="text" name="se['+countSeElement+']" value="" placeholder="Название" required>';
                element += '</div>';
                element += '<div class="col-3">';

                    element += '<select name="set['+countSeElement+']" required>';
                        element += '<option value="30">30 мин.</option>';
                        element += '<option value="60">60 мин.</option>';
                        element += '<option value="90">90 мин.</option>';
                        element += '<option value="120">120 мин.</option>';
                    element += '</select>';

                element += '</div>';
                element += '<div class="col-3">';
                    element += '<input type="text" name="sep['+countSeElement+']" value="" placeholder="Цена" required>';
                element += '</div>';
                element += '<div class="col-1">';
                    element += '<a href="#" class="item-remove" data-id="'+countSeElement+'" data-name="se-block">Удалить</a>';
                element += '</div>';
            element += '</div>';

            $(this).before(element);

            return false;
        },

        removeItem: function(){
            let itemID = $(this).attr('data-id');
            let itemName = $(this).attr('data-name');
            $('.'+itemName+'-'+itemID).remove();
            return false;
        },

        cityAutocomplete: function(){
            if ($('#user-city').length){
                ymaps.load(function () {
                    let city;

                    var suggestView = new ymaps.SuggestView('user-city', {
                        offset: [10, 10]
                    });

                    suggestView.events.add("select", function(e) {
                        city = e.get('item').value;
                        ymaps.geocode(city, {
                            results: 1
                        }).then(function (res) {
                            let first 	= res.geoObjects.get(0),
                                coords 	= first.geometry.getCoordinates();

                            document.getElementById('coords').value = coords;
                        });
                    });
                });
            }
        },

        init: function(){
           profile.action();
           profile.dob();
           profile.cityAutocomplete();
        }

    }

    let userCalendar = {
        init: function(){
            if ($('#doctor_grafik').length){
                let page = location.origin;

                $.ajax({
                    url: page + '/doctors/get_calendar/',
                    type: 'get',
                    headers: {'api-csrftoken': csrftoken},
                    success: function(data) {

                        let dataEvent = {events : []}

                        for (var key in data) {

                            let year = new Date(data[key]['date']).getFullYear();
                            let month = new Date(data[key]['date']).getMonth();
                            let day = new Date(data[key]['date']).getDate();

                            let hStart = new Date(data[key]['date']+' '+data[key]['time_start']).getHours();
                            let mStart = new Date(data[key]['date']+' '+data[key]['time_start']).getMinutes();

                            let hEnd = new Date(data[key]['date']+' '+data[key]['time_end']).getHours();
                            let mEnd = new Date(data[key]['date']+' '+data[key]['time_end']).getMinutes();

                            let _event = {
                                "id": data[key]['id'],
                                "start": new Date(year, month, day, hStart, mStart),
                                "end": new Date(year, month, day, hEnd, mEnd),
                                "title": data[key]['title'],
                            }
                            dataEvent.events.push(_event)
                        }

                        $('#doctor_grafik').weekCalendar({
                            timeslotsPerHour: 4,
                            eventNew : function(calEvent, $event) {

                                let year = calEvent.start.getFullYear();
                                let month = calEvent.start.getMonth()+1;
                                let day = calEvent.start.getDate();
                                let date = day + '.' + month + '.' + year;

                                let time_start = calEvent.start.getHours() + ':' + calEvent.start.getMinutes();
                                let time_end = calEvent.end.getHours() + ':' + calEvent.end.getMinutes();

                                $.ajax({
                                    url: page + '/doctors/create_event/',
                                    type: 'get',
                                    headers: {'api-csrftoken': csrftoken},
                                    data:{'date': date, 'time_start': time_start, 'time_end': time_end},
                                    success: function(data) {
                                        $event.attr('data-id', data)
                                    },
                                });

                            },
                            eventClick : function(calEvent, $event) {
                                let event_id = $event.attr('data-id');

                                if(event_id == 'undefined'){
                                    $event.remove();
                                } else {
                                    $.ajax({
                                        url: page + '/doctors/delete_event/',
                                        type: 'get',
                                        headers: {'api-csrftoken': csrftoken},
                                        data:{'event_id': event_id},
                                        success: function(data) {
                                            $event.remove();
                                        },
                                    });
                                }
                            },

                            eventDrop : function(calEvent, $event) {
                                let event_id = $event.id;
                                let year = calEvent.start.getFullYear();
                                let month = calEvent.start.getMonth()+1;
                                let day = calEvent.start.getDate();
                                let date = day + '.' + month + '.' + year;

                                let time_start = calEvent.start.getHours() + ':' + calEvent.start.getMinutes();
                                let time_end = calEvent.end.getHours() + ':' + calEvent.end.getMinutes();

                                $.ajax({
                                    url: page + '/doctors/update_event/',
                                    type: 'get',
                                    headers: {'api-csrftoken': csrftoken},
                                    data:{'date': date, 'time_start': time_start, 'time_end': time_end, 'event_id': event_id},
                                    success: function(data) {
                                        console.log(data);
                                    },
                                });
                            },
                            use24Hour : true,
                            businessHours : {start: 8, end: 22, limitDisplay : true},
                            timeSeparator : " - ",
                            firstDayOfWeek : 1,
                            data:dataEvent,
                            timeFormat : "H:i",
                            dateFormat : "d.m.Y",
                            shortDays : ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
                            longDays : ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
                            buttonText : {
                                today : "Сегодня",
                                lastWeek : "&nbsp;&lt;&nbsp;",
                                nextWeek : "&nbsp;&gt;&nbsp;"
                            },

                        });
                    },
                });
            }
        }
    }

    let userTask = {
        action: function(){
            $('body').on('click', '.task-get', userTask.get);
        },

        sortable: function () {
			$('.task-list').sortable({

				connectWith: ".task-list",

				start: function (event, ui) {
                    $('.scroll-wrapper').css('overflow', 'unset');
                    $('.scroll-content').css('overflow', 'unset');
				},

				stop: function (event, ui) {
                    $('.scroll-wrapper').css('overflow', 'hidden');
                    $('.scroll-content').css('overflow', 'scroll');
				},

				update: function (event, ui) {

				    let items = {},
				        page = location.origin,
					    wrapID = event.target.getAttribute('id'),
					    status = event.target.getAttribute('data-status');


                    $('#' + wrapID + ' .task-item').each(function (i) {
                        let dataID = $(this).attr('data-id');

                        if (typeof (dataID) != 'undefined') {
                            let item = {};

                            item['id'] = dataID;
                            item['sort'] = i + 1;
                            item['status'] = status;

                            items[i] = item;
                        }
                    });

                    items = JSON.stringify(items);

                    $.ajax({
                        url: page + '/doctors/update_meeting/',
                        type: 'get',
                        headers: {'api-csrftoken': csrftoken},
                        data:{'items': items},
                        success: function(data) {
                            //console.log(data);
                        },
                    });

				},

			});

			$('.task-list').scrollbar();
		},

        get: function () {
            let meeting_id = $(this).attr('data-id');
            let page = location.origin;

            $('.modal-body-ajax').html('Загрузка...');

            $.ajax({
                url: page + '/doctors/get_meeting/',
                type: 'get',
                headers: {'api-csrftoken': csrftoken},
                data:{'meeting_id': meeting_id},
                success: function(data) {

                    let date = new Date(data[0].date);
                    let year = date.getFullYear();
                    let month = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);
                    let day = (date.getDate() < 10 ? '0' : '') + date.getDate();
                    let newDate = day + '.' + month + '.' + year;

                    let html = '';
                    html += '<p><strong>Пациент:</strong> '+data[0].user.fio+'</p>';
                    html += '<p><strong>Услуга:</strong> '+data[0].services[0].name+'</p>';
                    html += '<p><strong>Продолжительность:</strong> '+data[0].services[0].time+' минут</p>';
                    html += '<p><strong>Дата:</strong> '+newDate+'</p>';
                    html += '<p><strong>Время:</strong> '+data[0].time_start+'</p>';

                    if(data[0].phone != ''){
                        html += '<p><strong>Контактный телефон:</strong> '+data[0].phone+'</p>';
                    }

                    if(data[0].skype != ''){
                        html += '<p><strong>Skype:</strong> '+data[0].skype+'</p>';
                    }

                    if(data[0].whatsapp != ''){
                        html += '<p><strong>WhatsApp:</strong> '+data[0].whatsapp+'</p>';
                    }

                    if(data[0].email != ''){
                        html += '<p><strong>E-mail:</strong> '+data[0].email+'</p>';
                    }

                    $('.modal-body-ajax').html(html);

                },

            });
        },

        init: function(){
            userTask.action();
            userTask.sortable();
        }
    }

    let modal = {

       action: function(){
            $('body').on('click', '.show-modal', modal.show);
            $('body').on('click', '.hide-modal', modal.hide);
       },

       show: function(){
            $('.modal-cover').fadeIn('500').css('display', 'flex');
            return false;
       },

       hide: function(){
            $('.modal-cover').fadeOut('500');
       },

       init: function(){
            modal.action();
       },

    }

    profile.init();
    userCalendar.init();
    userTask.init();
    modal.init();

});