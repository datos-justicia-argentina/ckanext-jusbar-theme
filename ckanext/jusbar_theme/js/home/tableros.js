$(function () {
    var animationDelay = 50;
    //var calls = $('.featured-groups img[data-replace="svg"]').replaceSVG();
    var calls = $('#tablero .panel img').replaceSVG();
    //console.log(calls);
    var callback = function () {
        $.each($('.lalalagroup-container'), function (i, el) {
        //$.each($('.minjus-group'), function (i, el) {
            setTimeout(function () {
                //$(el).removeClass('invisible');
            }, animationDelay * i);
        });
    };
    $.when(calls).done(callback).fail(callback);
});
