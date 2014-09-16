init_form_confirm = function(id, is_confirm_needed) {
    $(id).submit(function(event){
        var target = $(event.target);
        var confirmation = $('input[name=confirmation]', target).val();
        if(confirmation == '' && is_confirm_needed(target)) {
            $('#newgame_confirm_modal').modal();
            event.preventDefault();
        }
    });
    $(id + '_yes').click(function(){
        var target = $(id + '_confirm_modal');
        $('input[name=confirmation]', target).val('true');
        target.submit();
    });
}
