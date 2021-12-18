from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import flt,today
from frappe import _


def validate(doc, method):
	for i in doc.items:
		if  not i.number_of_pieces:
			frappe.throw("Please add number of pieces.")
		if not i.wt_range:
			frappe.throw("Please add Wt Range")
		#we're already calculating it in client side
		#i.qty = i.wt_range * i.number_of_pieces