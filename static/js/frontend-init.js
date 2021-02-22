'use strict';

import { getCookie } from './components/cookie.js';
import { modal } from './components/modal.js';
import { starRate } from './components/rate.js';
import { doctorMap } from './components/map.js';
import { specialty } from './components/specialty.js';
import { registry } from './components/registry.js';

$(document).ready(function(){
    const csrftoken = getCookie('csrftoken');

    doctorMap.init(csrftoken);
    registry.init(csrftoken);
    modal.init();
    specialty.init();
    starRate.init();
});
