import { modal } from './modal.js';

let userTask = {
    csrftoken: '',

    action: function(){
        $('body').on('click', '.task-get', userTask.get);
        $('body').on('click', '.show-modal-info', userTask.showModalInfo);
        $('body').on('click', '.task-to-arch', userTask.toArch);
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
                    headers: {'api-csrftoken': userTask.csrftoken},
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
            headers: {'api-csrftoken': userTask.csrftoken},
            data:{'meeting_id': meeting_id},
            success: function(data) {

                let date = new Date(data[0].date);
                let year = date.getFullYear();
                let month = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);
                let day = (date.getDate() < 10 ? '0' : '') + date.getDate();
                let newDate = day + '.' + month + '.' + year;

                let html = '';
                html += '<p><strong>Номер:</strong> '+data[0].id+'</p>';
                html += '<p><strong>Пациент:</strong> '+data[0].user.fio+'</p>';
                html += '<p><strong>Услуга:</strong> '+data[0].services[0].name+'</p>';
                html += '<p><strong>Продолжительность:</strong> '+data[0].services[0].time+' минут</p>';
                html += '<p><strong>Дата:</strong> '+newDate+'</p>';
                html += '<p><strong>Время:</strong> '+data[0].time_start+'</p>';

                if(data[0].phone != ''){
                    html += '<p><strong>Контактный телефон:</strong> <a href="tel:'+data[0].phone+'">'+data[0].phone+'</a></p>';
                }

                if(data[0].skype != ''){
                    html += '<p><strong>Skype:</strong> <a href="skype:'+data[0].skype+'">'+data[0].skype+'</a></p>';
                }

                if(data[0].whatsapp != ''){
                    html += '<p><strong>WhatsApp:</strong> <a target="_blank" href="https://web.whatsapp.com/send?l=en&amp;phone='+data[0].whatsapp+'&amp;text=Добрый день!">'+data[0].whatsapp+'</a></p>';
                }

                if(data[0].email != ''){
                    html += '<p><strong>E-mail:</strong> <a href="mailto:'+data[0].email+'">'+data[0].email+'</a></p>';
                }

                $('.modal-body-ajax').html(html);

            },

        });
    },

    showModalInfo: function () {
        let meeting_id = $(this).attr('data-id');
        let html = '';

        $('.modal-body-ajax').html('<p>Загрузка...</p>');

        html += '<p>Удалить консультацию #' + meeting_id + '?</p>';
        html += '<div class="modal-btn task-to-arch" data-id="' + meeting_id + '">Да</div>';
        html += '<div class="modal-btn hide-modal">Нет</div>';

        $('.modal-body-ajax').html(html);
    },

    toArch: function () {
        let meeting_id = $(this).attr('data-id');
        let page = location.origin;
        $('#task-item-'+meeting_id).remove();

        $.ajax({
            url: page + '/doctors/archive_meeting/',
            type: 'get',
            headers: {'api-csrftoken': userTask.csrftoken},
            data:{'meeting_id': meeting_id},
            success: function(data) {
               modal.hide();
            }
        });

    },

    init: function(csrftoken){
        userTask.action();
        userTask.sortable();
        userTask.csrftoken = csrftoken
    }
}

export { userTask }