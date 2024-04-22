import time
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd

sample = pd.read_csv('realtime.csv')

tag_ddos = ''
tag_slow_rate = ''
tag_mitm = ''
#  sudo hping3 -S --flood -V -p 80 10.20.0.10 --rand-source


if sample['SSIP'].values > 600:
    tag_ddos = 'DDOS '
if sample['SSIP'].values > 100 and sample['SFE'].values < 300:
    tag_slow_rate = 'Slow Rate '
if sample['MISS_MAC'].values == 1:
    tag_mitm = 'MITM '
if tag_ddos == '' and tag_slow_rate == '' and tag_mitm == '':
    tag = 'Normal'
else:
    tag = tag_ddos + tag_slow_rate + tag_mitm

print(tag)
# save tag to txt file
with open('result.txt', 'w') as f:
    f.write(tag)
    f.close()


def main():
    # Đọc dữ liệu từ file CSV, bỏ cột cuối cùng 'TAGS'
    df = pd.read_csv('real_dataset.csv').iloc[:, :-1]

    # Tách ma trận đặc trưng (X) và nhãn (y)
    # Bỏ ba cột nhãn để có ma trận đặc trưng X
    X = df.drop(columns=['DDOS', 'SLOW-RATE', 'MITM'])
    # Chọn ba cột nhãn để có ma trận nhãn y
    y = df[['DDOS', 'SLOW-RATE', 'MITM']]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    # Định nghĩa pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Chuẩn hóa dữ liệu
        # Sử dụng PCA để giảm chiều dữ liệu, chỉ giữ lại các thành phần giải thích được 95% phương sai
        ('pca', PCA(n_components=0.98))
    ])

    # Fit và transform dữ liệu
    X_train_scaled = pipeline.fit_transform(X_train)
    X_test_scaled = pipeline.transform(X_test)

    filename = 'real_NN'

    with open(filename, 'rb') as file:
        classifier = pickle.load(file)

    sample = pd.read_csv('realtime.csv')

    # print start time type h:m:s
    start_time = time.time()
    specific_case_scaled = pipeline.transform(sample)
    result = classifier.predict(specific_case_scaled)

    labels = []
    # Xác định nhãn cho mỗi phần tử
    for i, prob in enumerate(result[0]):
        if prob > 0.5:
            if i == 0:
                labels.append('DDoS')
            elif i == 1:
                labels.append('Slowrate')
            elif i == 2:
                labels.append('Mitm')
        else:
            labels.append('')
    print(labels)
