import datetime
import aws_signer
import json

host='a7zgalw2j0.execute-api.us-east-1.amazonaws.com'

def get_body_validate_client(channel, client_id, phone_number, value):
	t = datetime.datetime.utcnow()
	date_stamp = t.strftime('%Y%m%d')

	message_id = date_stamp
	request_date = date_stamp

	validateClientRQ={}
	validateClientRQ['phoneNumber'] = phone_number
	validateClientRQ['value'] = value

	any_arr={}
	any_arr['validateClientRQ']=validateClientRQ

	RequestBody={}
	RequestBody['any']=any_arr

	Destination={}
	Destination['ServiceName']='RechargeService'
	Destination['ServiceOperation']='validateClient'
	Destination['ServiceRegion']='C001'
	Destination['ServiceVersion']='1.4.0'

	RequestHeader={}
	RequestHeader['Channel'] = channel
	RequestHeader['RequestDate'] = request_date
	RequestHeader['MessageID'] = message_id
	RequestHeader['ClientID'] = client_id
	RequestHeader['Destination'] = Destination


	RequestMessage={}
	RequestMessage['RequestHeader']=RequestHeader
	RequestMessage['RequestBody']=RequestBody

	nequi_body={}
	nequi_body['RequestMessage']=RequestMessage

	json_nequi_body = json.dumps(nequi_body)
	return json_nequi_body

def get_body_cash_in_client(channel, client_id, phone_number, value, nit_code='001'):
	message_id = str(datetime.timestamp(datetime.now()))[0:9]
	request_date = str(datetime.now())[0:10]

	cashInRQ={}
	cashInRQ['phoneNumber'] = phone_number
	# Ccode: NIT del comercio en donde se esta haciendo la recarga
	cashInRQ['code'] = nit_code
	cashInRQ['value'] = value

	any_arr={}
	any_arr['cashInRQ']=cashInRQ

	RequestBody={}
	RequestBody['any']=any_arr

	Destination={}
	Destination['ServiceName']='CashInService'
	Destination['ServiceOperation']='cashIn'
	Destination['ServiceRegion']='C001'
	Destination['ServiceVersion']='1.0.0'

	RequestHeader={}
	RequestHeader['Channel'] = channel
	RequestHeader['RequestDate'] = request_date
	RequestHeader['MessageID'] = message_id
	RequestHeader['ClientID'] = client_id
	RequestHeader['Destination'] = Destination

	RequestMessage={}
	RequestMessage['RequestHeader']=RequestHeader
	RequestMessage['RequestBody']=RequestBody

	nequi_body={}
	nequi_body['RequestMessage']=RequestMessage

	json_nequi_body = json.dumps(nequi_body)
	return json_nequi_body

def make_signed_request(host,service_path,method,body, region = 'us-east-1'):
	service = 'execute-api'
	algorithm = 'AWS4-HMAC-SHA256'

def validate_client(client_id,phone_number,value):
	service_path = '/qa/-services-clientservice-validateclient'
	body = get_body_validate_client('MF-001', client_id, phone_number, value)
	response = aws_signer.make_signed_request(host, service_path, 'POST', body)
	print(response)
def cash_in_client(client_id,phone_number,value):
	service_path = "/-services-cashinservice-cashin"
	body = get_body_cash_in_client('MF-001', client_id, phone_number, value)
	print(body)
	response = make_signed_request(host,service_path,"POST",body)

validate_client('007','3998764643','2000')