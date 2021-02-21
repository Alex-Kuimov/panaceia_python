let modal = {

   action: function(){
        $('body').on('click', '.show-modal', modal.show);
        $('body').on('click', '.hide-modal', modal.hide);
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

export { modal }