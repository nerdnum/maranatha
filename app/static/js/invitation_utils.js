

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

function do_page_setup(page_hook, data){
    // page_hook.loadTemplate("/static/js/templates/table_template.html");
    var display_array = new Array();
    for (invite in data.invalid_invitations) {
        var invite_data =
            {
                id: invite,
                detail: data.invalid_invitations[invite]
            };
        display_array.push(invite_data);
    };

    page_hook.loadTemplate("/static/js/templates/row_template.html", display_array);

};