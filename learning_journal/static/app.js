$(document).ready(function(){
    var deleters = $(".delete");
    deleters.on("click", function(){
        // send ajax request to edit a journal entry
        $.ajax({
            url: 'journal/5/edit-entry',
            type: 'POST',
            data: {
                "title": "some name",
                "body": "some company"
            }
            success: function(){
                console.log("edited");
            }
        });
        // fade out expense
        this_row = $(this.parentNode.parentNode);
        // delete the containing row
        this_row.animate({
            opacity: 0
        }, 500, function(){
            $(this).remove();
        })
    });
});
