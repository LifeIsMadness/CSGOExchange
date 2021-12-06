$(document).ready(() => {
    $('#userbar').click(function(){
        $(this).toggleClass('active');
        $('#header-dropdown').toggleClass('active');
    });
});

