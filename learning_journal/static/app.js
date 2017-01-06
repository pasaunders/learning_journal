$(document).ready(function(){
    var add = $(".form_add");
    var sec = $(".security");
    console.log("sec value: ", sec);
    var token_cookie = sec[0].attributes.value.value;
    console.log("token_cookie: ", token_cookie)
    console.log('variable bound');
    add.on("click", function(event){
        console.log("titleval: ", $("#title").val());
        event.preventDefault();
        console.log("Event: ", event)
        console.log("data: "), event.data
        console.log("add: ", add);
        // send ajax request to edit a journal entry
        $.ajax({
            url: '/journal/new-entry',
            headers: { 'X-CSRF-Token': token_cookie },
            // headers: { 'X-CSRF-Token': $("#entry_form").parent().find("input[value='csrf_token']").value },
            type: 'POST',
            data: {
                "title": $("#title").val(),
                "body": $("#body").val(),
            },
            success: function(){
                console.log("added");
            }
        });
    edit.on("click", function(event){
        event.preventDefault();
        $.ajax({
            url: '/journal/{id:\d+}/edit-entry'
            headers: { 'X-CSRF-Token': token_cookie },
            type: 'POST',
            data: {
                "title": $("#title").val(),
                "body": $("#body").val(),
            },
            success: function(){
                console.log("edited");
            }
        })
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
