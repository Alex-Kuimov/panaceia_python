let doctorMap = {

    csrftoken: '',

    loadMap: function(){
        if ($('#doctor-map').length){
            ymaps.ready(function(){

                let page = location.origin;
                let siteUrl = window.location.origin;
                let slug = $('#doctor-map').attr('data-slug');

                let map = new ymaps.Map('doctor-map', {
                    center: [0, 0],
                    zoom: 12,
                });

                $.ajax({
                    url: page + '/doctors/get_doctors_list/',
                    type: 'get',
                    headers: {'api-csrftoken': doctorMap.csrftoken},
                    data: {'slug': slug},
                    success: function(data) {
                        let mapEl = data

                        for (var key in mapEl) {
                            let coords = mapEl[key]['coords'].split(',');
                            let doctor_id = mapEl[key]['id'];
                            let fio = mapEl[key]['fio'];
                            let specialty = mapEl[key]['specialty'];
                            let experience_years = mapEl[key]['experience_years'];
                            let phone = mapEl[key]['phone'];
                            let city = mapEl[key]['city'];
                            let avatar = mapEl[key]['avatar'];
                            let count_meeting = mapEl[key]['count_meeting'];
                            let average_price = mapEl[key]['average_price'];
                            let meet = mapEl[key]['meet'];
                            let patients = mapEl[key]['patients'];
                            let button = mapEl[key]['button'];
                            let reviews_count = mapEl[key]['reviews_count'];

                            if(coords != ''){

                                let objects = new ymaps.Placemark(coords);

                                let content = '';
                                content += '<div class="doctor-map-content">';

                                    content += '<div class="doctor-map-left">';
                                        content += '<img src="'+ avatar +'" class="doctor-map-image">';
                                        content += '<p class="doctor-map-price">' + average_price + ' руб.</p>';
                                        content += '<p class="doctor-map-reviews">' + reviews_count + '</p>';
                                    content += '</div>';

                                    content += '<div class="doctor-map-right">';
                                        content += '<p class="doctor-map-fio">' + fio + '</p>';
                                        content += '<p class="doctor-map-specialty">' + specialty + '</p>';
                                        content += '<p class="doctor-map-experience-years">' + experience_years + '</p>';
                                        content += '<p class="doctor-map-phone-title">Телефон для записи</p>';
                                        content += '<p class="doctor-map-phone">' + phone + '</p>';
                                        content += '<p class="doctor-map-count-meeting">Всего записались ' + count_meeting + ' чел.</p>';
                                        content += '<p class="doctor-map-patients"><strong>Специализация:</strong> ' + patients + '</p>';
                                        content += '<p class="doctor-map-meet"><strong>Прием:</strong> ' + meet + '</p>';
                                        content += button;
                                    content += '</div>';

                                content += '</div>';

                                objects.options.set('preset', 'islands#greenMedicalIcon');
                                objects.properties.set('iconCaption', fio);
                                objects.properties.set('balloonContentBody', content);

                                map.geoObjects.add(objects);
                            }
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

    init: function(csrftoken){
        doctorMap.loadMap();
        doctorMap.csrftoken = csrftoken
    }

}

export { doctorMap }