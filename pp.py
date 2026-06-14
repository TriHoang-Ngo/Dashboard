import streamlit as st
import pandas as pd

# 1. Cấu hình trang hiển thị của Dashboard
st.set_page_config(page_title="Dashboard Sản Xuất", layout="wide")

st.title("📊 HỆ THỐNG GIÁM SÁT TỶ LỆ PHẾ PHẨM ONLINE")
st.write("Dữ liệu được cập nhật tự động theo từng nhóm sản xuất.")

# 2. Tạo dữ liệu gốc
du_lieu = {
    "Nhóm": ["Nhóm 1", "Nhóm 2", "Nhóm 3", "Nhóm 4", "Nhóm 5"],
    "Sản lượng (Pcs)": [1200, 1450, 1100, 1350, 1250],
    "Số phế phẩm (Scrap)": [12, 25, 8, 40, 15]
}
df = pd.DataFrame(du_lieu)
df["Tỷ lệ lỗi (%)"] = (df["Số phế phẩm (Scrap)"] / df["Sản lượng (Pcs)"]) * 100

# 3. Làm bộ lọc tương tác trên giao diện (Thanh trượt chọn giới hạn lỗi)
st.sidebar.header("Bộ Lọc Dữ Liệu")
muc_canh_bao = st.sidebar.slider("Đặt mức cảnh báo lỗi tối đa (%)", 0.0, 5.0, 1.5, step=0.1)

# Lọc ra các nhóm có tỷ lệ lỗi vượt mức cảnh báo để hiển thị riêng
nhom_loi_cao = df[df["Tỷ lệ lỗi (%)"] > muc_canh_bao]

# 4. Thiết kế giao diện Dashboard thành các cột số liệu
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Bảng số liệu chi tiết")
    st.dataframe(df.style.format({"Tỷ lệ lỗi (%)": "{:.2f}%"}))

with col2:
    st.subheader("🚨 Nhóm vượt định mức an toàn")
    if not nhom_loi_cao.empty:
        st.error(f"Có {len(nhom_loi_cao)} nhóm vượt ngưỡng {muc_canh_bao}%!")
        st.dataframe(nhom_loi_cao)
    else:
        st.success(f"Tất cả các nhóm đều an toàn dưới {muc_canh_bao}%!")

# 5. Vẽ biểu đồ cột trực quan bằng công cụ tích hợp của Streamlit
st.subheader("📈 Biểu đồ so sánh tỷ lệ lỗi giữa các nhóm")
st.bar_chart(data=df, x="Nhóm", y="Tỷ lệ lỗi (%)", color="#DC143C")