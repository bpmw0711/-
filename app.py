import streamlit as st

# 設定網頁標題與圖示
st.set_page_config(page_title="跨國稅務合規專家系統", page_icon="⚖️")

def main():
    st.title("⚖️ 跨國稅務合規審查專家系統")
    st.markdown("""
    本系統基於**知識工程**架構開發，旨在協助企業判斷跨境交易中的稅務義務。
    請根據目前的交易狀況選擇以下參數：
    """)

    st.sidebar.header("輸入特徵 (Input Features)")

    # 1. 交易主體判斷
    seller_type = st.sidebar.selectbox(
        "1. 銷售方(Seller)所在地點",
        ["境外公司 (Non-resident)", "台灣公司 (Domestic)"]
    )

    buyer_type = st.sidebar.selectbox(
        "2. 購買方(Buyer)身分",
        ["企業 (B2B - 有統編)", "個人 (B2C - 一般消費者)"]
    )

    # 2. 交易性質判定
    transaction_type = st.sidebar.selectbox(
        "3. 交易性質分類",
        ["電子勞務 (SaaS/串流/雲端)", "權利金 (商標/技術授權)", "實體貨物銷售", "技術服務費"]
    )

    # 3. 租稅協定判斷
    has_treaty = st.sidebar.radio("4. 雙邊是否有租稅協定 (DTA)?", ["是", "否"])
    
    annual_sales = 0
    if buyer_type == "個人 (B2C - 一般消費者)":
        annual_sales = st.sidebar.number_input("5. 該年度累計銷售額 (TWD)", value=0)

    # 推論引擎 (Inference Engine)
    st.subheader("🔍 專家診斷報告")
    
    diagnosis = []
    warning_level = "info"

    # 規則 1: 境外電商 B2C 營業稅規則
    if seller_type == "境外公司 (Non-resident)" and buyer_type == "個人 (B2C - 一般消費者)":
        if transaction_type == "電子勞務 (SaaS/串流/雲端)":
            if annual_sales >= 480000:
                diagnosis.append("✅ 觸發合規義務：賣方須在台灣辦理「稅籍登記」。")
                diagnosis.append("💰 稅務責任：須申報並繳納 5% 營業稅 (VAT)。")
                warning_level = "error"
            else:
                diagnosis.append("ℹ️ 尚未達門檻：年銷售額未達 48 萬，暫無需辦理稅籍登記。")

    # 規則 2: 權利金扣繳規則
    elif transaction_type == "權利金 (商標/技術授權)":
        if has_treaty == "是":
            diagnosis.append("✅ 適用租稅協定：扣繳稅率通常可由 20% 降至 10%。")
            diagnosis.append("📝 必要文件：請確保已取得對方的「居住者證明 (COR)」。")
            warning_level = "success"
        else:
            diagnosis.append("⚠️ 法定稅率：須按 20% 稅率進行就源扣繳。")
            warning_level = "warning"

    # 規則 3: B2B 技術服務
    elif buyer_type == "企業 (B2B - 有統編)" and transaction_type == "技術服務費":
        diagnosis.append("✅ 扣繳義務：買方給付時須進行就源扣繳 (通常為 20%)。")
        diagnosis.append("💡 專業建議：若屬境外提供且無境內來源，可嘗試申請所得稅法第 25 條核定貢獻度以降低稅賦。")

    # 規則 4: 實體貨物
    elif transaction_type == "實體貨物銷售":
        diagnosis.append("📦 關稅邏輯：不適用電子勞務稅法，請參考海關進口稅則與營業稅法進口章節。")

    else:
        diagnosis.append("❓ 需要更多數據：目前的組合不符合現有自動化規則，建議諮詢稅務專家。")

    # 顯示結果
    if warning_level == "success":
        st.success("\n".join(diagnosis))
    elif warning_level == "warning":
        st.warning("\n".join(diagnosis))
    elif warning_level == "error":
        st.error("\n".join(diagnosis))
    else:
        st.info("\n".join(diagnosis))

    st.divider()
    st.caption("本系統為專家系統作業演示，不構成正式法律或稅務諮詢建議。")

if __name__ == "__main__":
    main()