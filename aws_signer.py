import sys, os, base64, datetime, hashlib, hmac 
import requests

def make_signed_request(host, service_path, method, body):
  service = 'execute-api'
  region = 'us-east-1'
  endpoint = 'https://' + host + service_path
  content_type = 'application/json'
  request_parameters = body
  #[Provide your own keys]: https://conecta.nequi.com.co/content/consultas
  api_key = ''
  access_key = ''
  secret_key = ''

  if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()
  t = datetime.datetime.utcnow()
  amz_date = t.strftime('%Y%m%dT%H%M%SZ')
  date_stamp = t.strftime('%Y%m%d')
  canonical_uri = '/qa/-services-clientservice-validateclient'
  canonical_querystring = ''
  canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-api-key:' + api_key + '\n'
  signed_headers = 'content-type;host;x-api-key'
  payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()
  canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash
  algorithm = 'AWS4-HMAC-SHA256'
  credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
  string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
  signing_key = getSignatureKey(secret_key, date_stamp, region, service)
  signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()
  authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
  headers = {'Content-Type':content_type,
             'x-amz-date':amz_date,
             'x-api-key':api_key,
             'Authorization':authorization_header}
  #print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
  #print('Request URL = ' + endpoint)
  r = requests.post(endpoint, data=request_parameters, headers=headers)
  #print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
  #print('Response code: %d\n' % r.status_code)
  #print(r.text)
  return r.text


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

 



 


