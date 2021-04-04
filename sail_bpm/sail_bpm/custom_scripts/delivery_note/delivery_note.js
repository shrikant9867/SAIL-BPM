/*frappe.ui.form.on("Delivery Note ", {
	
	refresh: function(frm){
		

	}	
	
});

frappe.ui.form.on("Delivery Note Item", "wt_range", function(frm, cdt, cdn) { // notice the presence of cdt and cdn
// that means that child doctype and child docname are passed to function and hence you can know what 
   // row was modified and triggered
    var item = locals[cdt][cdn]; // this is where the magic happens
    // locals is a global array that contains all the local documents opened by the user
    // item is the row that the user is working with
    // to what you need to do and update it back
    
    if (item.number_of_pieces == undefined ||item.number_of_pieces == ''   )
    {
    	item.number_of_pieces =0 
    }
    if (item.wt_range == undefined ||item.wt_range == ''   )
    {
    	item.wt_range = 0 
    }
    item.qty = item.number_of_pieces * item.wt_range; // remember to refresh the field to see the changes in the UI
    console.log(item.qty,"set1")
    frm.refresh_field('Delivery Note Item');
});

frappe.ui.form.on("Delivery Note Item", "number_of_pieces", function(frm, cdt, cdn) { // notice the presence of cdt and cdn
// that means that child doctype and child docname are passed to function and hence you can know what 
   // row was modified and triggered
    var item = locals[cdt][cdn]; // this is where the magic happens
    // locals is a global array that contains all the local documents opened by the user
    // item is the row that the user is working with
    // to what you need to do and update it back
 
    if(item.number_of_pieces == undefined || item.number_of_pieces == '')
    {
    	item.number_of_pieces =0; 
    }
    if(item.wt_range == undefined ||item.wt_range == '' )
    {
    	item.wt_range =0; 
    }
   item.qty = item.number_of_pieces * item.wt_range; // remember to refresh the field to see the changes in the UI
   console.log(item.qty,"set2")
    frm.refresh_field('Delivery Note Item');
});

frappe.ui.form.on("Delivery Note Item", {
  'length': function(frm,cdt,cdn) {
    // your validation logic here
        var item = locals[cdt][cdn]; // this is where the magic happens
    // locals is a global array that contains all the local documents opened by the user
    // item is the row that the user is working with
    // to what you need to do and update it back
 
    if(item.number_of_pieces == undefined || item.number_of_pieces == '')
    {
    	item.number_of_pieces =0; 
    }
    if(item.wt_range == undefined ||item.wt_range == '' )
    {
    	item.wt_range =0; 
    }
   item.qty = item.number_of_pieces * item.wt_range; // remember to refresh the field to see the changes in the UI
   console.log(item.qty,"length")
    frm.refresh_field('Delivery Note Item');
  }
})
*/

frappe.ui.form.on("Delivery Note", {
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

frappe.ui.form.on("Delivery Note Item", {
    number_of_pieces: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frm.events.calculate_wt_range(frm, row);
    },
    qty: function(frm, cdt, cdn) {
        var row = locals[cdt][cdn];
        frm.events.calculate_wt_range(frm, row);
    }
})