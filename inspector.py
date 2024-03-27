from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
import time

# Đọc dữ liệu từ file CSV, bỏ cột cuối cùng 'TAGS'
df = pd.read_csv('filtered6_dataset.csv').iloc[:, :-1]

# Tách ma trận đặc trưng (X) và nhãn (y)
# Bỏ ba cột nhãn để có ma trận đặc trưng X
X = df.drop(columns=['DDOS', 'SLOW-RATE', 'MITM'])
y = df[['DDOS', 'SLOW-RATE', 'MITM']]  # Chọn ba cột nhãn để có ma trận nhãn y

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


filename = 'NN'


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
# Đo thời gian kết thúc và tính toán thời gian thực thi
end_time = time.time()
execution_time = end_time - start_time

print("Response time:", execution_time, "seconds")
print(labels)
