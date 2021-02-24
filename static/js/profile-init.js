'use strict';

import { getCookie } from './components/cookie.js';
import { profile } from './components/profile.js';
import { userCalendar } from './components/calendar.js';
import { userTask } from './components/task.js';
import { modal } from './components/modal.js';
import { starRate } from './components/rate.js';
import { tinyMce } from './components/tinymce.js';

$(document).ready(function(){
    const csrftoken = getCookie('csrftoken');

    userCalendar.init(csrftoken);
    userTask.init(csrftoken);
    profile.init();
    modal.init();
    starRate.init();
    tinyMce.init();
});