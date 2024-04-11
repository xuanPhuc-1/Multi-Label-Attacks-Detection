import csv
from collections import Counter

while True:
    # Đọc file CSV và đếm số lần xuất hiện của mỗi địa chỉ MAC
    with open("data/ethsrc.csv", mode="r") as file:
        csvFile = csv.reader(file)
        # Đếm số lần xuất hiện của mỗi địa chỉ MAC
        count = Counter([rows[0] for rows in csvFile])
        # Lấy ra địa chỉ MAC có số lần xuất hiện nhiều nhất
        # nếu file rỗng thì banned_address = ""
        if count:
            banned_address = count.most_common(1)[0][0]
        else:
            banned_address = ""
    print(f"Banned address: {banned_address}")
