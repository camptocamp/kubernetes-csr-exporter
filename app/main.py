from __future__ import print_function
import time
import kubernetes.client
from kubernetes import config
from kubernetes.client.rest import ApiException
from pprint import pprint
import json
from flask import Flask,render_template,Response
from prometheus_client import Gauge,generate_latest

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

c = Gauge('kube_csr_pending', 'List of unapproved CSR', ['name'])

app = Flask(__name__)

@app.route("/metrics")
def metrics():
  try:
    configuration = kubernetes.client.Configuration().load_incluster_config()

    with kubernetes.client.ApiClient(configuration) as api_client:
      api_instance = kubernetes.client.CertificatesV1beta1Api(api_client)

    certificates = api_instance.list_certificate_signing_request()
    for certificate in certificates.items:
      if certificate.status.certificate is None:
        c.labels(name=certificate.metadata.name).set(1)
      else:
        c.labels(name=certificate.metadata.name).set(0)
  except ApiException as e:
    print("Exception when calling CertificatesV1beta1Api->list_certificate_signing_request: %s\n" % e)
  except AttributeError:
    configuration = Configuration()
    configuration.assert_hostname = False

  return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host='0.0.0.0')