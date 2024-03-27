import csv
from collections import defaultdict


def count_last_column(filename):
    counts = defaultdict(int)

    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Loại bỏ khoảng trống và chuyển đổi thành chữ thường
            last_column = row[-1].strip().lower()
            counts[last_column] += 1

    return counts


def main():
    filename = 'real_dataset.csv'
    result = count_last_column(filename)
    print("Số lượng hàng theo cột cuối:")
    for value, count in result.items():
        print(f"{value}: {count}")


if __name__ == "__main__":
    main()
