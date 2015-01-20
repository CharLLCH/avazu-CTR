from csv import DictReader
import csv

train = 'C:/RWD/AVAZU.Click-Through Rate Prediction/train/train.csv'  

#You can live out any one of the variables if you want simple by using #
def data(path):
    for t, row in enumerate(DictReader(open(path))):
        id = row['id']
        click = int(row['click'])
        hour = int(row['hour'])
        C1 = int(row['C1'])
        banner_pos = int(row['banner_pos'])
        site_id = row['site_id']
        site_domain = row['site_domain']
        site_category = row['site_category']
        app_id = row['app_id']
        app_domain = row['app_domain']		
        app_category = row['app_category']
        device_id = row['device_id']
        device_ip = row['device_ip']
        device_model = row['device_model']		
        device_type = int(row['device_type'])
        device_conn_type = int(row['device_conn_type'])
        C14 = int(row['C14'])
        C15 = int(row['C15'])
        C16 = int(row['C16'])
        C17 = int(row['C17'])
        C18 = int(row['C18'])
        C19 = int(row['C19'])
        C20 = int(row['C20'])
        C21 = int(row['C21'])

        x = [id,click,hour,C1,banner_pos,site_id,site_domain,site_category,app_id,app_domain,app_category,device_id,device_ip,device_model,device_type,device_conn_type,C14,C15,C16,C17,C18,C19,C20,C21]

        yield t, x 

x_names = ["id","click","hour","C1","banner_pos","site_id","site_domain","site_category","app_id","app_domain","app_category","device_id","device_ip","device_model","device_type","device_conn_type","C14","C15","C16","C17","C18","C19","C20","C21"]

# There are approximately 40.000.000 rows in train data. Setting holdout = 40 while sample one row every 40 ~= 1.000.000 rows
holdout = 40

sample = csv.writer(open("sample.csv", 'w'))
sample.writerow(x_names)

for t, x in data(train): 
    if (holdout and t % holdout == 0):
        sample.writerow(x)
