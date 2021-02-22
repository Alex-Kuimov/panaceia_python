let userCalendar = {

    init: function(csrftoken){
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
                        eventResize : function(calEvent, $event) {
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

export { userCalendar }