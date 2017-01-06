$(document).ready(function(){
    var add = $(".form_add");
    var sec = $(".security");
    var token_cookie = sec[0].attributes.value.nodeValue;
    console.log(token_cookie);
    console.log('variable bound');
    add.on("click", function(event){
        event.preventDefault();
        console.log(add);
        // send ajax request to edit a journal entry
        $.ajax({
            url: '/',
            headers: { 'X-CSRF-Token': $(this).parent().find("input"["security"]).value, }
            type: 'POST',
            data: {
                "title": $(this).parent().find("input"["title"]).value,
                "body": $(this).parent().find("input"["body"]).value,
            },
            success: function(){
                console.log("edited");
            }
        });
        // // fade out expense
        // this_row = $(this.parentNode.parentNode);
        // // delete the containing row
        // this_row.animate({
        //     opacity: 0
        // }, 500, function(){
        //     $(this).remove();
        // })
    });
});
