import boto3
import datetime
from datetime import date
from datetime import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


td = date.today()
tm = date.today()+ datetime.timedelta(days=1)
time= time(5,0,0)
today = datetime.datetime.combine(td, time)
tomorrow = datetime.datetime.combine(tm, time)
client = boto3.client('connect')
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('QueueMetrics.json', scope)
client2 = gspread.authorize(creds)

# function to collect metric data for each prompt from Connect and then
# export the metrics to the Google Sheet that displays the dashboard

def lambda_handler(event, context):
    # dictionary of ID's for each prompt
    queueIDs = {
        'Access': '********-****-****-****-************',
        'GenComp': '********-****-****-****-************',
        'Canvas': '********-****-****-****-************',
        'Default': '********-****-****-****-************',
        'FIN': '********-****-****-****-************',
        'Fleming': '********-****-****-****-************',
        'Admin': '********-****-****-****-************',
        'MiWorkspace': '********-****-****-****-************'
    }

    # dictionary of metrics to collect for each prompt, reset to zero each time
    # function is called
    accessMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    genCompMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    canvasMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
	"CALLBACK_CONTACTS_HANDLED": 0
    }
    defaultMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    finMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    flemingMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    adminMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    miworkspaceMetrics = {
        "CONTACTS_QUEUED": 0,
        "SERVICE_LEVEL": 0,
        "CONTACTS_HANDLED": 0,
        "QUEUED_TIME": 0,
        "QUEUE_ANSWER_TIME": 0,
        "CONTACTS_ABANDONED": 0,
        "AGENTS_ONLINE": 0,
        "AGENTS_NON_PRODUCTIVE": 0,
        "AGENTS_AVAILABLE": 0,
        "CONTACTS_IN_QUEUE": 0,
        "OLDEST_CONTACT_AGE": 0,
		"CALLBACK_CONTACTS_HANDLED": 0
    }
    # list of metric dictionaries
    queueMetrics = [accessMetrics, genCompMetrics, canvasMetrics, defaultMetrics, finMetrics, flemingMetrics, adminMetrics, miworkspaceMetrics]
    # for each prompt, call Connect API to retrieve current metric data
    # metric data retrieved through two APIs, historic and real time metrics
    for i in range(8):
        response = client.get_metric_data(
            InstanceId= 'a351243b-6844-41b0-97d9-934414342d87',
            StartTime= today,
            EndTime= tomorrow,
            Filters= {
                'Queues': [
                    list(queueIDs.values())[i],
                ]
        },

            HistoricalMetrics= [
            {
                'Name': 'QUEUED_TIME',
                'Statistic': 'MAX',
                'Unit': 'SECONDS'
            },
		    {
                "Name": "CONTACTS_QUEUED",
                "Statistic": "SUM",
                "Unit": "COUNT"
            },
		    {
                "Name": "CONTACTS_HANDLED",
                "Statistic": "SUM",
                "Unit": "COUNT"
            },
		    {
                "Name": "QUEUE_ANSWER_TIME",
                "Statistic": "AVG",
                "Unit": "SECONDS"
            },
		    {
                "Name": "CONTACTS_ABANDONED",
                "Statistic": "SUM",
                "Unit": "COUNT"
            },
		    {
                "Name": "SERVICE_LEVEL",
                "Statistic": "AVG",
			    "Threshold": {
			    	"Comparison": "LT",
		    		"ThresholdValue": 60.0
		    		},
                "Unit": "PERCENT"
            },
		    {
                "Name": "CALLBACK_CONTACTS_HANDLED",
                "Statistic": "SUM",
                "Unit": "COUNT"
            }

        ],

    )
        response2 = client.get_current_metric_data(
            InstanceId= 'a351243b-6844-41b0-97d9-934414342d87',
            Filters= {
                'Queues': [
                    list(queueIDs.values())[i],
                ]
            },

            CurrentMetrics= [
                {
                'Name': 'AGENTS_ONLINE',
                'Unit': 'COUNT'
                },
                {
                'Name': 'AGENTS_AVAILABLE',
                'Unit': 'COUNT'
                },
                {
                'Name': 'AGENTS_NON_PRODUCTIVE',
                'Unit': 'COUNT'
                },
                {
                'Name': 'CONTACTS_IN_QUEUE',
                'Unit': 'COUNT'
                },
                {
                'Name': 'OLDEST_CONTACT_AGE',
                'Unit': 'SECONDS'
                },
        ],
    )
        # update dictionary with reponse from API calls
        metricCount = len(response['MetricResults'][0]['Collections'])
        for j in range(metricCount):
            name = response['MetricResults'][0]['Collections'][j]['Metric']['Name']
            value = response['MetricResults'][0]['Collections'][j]['Value']
            queueMetrics[i][name] = int(value)
        metricCount = len(response2['MetricResults'][0]['Collections'])
        for e in range(metricCount):
            name = response2['MetricResults'][0]['Collections'][e]['Metric']['Name']
            value = response2['MetricResults'][0]['Collections'][e]['Value']
            queueMetrics[i][name] = int(value)

    client2 = gspread.authorize(creds)
    # open Google Sheet to export data
    sheet = client2.open('ITS SC AWS SIGN').get_worksheet(0)
    if creds.access_token_expired:
        client2.login()
    cell_list = sheet.range('B2:M9')
    # create list of combined metrics in order to update all cells in one call 
    listMetrics = []
    for i in range(8):
        listMetrics += list(queueMetrics[i].values())
    i = 0;
    for cell in cell_list:
        cell.value = listMetrics[i]
        i += 1
    # update sheet with list of metrics
    sheet.update_cells(cell_list)
    # return current metrics
    return queueMetrics
