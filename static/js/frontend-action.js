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
                        headers: {'api-csrftoken': csrftoken},
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
                headers: {'api-csrftoken': csrftoken},
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
                headers: {'api-csrftoken': csrftoken},
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
                            let html = '';
                            let service_obj = {};

                            for (var key in data) {
                                service_obj = data[key]['services'];
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
                headers: {'api-csrftoken': csrftoken},
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

                            let difference = parseInt(timeEnd) - parseInt(timeStart);
                            let count = 0;
                            let cof = 0;

                            if(interval == 30){
                                cof = 2;
                            }

                            if(interval == 45){
                                cof = 1.25;
                            }

                            if(interval == 60){
                                cof = 1;
                            }

                            if(interval == 90){
                                cof = 0.75;
                            }

                            if(interval == 120){
                                cof = 0.5;
                            }

                            count = difference * cof;

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

                            end.setMinutes(end.getMinutes() - interval);

                            html += '<option value="' + time_arr[key]['time_start']  + '">' + time_arr[key]['time_start'] + '</option>';

                            for (var i = 0; i < count; i++) {
                                start.setMinutes(start.getMinutes() + interval);

                                let m = start.getMinutes();
                                let h = start.getHours()

                                if(start.getMinutes() == 0){
                                    m = '00';
                                }

                                let displayTime = h + ':' + m;
                                let time = getDate(displayTime);

                                if(time <= end){
                                    html += '<option value="' + displayTime + '">' + displayTime + '</option>';
                                }
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

    doctorMap.init();
    registry.init();
    modal.init();

});