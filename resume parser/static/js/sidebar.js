$(document).ready(function(){
    $(window).resize(function(){

        if($(window).width()>690)
        {
            $(".sidenav").show();
        }
        else
        {
            $(".sidenav").hide();
        }
    });
    $(".navbar-collapse-btn").click(function(){
            $(".sidenav").slideToggle("slow");
        });
});


