
import streamlit as st
import pandas as pd
import requests 

### 1. Configurazione dell'interfaccia mobile

st.set_page_config(page_title="COT Real-Time Analyzer", layout="centered") 

st.title("📊 COT Live Analyzer")
st.caption("Dati reali e storici prelevati in tempo reale dai server CFTC") 

### Mappa dei mercati monitorati e dei loro esatti codici CFTC (Market Code / Contract Market Name)

### Per metalli e petrolio usiamo il report "Disaggregated" (Managed Money)

### Per l'S&P 500 usiamo il report "TFF" (Leveraged Funds / Asset Managers)

MARKET_MAP = {
"PALLADIUM (NYMEX)": {"id": "PALLADIUM - NEW YORK MERCANTILE EXCHANGE", "type": "disaggregated"},
"GOLD (COMEX)": {"id": "GOLD - COMMODITY EXCHANGE INC.", "type": "disaggregated"},
"CRUDE OIL WTI (NYMEX)": {"id": "CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE EXCHANGE", "type": "disaggregated"},
"S&P 500 (CME)": {"id": "E-MINI S&P 500 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE", "type": "tff"}
} 

selected_market = st.selectbox("Seleziona Mercato:", list(MARKET_MAP.keys()))
market_info = MARKET_MAP[selected_market] 

### 2. Funzione di Download Dati tramite API Pubblica CFTC

@st.cache_data(ttl=3600)  # Conserva i dati in memoria per un'ora per non rallentare l'app
def fetch_cftc_data(market_name, report_type): 

### Endpoint API ufficiali della CFTC (Socrata)

if report_type == "disaggregated":
# Disaggregated Futures Only dataset
url = f"https://publicreporting.cftc.gov/resource/jx43-79vv.json?contract_market_name={market_name}&
𝑜𝑟𝑑𝑒𝑟

=𝑟𝑒𝑝𝑜𝑟𝑡𝑑𝑎𝑡𝑒𝑎𝑠𝑦𝑦𝑦𝑦𝑚𝑚𝑑𝑑𝐷𝐸𝑆𝐶

limit=52"
else:
# Traders in Financial Futures (TFF) Futures Only dataset
url = f"https://publicreporting.cftc.gov/resource/gpe6-w3vs.json?contract_market_name={market_name}&
𝑜𝑟𝑑𝑒𝑟

=𝑟𝑒𝑝𝑜𝑟𝑡𝑑𝑎𝑡𝑒𝑎𝑠𝑦𝑦𝑦𝑦𝑚𝑚𝑑𝑑𝐷𝐸𝑆𝐶

limit=52" 

response = requests.get(url)
if response.status_code != 200:
return None 

data = response.json()
if not data:
return None 

df = pd.DataFrame(data) 

### Uniformiamo i nomi dei campi in base al tipo di report

if report_type == "disaggregated":
df["long_pos"] = pd.to_numeric(df["m_money_positions_long_all"])
df["short_pos"] = pd.to_numeric(df["m_money_positions_short_all"])
else:
# Nel TFF sommiamo Leveraged e Asset Manager o tracciamo i Leveraged Funds (Mani Forti speculative)
df["long_pos"] = pd.to_numeric(df["lev_money_positions_long_all"])
df["short_pos"] = pd.to_numeric(df["lev_money_positions_short_all"]) 

df["net_position"] = df["long_pos"] - df["short_pos"]
df["date"] = pd.to_datetime(df["report_date_as_yyyy_mm_dd"])
return df.sort_values("date").reset_index(drop=True) 

### 3. Download e Calcolo Dinamico delle Metriche

with st.spinner("Connessione ai server governativi CFTC..."):
df_market = fetch_cftc_data(market_info["id"], market_info["type"]) 

if df_market is not None and not df_market.empty: 

### Estraiamo i record chiave per le finestre temporali storiche

current_row = df_market.iloc[-1] 

current_net = current_row["net_position"]
current_date = current_row["date"].strftime('%d/%m/%Y') 

### Calcolo variazioni (se lo storico ha abbastanza record)

w1_net = df_market.iloc[-2]["net_position"] if len(df_market) > 1 else current_net
m1_net = df_market.iloc[-5]["net_position"] if len(df_market) > 4 else current_net
m3_net = df_market.iloc[-13]["net_position"] if len(df_market) > 12 else current_net 

change_1w = current_net - w1_net
change_1m = current_net - m1_net
change_3m = current_net - m3_net 

### Calcolo COT Index (Percentile a 52 settimane)

min_52 = df_market["net_position"].min()
max_52 = df_market["net_position"].max()
cot_index = ((current_net - min_52) / (max_52 - min_52)) * 100 if max_52 != min_52 else 50 

### 4. Rendering Grafico dell'Interfaccia Mobile

st.markdown("---")
st.write(f"📅 **Dati aggiornati al:** {current_date}")
st.metric("Posizione Netta Mani Forti", f"{int(current_net):,}") 

st.write("### Variazioni dei Contratti")
st.write(f"📆 **1 Settimana (1W):** {int(change_1w):+}")
st.write(f"📅 **1 Mese (1M):** {int(change_1m):+}")
st.write(f"📊 **3 Mesi (3M):** {int(change_3m):+}")
st.write(f"📈 **COT Index (1Y):** {cot_index:.1f}%") 

st.markdown("---")
st.write("### Analisi del Sentiment") 

# Algoritmo decisionale automatico basato sul COT Index reale

if cot_index >= 85:
st.error(f"⚠️ IPERCOMPRATO STORICO ({cot_index:.1f}%)")
st.write(f"I fondi speculativi sono esposti al rialzo in modo estremo sul mercato {selected_market}. Elevato rischio di prese di profitto e potenziali inversioni ribassiste strutturali.")
elif cot_index <= 15:
st.success(f"💡 IPERVENDUTO STORICO / OPPORTUNITÀ ({cot_index:.1f}%)")
st.write(f"Il pessimismo su {selected_market} ha raggiunto livelli storici estremi. Le posizioni short sono sature; monitorare possibili segnali di inversione rialzista causati da ricoperture coatte (*short squeeze*).")
else:
st.info(f"📊 SENTIMENT NEUTRO ({cot_index:.1f}%)")
st.write(f"Il posizionamento istituzionale su {selected_market} si trova in una fascia mediana rispetto agli ultimi 12 mesi. Il trend attuale è guidato prevalentemente dalle dinamiche dei flussi standard.")

else:
st.error("❌ Errore nel recupero dati. Verifica la connessione o riprova più tardi.")
