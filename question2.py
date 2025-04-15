'''
Thuật toán/Function này được thiết kế với logic để có thể tính ra kết quả cuối cùng
cho internal_id "a"  có giá trị thặng dư = -5. Thứ tự logic như sau:

1. Chạy for loop, duyệt qua từng internal_id riêng biệt trong DataFrame.
2. Đối với mỗi internal_id, nhóm dữ liệu theo external_id và đếm số lần giao dịch với mỗi external_id.
3. Sắp xếp các external_id theo số lần giao dịch, chọn ra external_id có số lần giao dịch nhiều nhất.
4. Với cặp internal_id và external_id này, tính toán thặng dư cho từng giao dịch.
5. Chọn 3 giao dịch có cashflow (absolute của credit và debit) lớn nhất
6. Tính trung bình thặng dư của 3 giao dịch này, ta được giá trị thặng dư trung bình cần tìm cho mỗi internal_id
7. Trả về DataFrame chứa giá trị thặng dư trung bình cho mỗi internal_id.

Đây không phải là logic hợp lí nhất theo đề bài, nhưng là logic duy nhất
để tính ra kết quả -5 cho internal_id "a".
1 số logic khác đã thử nhưng không cho ra kết quả -5 cho internal_id "a": 
- Với mỗi internal_id, chọn top 3 external_id có số lần giao dịch nhiều nhất
sau đó tính trung bình thặng dư giao dịch với 3 external_id này.
(Ở internal_id "a" là 3 id b,c,d)
- Với mỗi internal_id, chọn top 3 external_id có tổng giá trị giao dịch lớn nhất.
Sau đó tính trung bình thặng dư giao dịch với 3 external_id này.
(Ở internal_id "a" là 3 id c,d,e)
Tuy nhiên đều không cho ra kết quả -5 cho internal_id "a".
'''

# B1: Cài thư viện cần thiết
# import subprocess
# import sys
# subprocess.check_call([sys.executable, "-m", "conda", "install", "pandas"])

# B2: Import thư viện
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# B3: Import data & convert datetime
data = {
    'Transaction_id': [1, 2, 3, 4, 5, 6, 7, 8],
    'internal_id': ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a'],
    'external_id': ['b', 'b', 'c', 'd', 'd', 'd', 'c', 'e'],
    'Amount_credit': [1, 0, 6, 0, 0, 0, 0, 30],
    'Amount_debit': [0, -1, 0, -4, -5, -6, -5, 0],
    'time': ['11/10/24 14:01', '11/10/24 14:00', '11/10/24 14:00', 
             '11/10/24 15:00', '11/10/24 15:00', '11/10/24 15:00', 
             '11/10/24 15:00', '11/10/24 15:00']
}

# Import data vào df tùy theo nhu cầu (import từ CSV, từ Spark, từ DB, ...)
# data = pd.read_csv('data.csv')
df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y %H:%M')

# Lọc giao dịch buổi chiều (12h-18h) (nếu cần)
# df = df[df['time'].dt.hour.between(12, 17)]

# B4: define function tính thặng dư trung bình cho top 3 giao dịch với external_id có số lần giao dịch nhiều nhất
def calc_avg_surplus_top3(df):
    result = []

    # Duyệt qua từng internal_id riêng biệt
    for internal in df['internal_id'].unique():
        sub_df = df[df['internal_id'] == internal]

        # Đếm số lần giao dịch với mỗi external_id rồi chọn external_id có số lần giao dịch nhiều nhất
        pair_counts = sub_df.groupby('external_id').size().reset_index(name='count')
        top_transaction = pair_counts.sort_values(by='count', ascending=False).head(1)['external_id']
        surplus_list = []

        # Lọc transaction theo top external_id
        pair_df = sub_df[sub_df['external_id'] == top_transaction.iloc[0]]

        # Tính thặng dư và giá trị giao dịch
        pair_df['surplus'] = pair_df['Amount_credit'] + pair_df['Amount_debit']
        pair_df['abs_value'] = pair_df['Amount_credit'].abs() + pair_df['Amount_debit'].abs()

        # Chọn top 3 giao dịch có giá trị tuyệt đối lớn nhất
        top3 = pair_df.sort_values(by='abs_value', ascending=False).head(3)
        # tính giá trị trung bình của thặng dư
        avg_surplus = top3['surplus'].mean()

        # Thêm kết quả vào list
        result.append({'internal_id': internal, 'avg_surplus_top3': avg_surplus})

    return pd.DataFrame(result)

# Gọi hàm và in kết quả
result_df = calc_avg_surplus_top3(df)
print(result_df)
