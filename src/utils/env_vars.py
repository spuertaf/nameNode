import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\Admin\\Desktop\\dataNode\\src\\creds\\gs_creds.json"
os.environ["PATH_2_GS_INDEX"] = "gs://data-nodes-index/index.csv" 
os.environ["OK-status"] = "200" #int
os.environ["ERROR-status"] = "400" #int

### SERVICES

os.environ["HTTP_HOST"] = "0.0.0.0"
os.environ["HTTP_PORT"] = "80" #int
os.environ["GRPC_PORT"] = "[::]:50000"

