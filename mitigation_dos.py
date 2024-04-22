import csv
from collections import Counter
import time
while True:
    # Đọc file CSV và đếm số lần xuất hiện của mỗi địa chỉ MAC
    with open("data/ethsrc.csv", mode="r") as file:
        csvFile = csv.reader(file)
        # Đếm số lần xuất hiện của mỗi địa chỉ MAC
        try:
            count = Counter([rows[0] for rows in csvFile])
            # Lấy ra địa chỉ MAC có số lần xuất hiện nhiều nhất
            # nếu file rỗng thì banned_address = ""
            if count:
                banned_address = count.most_common(1)[0][0]
            else:
                banned_address = ""
        except IndexError:
            banned_address = ""
    with open("data/inport.csv", mode="r") as file:
        csvFile = csv.reader(file)
        # Đếm số lần xuất hiện của mỗi cổng vào
        try:
            count = Counter([rows[0] for rows in csvFile])
            # Lấy ra cổng vào có số lần xuất hiện nhiều nhất
            # nếu file rỗng thì banned_port = ""
            if count:
                banned_port = count.most_common(1)[0][0]
            else:
                banned_port = ""
        except IndexError:
            banned_port = ""
    with open("result.txt", "r") as file:
        if "Normal" not in file.read():
            print(
                f"Banned address: {banned_address} - Banned port: {banned_port}")
        else:
            print("Normal")
    time.sleep(1)
