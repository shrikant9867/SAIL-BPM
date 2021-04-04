frappe.ui.form.on("Stock Entry", {
    calculate_wt_range: function(frm, row) {
        if(row.qty > 0 && row.number_of_pieces > 0) {
            row.wt_range = flt(row.qty / row.number_of_pieces)
        }
        else {
            row.wt_range = 0
        }
        refresh_field("wt_range", row.name, "items");
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