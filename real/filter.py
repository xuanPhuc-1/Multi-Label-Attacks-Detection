import csv


def filter_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header
        header = next(reader)
        writer.writerow(header)

        # Filter rows
        for row in reader:
            # Kiểm tra xem số lượng cột có đúng không trước khi truy cập
            if len(row) == len(header):
                mitm = int(row[-2])  # Lấy giá trị của cột MITM
                miss_mac = int(row[-5])  # Lấy giá trị của cột MISS_MAC

                # Kiểm tra điều kiện và viết dòng vào tệp đầu ra nếu thỏa mãn
                if (mitm == 1 and miss_mac == 1) or (mitm == 0 and miss_mac == 0):
                    writer.writerow(row)


input_file = 'real/mitm.csv'
output_file = 'filtered_mitm.csv'
filter_csv(input_file, output_file)
print("Filtering complete!")
