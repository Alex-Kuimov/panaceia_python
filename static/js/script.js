function advantageTab(evt, advantageName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(advantageName).style.display = "block";
  evt.currentTarget.className += " active";
}


//Скрипт календаря для расписания//

calendar = {};

// Названия месяцев
calendar.monthName=[
  'Январь', 'Февраль', 'Март', 'Апрель',
  'Май', 'Июнь', 'Июль', 'Август',
  'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

// Названия дней недели
calendar.dayName=[
  'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'
];

// Выбранная дата
calendar.selectedDate = {
  'Day' : null,
  'Month' : null,
  'Year' : null
};

// ID элемента для размещения календарика
calendar.element_id=null;

// Выбор даты
calendar.selectDate = function(day,month,year) {
  calendar.selectedDate={
    'Day' : day,
    'Month' : month,
    'Year' : year
  };
  calendar.drawCalendar(month,year);
}

// Отрисовка календарика на выбранный месяц и год
calendar.drawCalendar = function(month,year) {
  var tmp='';
  tmp+='<table class="calendar" cellspacing="0" cellpadding="0">';

  // Месяц и навигация
  tmp+='<tr>';
  tmp+='<td colspan="5" class="navigation" '+
       'onclick="calendar.drawCalendar('+
       calendar.selectedDate.Month+','+
       calendar.selectedDate.Year+');">'+
       calendar.monthName[(month-1)]+' - '+year+'<\/td>';
  tmp+='<td class="navigation link-nav" '+
       'onclick="calendar.drawCalendar('+(month>1?(month-1):12)+
       ','+(month>1?year:(year-1))+');"><<\/td>';
  tmp+='<td class="navigation link-nav" '+
       'onclick="calendar.drawCalendar('+(month<12?(month+1):1)+
       ','+(month<12?year:(year+1))+');">><\/td>';
  tmp+='<\/tr>';

  // Шапка таблицы с днями недели
  tmp+='<tr>';
  tmp+='<th>'+calendar.dayName[0]+'<\/th>';
  tmp+='<th>'+calendar.dayName[1]+'<\/th>';
  tmp+='<th>'+calendar.dayName[2]+'<\/th>';
  tmp+='<th>'+calendar.dayName[3]+'<\/th>';
  tmp+='<th>'+calendar.dayName[4]+'<\/th>';
  tmp+='<th class="holiday">'+calendar.dayName[5]+'<\/th>';
  tmp+='<th class="holiday">'+calendar.dayName[6]+'<\/th>';
  tmp+='<\/tr>';

  // Количество дней в месяце
  var total_days = 32 - new Date(year, (month-1), 32).getDate();
  // Начальный день месяца
  var start_day = new Date(year, (month-1), 1).getDay();
  if (start_day==0) { start_day=7; }
  start_day--;
  // Количество ячеек в таблице
  var final_index=Math.ceil((total_days+start_day)/7)*7;

  var day=1;
  var index=0;
  do {
    // Начало строки таблицы
    if (index%7==0) {
      tmp+='<tr>';
    }
    // Пустые ячейки до начала месяца или после окончания
    if ((index<start_day) || (index>=(total_days+start_day))) {
      tmp+='<td class="grayed"> <\/td>';
    }
    else {
      var class_name='';
      // Выбранный день
      if (calendar.selectedDate.Day==day &&
          calendar.selectedDate.Month==month &&
          calendar.selectedDate.Year==year) {
        class_name='selected';
      }
      // Праздничный день
      else if (index%7==6 || index%7==5) {
        class_name='holiday';
      }
      // Ячейка с датой
      tmp+='<td class="'+class_name+'" '+
           'onclick="calendar.selectDate('+
           day+','+month+','+year+');">'+day+'<\/td>';
      day++;
    }
    // Конец строки таблицы
    if (index%7==6) {
      tmp+='<\/tr>';
    }
    index++;
  }
  while (index<final_index);

  tmp+='<\/table>';

  // Вставить таблицу календарика на страницу
  var el=document.getElementById(calendar.element_id);
  if (el) {
    el.innerHTML=tmp;
  }
}

// ID элемента для размещения календарика
calendar.element_id = 'calendar_table';

// По умолчанию используется текущая дата
calendar.selectedDate={
  'Day' : new Date().getDate(),
  'Month' : parseInt(new Date().getMonth())+1,
  'Year' : new Date().getFullYear()
};

// Нарисовать календарик
calendar.drawCalendar(
  calendar.selectedDate.Month,
  calendar.selectedDate.Year
);

//Скрипт календаря для вывода онлайн записи//

calendar = {};

// Названия месяцев
calendar.monthName=[
  'Январь', 'Февраль', 'Март', 'Апрель',
  'Май', 'Июнь', 'Июль', 'Август',
  'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

// Названия дней недели
calendar.dayName=[
  'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'
];

// Выбранная дата
calendar.selectedDate = {
  'Day' : null,
  'Month' : null,
  'Year' : null
};

// ID элемента для размещения календарика
calendar.element_id=null;

// Выбор даты
calendar.selectDate = function(day,month,year) {
  calendar.selectedDate={
    'Day' : day,
    'Month' : month,
    'Year' : year
  };
  calendar.drawCalendar(month,year);
}

// Отрисовка календарика на выбранный месяц и год
calendar.drawCalendar = function(month,year) {
  var tmp='';
  tmp+='<table class="calendar" cellspacing="0" cellpadding="0">';

  // Месяц и навигация
  tmp+='<tr>';
  tmp+='<td class="navigation link-nav" '+
      'onclick="calendar.drawCalendar('+(month>1?(month-1):12)+
      ','+(month>1?year:(year-1))+');"><<\/td>';
  tmp+='<td colspan="5" class="navigation" '+
       'onclick="calendar.drawCalendar('+
       calendar.selectedDate.Month+','+
       calendar.selectedDate.Year+');">'+
       calendar.monthName[(month-1)]+' - '+year+'<\/td>';
  tmp+='<td class="navigation link-nav" '+
       'onclick="calendar.drawCalendar('+(month<12?(month+1):1)+
       ','+(month<12?year:(year+1))+');">><\/td>';
  tmp+='<\/tr>';

  // Шапка таблицы с днями недели
  //tmp+='<tr>';
  //tmp+='<th>'+calendar.dayName[0]+'<\/th>';
  //tmp+='<th>'+calendar.dayName[1]+'<\/th>';
  //tmp+='<th>'+calendar.dayName[2]+'<\/th>';
  //tmp+='<th>'+calendar.dayName[3]+'<\/th>';
  //tmp+='<th>'+calendar.dayName[4]+'<\/th>';
  //tmp+='<th class="holiday">'+calendar.dayName[5]+'<\/th>';
  //tmp+='<th class="holiday">'+calendar.dayName[6]+'<\/th>';
  //tmp+='<\/tr>';

  // Количество дней в месяце
  var total_days = 32 - new Date(year, (month-1), 32).getDate();
  // Начальный день месяца
  var start_day = new Date(year, (month-1), 1).getDay();
  if (start_day==0) { start_day=7; }
  start_day--;
  // Количество ячеек в таблице
  var final_index=Math.ceil((total_days+start_day)/7)*7;

  var day=1;
  var index=0;
  do {
    // Начало строки таблицы
    if (index%7==0) {
      tmp+='<tr>';
    }
    // Пустые ячейки до начала месяца или после окончания
    if ((index<start_day) || (index>=(total_days+start_day))) {
      tmp+='<td class="grayed"> <\/td>';
    }
    else {
      var class_name='';
      // Выбранный день
      if (calendar.selectedDate.Day==day &&
          calendar.selectedDate.Month==month &&
          calendar.selectedDate.Year==year) {
        class_name='selected';
      }
      // Праздничный день
      else if (index%7==6 || index%7==5) {
        class_name='holiday';
      }
      // Ячейка с датой
      tmp+='<td class="'+class_name+'" '+
           'onclick="calendar.selectDate('+
           day+','+month+','+year+');">'+day+'<\/td>';
      day++;
    }
    // Конец строки таблицы
    if (index%7==6) {
      tmp+='<\/tr>';
    }
    index++;
  }
  while (index<final_index);

  tmp+='<\/table>';

  // Вставить таблицу календарика на страницу
  var el=document.getElementById(calendar.element_id);
  if (el) {
    el.innerHTML=tmp;
  }
}

// ID элемента для размещения календарика
calendar.element_id = 'calendar_table_online';

// По умолчанию используется текущая дата
calendar.selectedDate={
  'Day' : new Date().getDate(),
  'Month' : parseInt(new Date().getMonth())+1,
  'Year' : new Date().getFullYear()
};

// Нарисовать календарик
calendar.drawCalendar(
  calendar.selectedDate.Month,
  calendar.selectedDate.Year
);


// Табы переключения
$(function() {
  var tab = $('#tabs .tab-maps > .tab-map'); 
  tab.hide().filter(':first').show(); 
  
  // Клики по вкладкам.
  $('#tabs .tabs-nav .icon a').click(function(){
    tab.hide(); 
    tab.filter(this.hash).show(); 
    $('#tabs .tabs-nav .icon a').removeClass('active');
    $(this).addClass('active');
    return false;
  }).filter(':first').click();
 
  // Клики по якорным ссылкам.
  $('.tabs-target').click(function(){
    $('#tabs .tabs-nav a[href=' + $(this).data('id')+ ']').click();
  });
});

//Всплывающие окна//

$(document).ready(function(){
    PopUpHide();
});
function PopUpShow(){
    $("#popup1").show();
}
function PopUpHide(){
    $("#popup1").hide();
}

$(document).ready(function(){
    PopUpHide();
});
