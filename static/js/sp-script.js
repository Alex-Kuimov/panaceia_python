$(document).ready(function(){

    'use strict';

    let profile = {

        action: function(){
            $('.remove-avatar').on('click', profile.removeAvatar);
            $('.avatar').on('change', profile.changeAvatar);
            $('.doctor_chk').on('change', profile.typeSpecialty);
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

        init: function(){
           profile.action();
           profile.dob();
        }

    }

    profile.init();

});