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
            $('.avatar').on('change', profile.changeAvatar);

            $('.doctor_chk').on('change', profile.typeSpecialty);

            $('.spec-add').on('click', profile.addSpec);
            $('.as-add').on('click', profile.addAs);
            $('.ed-add').on('click', profile.addEd);
            $('.qu-add').on('click', profile.addQu);
            $('.se-add').on('click', profile.addSe);

            $('body').on('click', '.item-remove', profile.removeItem);

            $('.doc_file').on('change', profile.changeDoc);
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

        changeAvatar: function(){
            let file = this.files;

            if(typeof(file)!=='undefined'){
                let size = file[0].size;
                let type = file[0].type;

                if(type == 'image/jpeg' || type == 'image/jpg' || type == 'image/png'){

                    if(size <= 1500000){
                        profile.readURL(this, '.avatar_image');
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

        changeDoc: function(){

            let file = this.files;

            if(typeof(file)!=='undefined'){
                let size = file[0].size;
                let type = file[0].type;
                let name = file[0].name;

                if(type == 'image/jpeg' || type == 'image/jpg' || type == 'image/png'){

                    if(size <= 1500000){
                        profile.readURL(this, '.doc_file');
                        $('.doc_file_label').html(name)
                    } else {
                        alert('Error size!');
                    }

                } else {
                    alert('Error format!');
                }
            }
        },

        removeItem: function(){
            let itemID = $(this).attr('data-id');
            let itemName = $(this).attr('data-name');
            $('.'+itemName+'-'+itemID).remove();
            return false
        },

        cityAutocomplete: function(){
            let city = document.getElementById('user-city');
            if(city){
                let autoCity = new google.maps.places.Autocomplete(city);
            }
        },

        init: function(){
           profile.action();
           profile.dob();
           profile.cityAutocomplete();
        }

    }

    profile.init();

});