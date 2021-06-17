frappe.ui.form.on("Stock Entry", {
    calculate_wt_range: function(frm, row) {
        if(row.qty > 0 && row.number_of_pieces > 0) {
            row.wt_range = flt(row.qty / row.number_of_pieces)
        }
        else {
            row.wt_range = 0
        }
        refresh_field("wt_range", row.name, "items");
    },

    refresh: function(frm) {
        // find item grid row and append print btn/icon
        var item_wrapper = frm.fields_dict.items.grid.wrapper
        var item_rows = item_wrapper.find('.grid-row').slice(1)
        $.each(item_rows, function(idx, r) {
            if(!$(r).find('.printb').length) {
                $(r).append('\
                    <span class="fa fa-print printb"></span> \
                ')
            }
        })
        //css
        $('.printb').css({
            "cursor": "pointer",
            "margin-left": -3,
            "font-size": "15px"
        })
        //capture row idx & open print preview
        $('.printb').click(function(e) {
            var idx = e.currentTarget.closest(".grid-row").getAttribute("data-idx") || 0
            window.open(frappe.urllib.get_full_url("/printview?"
                + "doctype=" + encodeURIComponent(frm.doc.doctype)
                + "&name=" + encodeURIComponent(frm.doc.name)
                + "&trigger_print=1"
                + "&format=Barcode Print"
                + "&idx="+ idx
                + "&no_letterhead=0"
                + "&_lang=en"
           ));
        })
    }
})

frappe.ui.form.on("Stock Entry Detail", {
    number_of_pieces: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frm.events.calculate_wt_range(frm, row);
    },
    qty: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frm.events.calculate_wt_range(frm, row);
    },
    wt_range: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frm.events.calculate_wt_range(frm, row);
    }
})