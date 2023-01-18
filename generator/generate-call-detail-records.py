import csv
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta 
from faker import Faker
faker = Faker()

YEAR_RANGE = 5
MONTHS_IN_YEAR = 12
ROW_SIZE = 2000
CSV_HEADERS = ["start_datetime","translated_calling_number","translated_called_number","connect_datetime","disconnect_datetime","charged_duration","originating_carrier_id","originating_transit_carrier_id","terminating_carrier_id","terminating_transit_carrier_id","call_direction","service_type","release_cause_number","sip_response"]
OUTPUT_FOLDER = '../data/'
# DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%d-%m-%Y %H:%M" # 25-02-2021 11:53

for year_offset in range(YEAR_RANGE):
    # minus 1 year
    currentTimeDate = datetime.now() - relativedelta(years=year_offset)
    current_year = currentTimeDate.strftime('%Y')

    for month_index in range(MONTHS_IN_YEAR):
        current_month = int(month_index)+1
        csv_filename = f'call-detail-records-{current_year}-{current_month:02}.csv'
        print('csv_filename', csv_filename)

        with open(OUTPUT_FOLDER+ csv_filename, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', escapechar=',', quoting=csv.QUOTE_NONE)
            writer.writerow(CSV_HEADERS)
            for x in range(ROW_SIZE):

                start_date = datetime(int(current_year),int(current_month),1)
                end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
                # print('date range', start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                fake_datetime = faker.date_time_between(start_date,end_date)
                start_datetime = fake_datetime.strftime(DATE_FORMAT)

                connect_datetime = (fake_datetime + timedelta(seconds=1)).strftime(DATE_FORMAT)
                
                charged_duration = faker.random_number(digits=2)
                disconnect_datetime = (fake_datetime + timedelta(minutes=charged_duration)).strftime(DATE_FORMAT)

                translated_calling_number = faker.msisdn()
                originating_transit_carrier_id = faker.random_number(digits=1)
                terminating_carrier_id = faker.random_number(digits=1)
                call_direction = faker.random.choice([1, 2])

                service_type = faker.random.choice([1, 2, 3])
                
                # https://www.startelecom.ca/resources/q-850-cause-codes/
                CAUSE_CODE_NORMAL_CALL_CLEARING = 16
                CAUSE_CODE_NORMAL_USER_BUSY = 17
                CAUSE_CODE_NO_USER_RESPONDING = 18
                CAUSE_CODE_CALL_REJECTED = 21
                abnormal_cause_codes = faker.random.choice([CAUSE_CODE_NORMAL_USER_BUSY, CAUSE_CODE_NO_USER_RESPONDING, CAUSE_CODE_NO_USER_RESPONDING])
                release_cause_number = faker.random.choice([CAUSE_CODE_NORMAL_CALL_CLEARING, abnormal_cause_codes])

                # https://www.startelecom.ca/resources/sip-response-codes/
                SIP_CODE_OK = 200
                SIP_CODE_MULTIPLE_CHOICES = 300
                SIP_CODE_NOT_FOUND = 404
                SIP_CODE_SERVER_INTERNAL_ERROR = 500

                abnormal_sip_codes = faker.random.choice([SIP_CODE_MULTIPLE_CHOICES, SIP_CODE_NOT_FOUND, SIP_CODE_SERVER_INTERNAL_ERROR])
                sip_response = faker.random.choice([SIP_CODE_OK, abnormal_sip_codes])

                new_row = [start_datetime,translated_calling_number,translated_calling_number,connect_datetime,disconnect_datetime,charged_duration,originating_transit_carrier_id,originating_transit_carrier_id,terminating_carrier_id,terminating_carrier_id,call_direction,service_type,release_cause_number,sip_response]
                writer.writerow(new_row)
            file.close()
