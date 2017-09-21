$(document).ready(function() {
    $.widget("custom.addroom", {
        _create: function() {
            this.element.click(function(event){
                event.preventDefault();
                var target = $(event.target);
                var widget = $('#' + target.attr('for'));
                var clon = widget.clone();
                clon.attr('id', '');
                clon.attr('value', '');
                clon.insertBefore(target);
            });
        }
    });
    $.widget("custom.add_from_list", {
        _create: function() {
            this.element.click(function(event){
                event.preventDefault();
                var target = $(event.target);
                var widget = $('#' + target.attr('for'));
                var clon = $('<input>');
                clon.addClass('form-control');
                clon.attr('value', widget.val());
                clon.prop('readonly', true);
                clon.attr('name', target.attr('for_name'));
                clon.insertBefore(widget);

                widget.find('option:selected').remove();
                if(widget.val() == null) {
                    target.prop('disabled', true);
                };
            });
        }
    });
    $.widget("custom.remove_button", {
        _create: function() {
            this.element.click(function(event){
                event.preventDefault();
                var target = $(event.target);
                var input =  $('#' + target.attr('for'));
                var select = $('#' + target.attr('select_for'));
                var value = input.find('input').val();

                select.append(new Option(value, value));
                input.remove();
                $('button.add_from_list').prop('disabled', false);
            });
        }
    });
});
