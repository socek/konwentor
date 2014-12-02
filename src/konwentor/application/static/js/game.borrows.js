$(document).ready(function() {
    function GatherHint(id) {
        this.id = id;
        this.form = $('#' + id);
        this.name = $('#' + id + '_name');
        this.surname = $('#' + id + '_surname');
        this.number = $('#' + id + '_document_number');
        this.document = $('#' + id + '_document_type');

        this.number.blur(function(){
            $.post(
                "/game/borrows/hint",
                {
                    number: this.number.val(),
                }
            ).done(function(data){
                if(data.name != "") {
                    this.name.val(data.name);
                }
                if(data.surname != "") {
                    this.surname.val(data.surname);
                }
                if(data.document != "") {
                    this.document.val(data.document);
                }
            }.bind(this));
        }.bind(this));
    }

    var hint = new GatherHint('GameBorrowAddForm');
});
