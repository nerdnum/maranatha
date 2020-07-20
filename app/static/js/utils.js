
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

$('#subdivision_id').change(function(event){
    var selected = $('#subdivision_id option:selected').val();
    $.ajax({
        type: 'POST',
        url: '/geo/populated_area_by_division/' + selected })
    .then(function(data){

        $('#populated_area_id').children().remove();
        var choices = data.choices;
        for (i=0; i < choices.length; i++){
            $('#populated_area_id').append("<option value='"+  data.choices[i].id +"'>"
                + data.choices[i].name + "</option>")
        };
})});

$('#country_id').change(function(event){
    var selected = $('#country_id option:selected').val();
    $.ajax({
        type: 'POST',
        url: '/geo/subdivisions_by_country/' + selected})
    .then(function(data){
        $('#subdivision_id').children().remove();
        var choices = data.choices;
        for (var i=0; i < choices.length; i++){
            console.log(data.choices[i]);
            $('#subdivision_id').append("<option value='"+  data.choices[i].id +"'>"
                + data.choices[i].name + "</option>")
        };
        $('#subdivision_id').val(data.choices[0].id).trigger('change');
})});

