
import streamlit as st
import datetime 

### Configurazione dell'interfaccia mobile

st.set_page_config(page_title="COT Mobile Analyzer", layout="centered") 

st.title("📊 COT Mobile Analyzer")
st.caption("Mani Forti Momentum & Sentiment") 

### Database dei dati simulato (aggiornato al 2026)

cot_database = {
"PALLADIUM (NYMEX)": {
"net_pos": "-4,210 contratti",
"w1": "+2.3% (Ricoperture)",
"m1": "-5.1% (Distribuzione)",
"m3": "-18.5% (Trend Orso)",
"y1": "12% (Minimi Storici)",
"sentiment": "💡 IPERVENDUTO / OPPORTUNITÀ",
"details": "I grandi speculatori (Managed Money) sono vicini al massimo pessimismo storico degli ultimi 12 mesi. Storicamente, questo livello sul Palladio anticipa rimbalzi violenti dovuti a short-squeeze.",
"status": "success"
},
"GOLD (COMEX)": {
"net_pos": "+215,400 contratti",
"w1": "+0.8% (Accumulo)",
"m1": "+6.4% (Forte Spinta)",
"m3": "+22.1% (Trend Toro)",
"y1": "91% (Massimi Storici)",
"sentiment": "⚠️ IPERCOMPRATO / ATTENZIONE",
"details": "L'oro si trova al 91° percentile (COT Index) a 1 anno. I fondi speculativi sono estremamente esposti al rialzo. Il rischio di prese di profitto repentine nel breve periodo è molto alto.",
"status": "error"
},
"CRUDE OIL WTI (NYMEX)": {
"net_pos": "+142,800 contratti",
"w1": "-1.2% (Prese profitto)",
"m1": "+1.1% (Stabile)",
"m3": "-4.5% (Contrazione)",
"y1": "48% (Fase Neutra)",
"sentiment": "📊 NEUTRO / CONSOLIDAMENTO",
"details": "Il posizionamento sul Petrolio è bilanciato. Le mani forti non stanno prendendo una direzione netta sulle scadenze a lungo termine. Mercato ideale per strategie di trading range.",
"status": "info"
},
"S&P 500 (CME)": {
"net_pos": "+89,150 contratti",
"w1": "+1.5% (Nuovi Long)",
"m1": "+3.9% (Estensione)",
"m3": "+11.2% (Trend Solido)",
"y1": "76% (Rialzista)",
"sentiment": "📈 TREND TORO CONFERMATO",
"details": "Gli Asset Manager continuano ad aumentare l'esposizione long sull'indice azionario. Struttura macroeconomica sana nel medio periodo, supportata dai flussi istituzionali.",
"status": "info"
}
} 

### Menu a tendina per lo smartphone

selected = st.selectbox("Seleziona Mercato:", list(cot_database.keys()))
data = cot_database[selected] 

st.markdown("---") 

### Visualizzazione metriche compatte stile smartphone

st.metric("Posizione Netta", data["net_pos"]) 

col1, col2 = st.columns(2)
with col1:
st.markdown(f"**Variazione 1W:** {data['w1']}")
st.markdown(f"**Variazione 1M:** {data['m1']}")
with col2:
