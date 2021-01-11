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

            let year = new Date().getFullYear();
            let month = new Date().getMonth();
            let day = new Date().getDate();

            $.each($('.calendar'), function() {

                let eventData = {
                    events : [
                       {"id":1, "start": new Date(year, month, day, 12), "end": new Date(year, month, day, 13, 35),"title":"Lunch with Mike"},
                       {"id":2, "start": new Date(year, month, day, 14), "end": new Date(year, month, day, 14, 45),"title":"Dev Meeting"},
                       {"id":3, "start": new Date(year, month, day + 1, 18), "end": new Date(year, month, day + 1, 18, 45),"title":"Hair cut"},
                       {"id":4, "start": new Date(year, month, day - 1, 8), "end": new Date(year, month, day - 1, 9, 30),"title":"Team breakfast"},
                       {"id":5, "start": new Date(year, month, day + 1, 14), "end": new Date(year, month, day + 1, 15),"title":"Product showcase"}
                    ]
                };

                $('#'+this.id).weekCalendar({
                    timeslotsPerHour: 4,
                    eventNew : function(calEvent, $event) {
                    //
                    },
                    data:eventData
                });

            });

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

    let datePicker = {
        init: function(){
            $('#datepicker').datepicker();
        }
    }

    let registry = {

        action: function(){
            $('.registry').on('submit', registry.send);
            $('.set-doctor-id').on('click', registry.setID);
        },

        setID: function(){
            let doctorID = $(this).attr('doctor-id');
            $('.app-doctor-id').val(doctorID);
        },

        send: function(){
            let page = window.location.href;
            let form = $('.registry')
            let data = form.serialize();

            console.log(data);

            $.ajax({
                url: page + 'create_meeting/',
                type: 'get',
                data: data,
                success: function(data) {
                    //console.log(data)
                },

                failure: function(data) {
                    //console.log('err');
                }
            });

            return false;
        },

        init: function(){
            registry.action();
        },
    }

    profile.init();
    doctorMap.init();
    datePicker.init();
    modal.init();
    registry.init();

});