//Based on http://www.djangosnippets.org/snippets/1053/

//StackedInline
jQuery(function($) {
    $('div.inline-group').sortable({
        /*containment: 'parent',
        zindex: 10, */
        axis: 'y',
        items: 'div.inline-related',
        handle: 'h3:first',
        update: function() {
            $(this).find('div.inline-related').each(function(i) {
                //Find all visible inputs that don't have an id that ends in order
                //.val() gets the first non-blank value
                //So if it finds any value, the row has been filled in somehow
                if ($(this).find(':input:not(input[id$=order]):visible').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                }
            });
        }
    });
    $('div.inline-related h3').css('cursor', 'move');
    $('div.inline-related').find('input[id$=order]').parents('div.form-row').hide();
});

//TabularInline

function TabularInlineSortableUpdateOrder() {
    $('.module table tbody tr').each(function(i) {
        //Find all visible inputs that don't have an id that ends in order
        //.val() gets the first non-blank value
        //So if it finds any value, the row has been filled in somehow
        if ($(this).find(':input:not(input[id$=order]):visible').val()) {
            $(this).find('input[id$=order]').val(i+1);
        }
        else {
            //Delete the row if there's a delete box
            $(this).find('input[id$=DELETE]').attr('checked', true);
        }
    });
}

jQuery(function($) {
    //Update order on save
    $('.submit-row :submit').click(TabularInlineSortableUpdateOrder);
    
    $('.module table tbody').sortable({
        axis: 'y',
        items: 'tr',
        containment: 'parent',
        update: TabularInlineSortableUpdateOrder
    });
    $('.module table.ui-sortable tbody tr').css('cursor', 'move');
    $('.module table').find('input[id$=order]').parent('td').hide();
    
    //Hide the order header
    $('.module table thead th').each(function(i){
        elem = $(this);
        if (elem.text().toLowerCase() == 'order') {
            elem.hide();
            elem.next('th').attr('colspan', elem.attr('colspan'));
        }
    });
});