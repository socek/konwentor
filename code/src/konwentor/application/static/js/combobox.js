$(document).ready(function() {
    $.widget("custom.combobox", {
        _create: function() {
            this.wrapper = $("<span>")
                .insertAfter(this.element);
            this._createAutocomplete();
            this._createShowAllButton();
        },
        _createAutocomplete: function() {
            this.element
                .autocomplete({
                    delay: 0,
                    minLength: 0,
                    source: $.proxy(this, "_source")
                })
                .tooltip({
                    tooltipClass: "ui-state-highlight"
                });
        },
        _createShowAllButton: function() {
            var input = this.element,
                wasOpen = false;
            $("<a>")
                .attr("tabIndex", -1)
                .attr("title", "Show All Items")
                .tooltip()
                .appendTo(this.wrapper)
                .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                })
                .removeClass("ui-corner-all")
                .addClass("custom-combobox-toggle ui-corner-right")
                .mousedown(function() {
                    wasOpen = input.autocomplete("widget").is(":visible");
                })
                .click(function() {
                    input.focus();
                    // Close if already visible
                    if (wasOpen) {
                        return;
                    }
                    // Pass empty string as value to search for, displaying all results
                    input.autocomplete("search", "");
                });
        },
        _createShowAllButton: function() {
            var input = this.element,
                wasOpen = false;
            $("<a>")
                .attr("tabIndex", -1)
                .attr("title", "Show All Items")
                .tooltip()
                .appendTo(this.wrapper)
                .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                })
                .removeClass("ui-corner-all")
                .addClass("custom-combobox-toggle ui-corner-right")
                .mousedown(function() {
                    wasOpen = input.autocomplete("widget").is(":visible");
                })
                .click(function() {
                    input.focus();
                    // Close if already visible
                    if (wasOpen) {
                        return;
                    }
                    // Pass empty string as value to search for, displaying all results
                    input.autocomplete("search", "");
                });
        },
        _source: function(request, response) {
            var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
            var _id = this.element.attr('id');
            var list = $('#' + _id + '_list');
            response(list.children("li").map(function() {
                var text = $(this).text();
                if (!request.term || matcher.test(text))
                    return {
                        label: text,
                        value: text,
                    };
            }));
        },
        _destroy: function() {
            this.wrapper.remove();
            this.element.show();
        }
    });
});
