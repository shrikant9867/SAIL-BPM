from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
from frappe.utils import flt,today
from frappe import _
import decimal    
import json
from datetime import datetime, timedelta


@frappe.whitelist()
def get_delivery_note_data(doc):
	data = frappe.db.sql("""select item_code,qty,number_of_pieces,wt_range from `tabDelivery Note Item` where parent ="%s" order by item_code"""%(doc.name))
	data_aggregate = frappe.db.sql("""select item_code,sum(qty) as sumgrosswt,sum(number_of_pieces) as sum_qty from `tabDelivery Note Item` where parent ="%s" group by item_code"""%(doc.name))
	table_height=0
	sendata={}
	total_bundle=0
	total_weight=0
	data_to_send = ""
	last_data_aggregate_count =0
	for i in data_aggregate:
		last_data_aggregate_count += 1
		header = add_data(""" <table style ='width :200px'><tbody><tr class='cls_003' style='border: 1px solid black;'><th colspan ='4'  style='text-align:center' ><strong >%s</strong></th></tr>"""%(i[0]),table_height)
		table_height += 1
		header += add_data("""<tr ><td><strong>NO</strong></td><td><strong>Wt Range</strong></td><td><strong>Qty</strong></td><td><strong>Gross Wt</strong></td></tr>""",table_height)
		table_height += 1
		count=1
		for j in data:
			if j[0] == i[0]:
				header += add_data("""<tr><td>%s</td><td  align="right">%s</td><td align="right">%s</td><td align="right">%s</td></tr>"""%(count,'{:.3f}'.format(round(j[3], 3)),j[2],'{:.3f}'.format(round(j[1], 3))),table_height)
				table_height += 1
				count+=1
		header += add_data("""<tr><td><strong>%s</strong></td><td align="left"><strong>%s</strong></td><td align="right"><strong>%s</strong></td><td align="right"><strong>%s</strong></td></tr></tbody></table>"""%(count-1,"Bun",'{:.0f}'.format(round(i[2], 0)),'{:.3f}'.format(round(i[1], 3))),table_height)
		table_height += 1
		if last_data_aggregate_count == len(data_aggregate):
			header += add_data("""</div><p   align='justify'>&nbsp;</p></div>""",table_height)
		else:
			header += add_data("""<p   align='justify'>&nbsp;</p>""",table_height)
		table_height += 1

		data_to_send += header 
		total_bundle += count-1
		total_weight += i[1]
	
	headertable= """<table class = 'headertable'><tr><th>%s</th><th align="left"><strong>%s</strong></th><th>%s</th><th align="left"><strong>%s</strong></th></tr></table>"""%('Total Bundles',total_bundle,'Total Weight','{:.3f}'.format(round(total_weight, 3)))
	divtable = data_to_send
	sendata['divtable']=divtable
	sendata['headertable']=headertable
	return sendata

def add_data(data , num):
	
	if num%52 == 0:
		if ((num // 52)  )%4 ==0 or num ==0:
			if num ==0:
				return """ <div class='row'> <div class='column' style='margin-left:50px'  >""" + data
			else:
				return """ </tbody></table></div></div> <p >&nbsp;</p><div class='row'> <div class='column' style='margin-left:50px'  ><table style ='width :200px'><tbody>""" + data
		else:
			return """ </table></tbody></div><div class='column' style='margin-left:60px'><table style ='width :200px'><tbody>""" + data

	else:
		return data
