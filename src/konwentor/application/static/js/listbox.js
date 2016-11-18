$(document).ready(function() {
    var outside_box = $('#games_outside_box').DataTable({
        "paging":   false,
    });
    var in_box = $('#games_in_box').DataTable({
        "paging":   false,
    });
    console.log(outside_box);

    $('a.btn.btn-danger.movetobox').click(function(event){
        var target = $(event.target),
            url = target.attr('href'),
            row = target.closest('tr'),
            clone = row.clone();

        event.preventDefault();

        $.ajax({
            url: url
        }).done(function(){
            $('div.modal').modal('hide');
            $(clone).find('td:last').remove();
            outside_box.row(row).remove().draw(false);
            in_box.row.add(clone).draw(false);
        }).error(function(){
            alert('Coś poszłon niie tak. Skrypt zwrócił bład. Musisz odświeżyć stronę.');
        });
    });
});
