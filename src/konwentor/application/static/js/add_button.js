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
});
