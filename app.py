import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 🌊 设置 Streamlit 页面主题
st.set_page_config(page_title="Chemical Hazard Database", layout="wide")

# ✅ 读取 GitHub 上的 CSV 文件
file_url = "https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/Chemical-hazard-database-20250314.csv"

# 🔵 自定义海洋主题样式
ocean_background = """
    <style>
        .stApp {
            background-color: #e0f7fa;
        }
        .stMarkdown {
            font-size: 18px;
        }
        .blue-box {
            background-color: #b3e5fc;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 22px;
            font-weight: bold;
            color: #01579b;
        }
    </style>
"""
st.markdown(ocean_background, unsafe_allow_html=True)

# 📌 **添加 大连理工大学 图标**
st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/dlut_logo.jpg", width=150)

# 🎉 **Welcome Banner**
st.markdown('<div class="blue-box">🌊 Welcome to Chemical Hazard Database 🔬 🌍</div>', unsafe_allow_html=True)

# 📌 **模型介绍**
st.write("""
A user-friendly software interface covering **ecotoxicological and hazard data estimates**, facilitating rapid **quantitative prediction of chemical toxicity** without relying on animal testing,  
supporting **marine ecological risk assessment**.
""")

# 📌 **添加模型示意图**
st.image("https://raw.githubusercontent.com/Zhu-lele/Chemical-Hazard-Database-for-marine-ecological-risk-assessment/main/model_diagram.png", caption="Deep Learning Model for Marine Ecological Risk Assessment")

# 📌 **模型描述**
st.write("""
A multi-task deep-learning model based on **molecular graph and exposure duration**, enables **end-to-end prediction of chemical toxicity** for 18 marine organisms spanning five phyla.
""")

# ✅ 读取数据
try:
    df = pd.read_csv(file_url)

    # 📊 **数据预览**
    st.write("### 🔬 Data Preview")
    st.dataframe(df)

    # 📈 **数据统计**
    st.write("### 📈 Data Statistics")
    st.write(df.describe())

    # 🎯 **Sidebar Filters**
    st.sidebar.header("🔍 Data Filters")

    # 用户可选择筛选列
    filter_column = st.sidebar.selectbox("Select column to filter", ["CAS", "Name", "SMILES"])
    
    # 获取唯一值
    unique_values = df[filter_column].dropna().unique()
    selected_value = st.sidebar.selectbox(f"Select {filter_column}", unique_values)
    
    # 过滤数据
    filtered_df = df[df[filter_column] == selected_value]
    st.write(f"### Filtered Data - {filter_column}: {selected_value}")
    st.dataframe(filtered_df)

    # 📥 **下载筛选后的数据**
    csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data (CSV)", data=csv_filtered, file_name="filtered_data.csv", mime="text/csv")

    # 📊 **可视化**
    st.sidebar.header("📊 Visualization Options")
    
    # 选择数值列
    numeric_columns = df.select_dtypes(include=["number"]).columns
    selected_num_col = st.sidebar.selectbox("Select a numeric column", numeric_columns)

    # 📊 **柱状图**
    st.write(f"### 📊 Bar Chart - {selected_num_col} (CAS as X-axis)")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=df["CAS"][:10], y=df[selected_num_col][:10], palette="Blues", ax=ax)
    ax.set_xlabel("CAS Number")
    ax.set_ylabel(selected_num_col)
    ax.set_title(f"{selected_num_col} Distribution (Top 10 by CAS)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 📈 **折线图**
    st.write(f"### 📈 Line Chart - {selected_num_col} (CAS as X-axis)")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["CAS"][:30], df[selected_num_col][:30], marker="o", linestyle="-", color="#01579b")
    ax.set_xlabel("CAS Number")
    ax.set_ylabel(selected_num_col)
    ax.set_title(f"{selected_num_col} Trend (First 30 CAS)")
    plt.xticks(rotation=45)
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Failed to load file: {e}")
