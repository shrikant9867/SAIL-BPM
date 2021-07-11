import frappe
from frappe import _
from frappe.utils import cint

from erpnext.stock.doctype.serial_no.serial_no import get_item_details, \
get_auto_serial_nos, get_serial_nos

def process_serial_no(doc, method):
	# create serial numbers and update in stock entry item table 
	for i in doc.items:
		if not i.serial_no or (i.serial_no and len(i.serial_no.split('\n')) != i.qty):
			item_det = get_item_details(i.item_code)
			# args to create Serial Number
			args = frappe._dict({
				"company": doc.company
			})
			if cint(i.qty) > 0 and item_det.has_serial_no == 1 and item_det.serial_no_series:
				if not i.serial_no:
					serial_nos = get_auto_serial_nos(item_det.serial_no_series, i.qty)
					i.serial_no = serial_nos
					args.update({
						"item_code": i.item_code,
						"serial_no": i.serial_no,
						"actual_qty": i.qty
					})
					auto_make_serial_nos(args)
				# On Qty Change
				elif i.serial_no and len(i.serial_no.split('\n')) != i.qty:
					cur_serial_nos = i.serial_no.split('\n')
					# decreased qty
					if len(cur_serial_nos) > i.qty:
						i.serial_no = "\n".join(cur_serial_nos[:i.qty])
					# increased qty
					else:
						required_qty = i.qty - len(cur_serial_nos)
						new_serial_nos = get_auto_serial_nos(item_det.serial_no_series, required_qty)
						i.serial_no = i.serial_no + "\n" + new_serial_nos
						args.update({
							"item_code": i.item_code,
							"serial_no": new_serial_nos,
							"actual_qty": required_qty
						})
						auto_make_serial_nos(args)
	return True

def auto_make_serial_nos(args):
	try:
		serial_nos = get_serial_nos(args.get('serial_no'))
		args.pop("serial_no")
		item_code = args.get('item_code')
		for serial_no in serial_nos:
			if frappe.db.exists("Serial No", serial_no):
				sr = frappe.get_cached_doc("Serial No", serial_no)
				sr.update(args)
				sr.db_update()
			elif args.get('actual_qty', 0) > 0:
				sr = frappe.new_doc("Serial No")
				sr.update(args)
				sr.serial_no = serial_no
				sr.db_insert()
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), _("Auto Serial Number Creation"))
		frappe.throw(_("Something went wrong while creating Serial Numbers."))