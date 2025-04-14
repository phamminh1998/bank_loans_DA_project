import pandas as pd

# Khởi tạo dữ liệu
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

df = pd.DataFrame(data)

# Chuyển đổi thời gian
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%y %H:%M')
df['surplus_value'] = df['Amount_credit'] + df['Amount_debit']
df['transaction_value'] = df['Amount_credit'].abs() + df['Amount_debit'].abs()


# Xử lý theo mỗi internal_id
results = []

for internal in df['internal_id'].unique():
    df_internal = df[df['internal_id'] == internal]

    # Tính tổng giá trị giao dịch theo external_id (theo abs)
    external_totals = (
        df_internal.groupby('external_id')['transaction_value']
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )

    top_externals = external_totals.index.tolist()

    # Lọc lại giao dịch chiều giữa internal và top external
    df_top = df_internal[df_internal['external_id'].isin(top_externals)]

    # Tính trung bình surplus
    avg_surplus = df_top['surplus_value'].mean()
    results.append(avg_surplus)

# Kết quả cuối cùng
final_result = sum(results) / len(results)
print("Giá trị thặng dư trung bình:", final_result)
