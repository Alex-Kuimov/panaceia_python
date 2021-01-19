$(document).ready(function(){

    'use strict';

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
                    element += '<input type="text" name="set['+countSeElement+']" value="" placeholder="Время" required>';
                element += '</div>';
                element += '<div class="col-3">';
                    element += '<input type="text" name="sep['+countSeElement+']" value="" placeholder="Цена" required>';
                element += '</div>';
                element += '<div class="col-1">';
                    element += '<a href="#" class="item-remove" data-id="'+countSeElement+'" data-name="se-block">Удалить</a>';
                element += '</div>';
            element += '</div>';

            $(this).before(element);

            return false
        },

        removeItem: function(){
            let itemID = $(this).attr('data-id');
            let itemName = $(this).attr('data-name');
            $('.'+itemName+'-'+itemID).remove();
            return false
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

    let doctorMap ={

        loadMap: function(){
            if ($('#doctor-map').length){
                ymaps.ready(function(){

                    let page = window.location.href;
                    let siteUrl = window.location.origin;

                    let map = new ymaps.Map('doctor-map', {
                        center: [0, 0],
                        zoom: 12,
                    });

                    $.ajax({
                        url: page + 'get_doctors_list/',
                        type: 'get',
                        success: function(data) {
                            let mapEl = data

                            for (var key in mapEl) {
                                let coords = mapEl[key]['coords'].split(',');
                                let fio = mapEl[key]['fio'];
                                let specialty = mapEl[key]['specialty'];
                                let experience_years = mapEl[key]['experience_years'];
                                let phone = mapEl[key]['phone'];
                                let city = mapEl[key]['city'];
                                let avatar = mapEl[key]['avatar'];
                                let objects = new ymaps.Placemark(coords);

                                let content = '';
                                content += '<div class="doctor-map-content">';

                                    content += '<div class="doctor-map-left">';
                                        content += '<img src="'+ siteUrl +'/'+ avatar +'" class="doctor-map-image">';
                                    content += '</div>';

                                    content += '<div class="doctor-map-right">';
                                        content += '<p class="doctor-map-fio">' + fio + '</p>';
                                        content += '<p class="doctor-map-specialty">' + specialty + '</p>';
                                        content += '<p class="doctor-map-experience-years">' + experience_years + '</p>';
                                        content += '<p class="doctor-map-phone-title">Телефон для записи</p>';
                                        content += '<p class="doctor-map-phone">' + phone + '</p>';
                                    content += '</div>';

                                content += '</div>';

                                objects.options.set('preset', 'islands#greenMedicalIcon');
                                objects.properties.set('iconCaption', fio);
                                objects.properties.set('balloonContentBody', content);

                                map.geoObjects.add(objects);
                            }

                            map.setBounds(map.geoObjects.getBounds(), {
                                checkZoomRange: true,
                                zoomMargin: 35
                            });

                        },
                        failure: function(data) {
                            console.log('err');
                        }
                    });

                });
            }
        },

        init: function(){
            doctorMap.loadMap();
        }

    }

    let userCalendar = {
        init: function(){
            if ($('#doctor_grafik').length){
                let page = location.origin;

                $.ajax({
                    url: page + '/doctors/get_calendar/',
                    type: 'get',

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
                                    data:{'date': date, 'time_start': time_start, 'time_end': time_end},
                                    success: function(data) {
                                        console.log(data);
                                        $event.attr('data-id', data)
                                    },

                                    failure: function(data) {
                                        console.log(data);
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
                                        data:{'event_id': event_id},
                                        success: function(data) {
                                            $event.remove();
                                            console.log(data);
                                        },

                                        failure: function(data) {
                                            console.log(data);
                                        },
                                    });
                                }
                            },

                            eventDrop : function(calEvent, $event) {
                                let event_id = $event.id;
                                console.log(event_id);

                                let year = calEvent.start.getFullYear();
                                let month = calEvent.start.getMonth()+1;
                                let day = calEvent.start.getDate();
                                let date = day + '.' + month + '.' + year;

                                let time_start = calEvent.start.getHours() + ':' + calEvent.start.getMinutes();
                                let time_end = calEvent.end.getHours() + ':' + calEvent.end.getMinutes();

                                $.ajax({
                                    url: page + '/doctors/update_event/',
                                    type: 'get',
                                    data:{'date': date, 'time_start': time_start, 'time_end': time_end, 'event_id': event_id},
                                    success: function(data) {
                                        console.log(data);
                                    },

                                    failure: function(data) {
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

                    failure: function(data) {
                        console.log(data);
                    }
                });
            }
        }
    }

    let modal = {

       action: function(){
            $('.show-modal').on('click', modal.show);
            $('.hide-modal').on('click', modal.hide);
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

    let registry = {

        action: function(){
            $('.registry').on('submit', registry.send);
            $('.set-doctor-id').on('click', registry.setID);
            $('.appointment').on('click', registry.show);
            $('body').on('change', '.service-list', registry.service);
        },

        setID: function(){
            let doctorID = $(this).attr('doctor-id');
            $('.app-doctor-id').val(doctorID);
        },

        send: function(){
            let page = location.origin;
            let form = $('.registry')
            let data = form.serialize();

            $.ajax({
                url: page + '/doctors/list/create_meeting/',
                type: 'get',
                data: data,
                success: function(data) {
                    $('.registry').html('<p>Вы успешно записаны на приём!</p>');
                },

                failure: function(data) {
                    $('.registry').html('<p>Возникла ошибка!</p>');
                }
            });

            return false;
        },

        show: function(){
            let page = location.origin;
            let doctor_id = $(this).attr('doctor-id');

            $.ajax({
                url: page + '/doctors/get_calendar/',
                type: 'get',
                data:{'doctor_id': doctor_id},
                success: function(data) {

                    let date_array = [];
                    let html = '';

                    for (var key in data) {
                        let date = data[key]['date'];
                        date_array.push(date)
                    }

                    html += '<p><input type="text" id="datepicker" name="app-date" class="app-date" placeholder="Дата" required></p>';

                    $('.app-date-result').html(html);

                    $('#datepicker').datepicker({
                        beforeShowDay: function(date){
                            let string = jQuery.datepicker.formatDate('yy-mm-dd', date);
                            return [ date_array.indexOf(string) != -1 ]
                        },
                        onSelect: function(dateText) {
                            let datePattern = /(\d{2})\.(\d{2})\.(\d{4})/;
                            let checkDate = new Date(dateText.replace(datePattern,'$3-$2-$1'));
                            let html = '';
                            let service_obj = {};

                            for (var key in data) {
                                let current = new Date(data[key]['date']);

                                if(+current === +checkDate){
                                    service_obj = data[key]['services'];
                                }
                            }

                            html += '<p>2. Выберите услугу:</p>';

                            html += '<p><select name="app-service" class="service-list" required>';
                            html += '<option value="" disable>---</option>';
                            for (var key in service_obj) {
                                html += '<option value="' + service_obj[key]['id'] + '">' + service_obj[key]['name'] + '</option>';
                            }

                            html += '</select></p>';

                            $('.app-service-result').html(html);
                            $('.app-time-result').html('');

                        },
                    });
                },

                failure: function(data) {
                    console.log(data);
                }
            });
        },

        service: function(){
            let service_id = $(this).val();
            let doctor_id = $('.app-doctor-id').val();
            let page = location.origin;

            $.ajax({
                url: page + '/doctors/get_calendar/',
                type: 'get',
                data:{'doctor_id': doctor_id},
                success: function(data) {
                    let dateText = $('.app-date').val();
                    let datePattern = /(\d{2})\.(\d{2})\.(\d{4})/;
                    let checkDate = new Date(dateText.replace(datePattern,'$3-$2-$1'));
                    let time_arr = [];
                    let html = '';

                    for (var key in data) {
                        let current = new Date(data[key]['date']);

                        if(+current === +checkDate){
                            let time_obj = {};

                            let timeStart = data[key]['time_start'].substring(0, data[key]['time_start'].length-3);
                            let timeEnd = data[key]['time_end'].substring(0, data[key]['time_end'].length-3);
                            let services = data[key]['services'];

                            for (var i in services) {
                                if (services[i]['id'] == service_id){
                                    var interval = services[i]['time'];
                                }
                            }

                            let count = parseInt(timeEnd) - parseInt(timeStart);

                            if(interval == 30){
                                count = count * 2;
                                count = count - 1;
                            }

                            if(interval == 60){
                                count = count - 1;
                            }

                            time_obj['time_start'] = timeStart;
                            time_obj['time_end'] = timeEnd;
                            time_obj['count'] = count;
                            time_obj['interval'] = parseInt(interval);

                            time_arr.push(time_obj);
                        }
                    }

                    html += '<p>3. Выберите время</p>';

                    html += '<p><select name="app-time" class="app-time" required>';

                        html += '<option value="">---</option>';

                        for (var key in time_arr) {
                            let count = parseInt(time_arr[key]['count']);
                            let getDate = (string) => new Date(0,0,0, string.split(':')[0], string.split(':')[1]);
                            let start = getDate(time_arr[key]['time_start']);
                            let end = getDate(time_arr[key]['time_end']);
                            let interval = parseInt(time_arr[key]['interval']);

                            html += '<option value="' + time_arr[key]['time_start']  + '">' + time_arr[key]['time_start'] + '</option>';

                            for (var i = 0; i < count; i++) {
                                start.setMinutes(start.getMinutes() + interval);

                                let m = start.getMinutes();
                                let h = start.getHours()

                                if(start.getMinutes() == 0){
                                    m = '00';
                                }

                                let s = h + ':' + m;

                                html += '<option value="' + s + '">' + s + '</option>';
                            }
                        }

                    html += '</select></p>';

                    $('.app-time-result').html(html);
                }
            });
        },

        init: function(){
            registry.action();
        },
    }

    userCalendar.init();
    profile.init();
    doctorMap.init();
    modal.init();
    registry.init();

});