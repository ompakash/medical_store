
function copy(copyId){
    var $inp=$("<p>");
    $("body").append($inp);
    $inp.val($(""+copyId).text()).select();
    document.execCommand("copy");
    $inp.remove();
    $(".alert").fadeIn(500,function(){
        $(".alert").fadeOut();
    });
}
$(document).ready(function(){
    $("#copyButton1").click(function(){
        copy('#text1');
    });
    $("#copyButton2").click(function(){
        copy('#text2');
    });
});


// TIME JAVASCIRPT

$('#input_starttime').pickatime({
    // 12 or 24 hour
    twelvehour: true,
    });