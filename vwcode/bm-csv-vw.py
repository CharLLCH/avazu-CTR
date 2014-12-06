#coding=utf-8

from datetime import datetime

def csv_to_vw(loc_csv, loc_output, train=True):
    start = datetime.now()
    print("\nTurning %s into %s. Is_train_set? %s"%(loc_csv,loc_output,train))
    i = open(loc_csv, "r")
    j = open(loc_output, 'wb')
    counter=0
    with i as infile:
        line_count=0
        for line in infile:
            # to counter the header
            if line_count==0:
                line_count=1
                continue
            # The data has all categorical features
            #numerical_features = ""
            categorical_features = ""
            counter = counter+1
            #print counter
            line = line.split(",")
            if train:
                #working on the date column. We will take day , hour
                a = line[2]
                new_date= datetime(int("20"+a[0:2]),int(a[2:4]),int(a[4:6]))
                day = new_date.strftime("%A")
                hour= a[6:8]
                categorical_features += " |hr %s" % hour
                categorical_features += " |day %s" % day
                # 24 columns in data    
                for i in range(3,24):
                    if line[i] != "":
                        categorical_features += "|c%s %s" % (str(i),line[i])
            else:
                a = line[1]
                new_date= datetime(int("20"+a[0:2]),int(a[2:4]),int(a[4:6]))
                day = new_date.strftime("%A")
                hour= a[6:8]
                categorical_features += " |hr %s" % hour
                categorical_features += " |day %s" % day
                for i in range(2,23):
                    if line[i] != "":
                        categorical_features += " |c%s %s" % (str(i+1),line[i])
  #Creating the labels
            #print "a"
            if train: #we care about labels
                if line[1] == "1":
                    label = 1
                else:
                    label = -1 #we set negative label to -1
                #print (numerical_features)
                #print categorical_features
                j.write( "%s '%s %s\n" % (label,line[0],categorical_features))

            else: #we dont care about labels
                #print ( "1 '%s |i%s |c%s\n" % (line[0],numerical_features,categorical_features) )
                j.write( "1 '%s %s\n" % (line[0],categorical_features) )

  #Reporting progress
            #print counter
            if counter % 1000000 == 0:
                print("%s\t%s"%(counter, str(datetime.now() - start)))

    print("\n %s Task execution time:\n\t%s"%(counter, str(datetime.now() - start)))

#csv_to_vw("/Users/RahulAgarwal/kaggle_cpr/train", "/Users/RahulAgarwal/kaggle_cpr/click.train_original_data.vw",train=True)
#csv_to_vw("/Users/RahulAgarwal/kaggle_cpr/test", "/Users/RahulAgarwal/kaggle_cpr/click.test_original_data.vw",train=False)
