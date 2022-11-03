import csv
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta 
from faker import Faker
faker = Faker()

YEAR_RANGE = 5
MONTHS_IN_YEAR = 12
ROW_SIZE = 10000
CSV_HEADERS = ["start_datetime","translated_calling_number","translated_called_number","connect_datetime","disconnect_datetime","charged_duration","originating_carrier_id","originating_transit_carrier_id","terminating_carrier_id","terminating_transit_carrier_id","call_direction"]
OUTPUT_FOLDER = '../data/'

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
                start_datetime = fake_datetime.strftime("%d-%m-%Y %H:%M")
                connect_datetime = (fake_datetime + timedelta(seconds=1)).strftime("%d-%m-%Y %H:%M")
                
                charged_duration = faker.random_number(digits=2)
                disconnect_datetime = (fake_datetime + timedelta(minutes=charged_duration)).strftime("%d-%m-%Y %H:%M")

                translated_calling_number = faker.msisdn()
                originating_transit_carrier_id = faker.random_number(digits=1)
                terminating_carrier_id = faker.random_number(digits=1)
                call_direction = faker.random.choice([1, 2])

                new_row = [start_datetime,translated_calling_number,translated_calling_number,connect_datetime,disconnect_datetime,charged_duration,originating_transit_carrier_id,originating_transit_carrier_id,terminating_carrier_id,terminating_carrier_id,call_direction]
                writer.writerow(new_row)
            file.close()
