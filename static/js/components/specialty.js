let specialty = {

    action: function(){
        $('.specialty-form').on('submit', specialty.redirect);
    },

    redirect: function(){
        let slug = $('.speciality-select').val();
        let page = window.location.href;

        if(slug == '' || slug == 'all'){
            window.location.href = page + 'doctors/list/';
        } else {
            window.location.href = page + 'doctors/list/' + slug + '/';
        }

        return false;
    },

    init: function(){
        $('.speciality-select').customselect();
        specialty.action();
    },
}

export { specialty }