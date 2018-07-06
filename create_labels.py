import csv

# Takes a sorted ground truth table (sorted_gtt.csv) and adds the labels to the respective reference
# and consumer images. Returns a list with the following pattern: [ref_image | cons_image | class]

def preprocess_csv(file):

    with open(sorted_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')

        ref_images = []
        cons_images = []
        labels = []
        total = []
        csv_row = 0
        label = 1
        r = 0

        for row in reader:
            if csv_row > 0:
                ref_img = row[0]
                cons_img = row[1]
                ref_images.append(ref_img)
                cons_images.append(cons_img)
                if csv_row > 1:
                    labels.append(label)
            csv_row += 1

            if csv_row > 2:
                if ref_images[r] == ref_images[r - 1]:
                    r += 1
                else:
                    if ref_images[r][36:] == ref_images[r-1][36:]:
                        r += 1
                    else:
                        label += 1
                        labels[r] = label
                        r += 1

        for (a, b, c) in zip(ref_images, cons_images, labels):
            comb = [a, b, c]
            total.append(comb)

    return total


# Writes the list returned by the previous function and writes it to a new csv: gtt_with_labels.

def write_new_csv(file):
    old_csv_list = preprocess_csv(sorted_csv)
    new_file = '/home/ruifgmonteiro/Desktop/csv_desenvolvimentos/CSV_Handling/gtt_with_labels.csv'
    with open(new_file, 'w', newline='') as newCsv:
        csv_writer = csv.writer(newCsv)
        csv_writer.writerows(old_csv_list)
    print('Writing completed.')

    return newCsv

sorted_csv = '/home/ruifgmonteiro/Desktop/csv_desenvolvimentos/CSV_Handling/sorted_gtt.csv'
write_new_csv(sorted_csv)
