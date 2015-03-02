function Dashboard(){
    Dashboard.init();
}

Dashboard.init = function(){
    Dashboard.initSidebarNav();
}

Dashboard.initSidebarNav = function(){
    $('.nav.nav-sidebar li').click(function(){
        if ($(this).children('.subnav').size() > 0){
            $('.nav.subnav:not(.nav.subnav:has(.active))').removeClass('open');
            $(this).children('.subnav').addClass('open');
        }
    })
}

Dashboard.show_message = function(message, type){
    type = type || 'success';
    $('#main').prepend('<div class="alert alert-'+type+' alert-dismissible">' +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
         message +'</div>');
}


$(document).ready(function(){
    Dashboard();    
})
