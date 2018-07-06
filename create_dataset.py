import csv
import os
import errno
import shutil

# Receives a manipulated csv (final_database.csv) with the 7000 images and respective labels as input.
# Creates 1000 train folders (1 for each class 1 ... 1000)
# Moves 7000 images to their respective directories.

def create_dataset(file):

    dr = '/media/ruifgmonteiro/905EECF45EECD3CE/dr'
    dc = '/media/ruifgmonteiro/905EECF45EECD3CE/dc'
    train = '/home/ruifgmonteiro/Desktop/csv_desenvolvimentos/train'

    # Creates the train directories for classes 1 ... 1000
    if os.path.exists(train) == False:
        os.mkdir(train)

    for index in range(1, 1001):
        try:
            class_dir = os.path.join(train, str(index))
            os.makedirs(class_dir)

        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    # Reads csv and appends it to a list
    img_folder_list = []
    with open(database, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        for i in csv_reader:
            img_folder_list.append(i)

    # Moves the images from source folders (dc or dr) to respective train folders
    for file in img_folder_list:
        if file[0] in os.listdir(dr):
            print(str(file[0]) + " exists in dr.")
            shutil.move(os.path.join(dr, str(file[0])), os.path.join(train,str(file[1]),str(file[0])))
            print(str(file[0]) + " has been moved with success.")
        elif file[0] in os.listdir(dc):
            print(str(file[0]) +" exists in dc.")
            shutil.move(os.path.join(dc, str(file[0])), os.path.join(train, str(file[1]), str(file[0])))
            print(str(file[0]) + " has been moved with success.")
        else:
            print("Error: " + str(file[0]) + " does not exist in the specified directories.")

database = '/home/ruifgmonteiro/Desktop/csv_desenvolvimentos/CSV_Handling/final_database.csv'
create_dataset(database)