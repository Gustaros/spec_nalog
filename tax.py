import streamlit as st
import pandas as pd
from tax_const import *


st.title("Специальные налоговые режимы")

st.header("Ожидаемый доход")
income_col, option_col = st.columns(2)
with income_col:
    income = st.number_input("введите ожидаемый годовой доход", min_value=0, value=0)
with option_col:
    option = st.selectbox(
        "",
        ("₽", "К ₽", "МЛН ₽")
    )
if option == "К ₽":
    income = income * 1000
if option == "МЛН ₽":
    income = income * 1000000

workers = st.number_input("кол-во наемных работников", min_value=0, value=0)

days = 365

def add_lines(text):
    lines = text.split(';')
    result = ""
    for line in lines:
        result += f"""{line}\n"""
    return result


def calculate_tax(income, regime):
    if regime != "ПСН":
        tax = income * tax_rates[regime]
    else:
        tax = 1229.067 * workers + 176.66 * days
    return tax

accessed_regimes = []
def access_regime(income, regime):
    if income <= income_ranges[regime][1] and workers <= workers_ranges[regime][1]:
        access = st.success(f"Ваш налог: {calculate_tax(income, regime)}", icon="✅")
        accessed_regimes.append(regime)
    else:
        access = st.error('Режим не доступен', icon="🚨")
    return access


def regimes_analysis(income, regime):
    access_regime(income, regime)

    with st.popover("описание"):
        st.markdown(regime_descriptions[regime])
    
    with st.popover("лимиты и ограничения"):
        st.markdown(add_lines(regime_limits[regime]))




regime_columns = st.columns(4)
for i, regime in enumerate(regimes):
    with regime_columns[i]:
        st.header(regime)
        regimes_analysis(income, regime)


df = pd.DataFrame(
    {"Режим": accessed_regimes, "Налог на доход": [calculate_tax(income, r) for r in accessed_regimes]}
)

st.header("Сравнение налогов")
st.bar_chart(df, x="Режим", y="Налог на доход", color="Режим")


