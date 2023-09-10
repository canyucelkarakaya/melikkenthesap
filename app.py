import streamlit as st
import pandas as pd

# Excel dosyasını oku
df = pd.read_excel('hesaptakip.xlsx')

# "GELİR NEDENİ" sütununda "2021 YILINDAN DEVİR" ve "2022 YILINDAN DEVİR" değerlerini içeren satırları filtrele
df = df[~df['GELİR NEDENİ'].isin(["2021 YILINDAN DEVİR", "2022 YILINDAN DEVİR"])]

# Toplam aidat gelirlerini hesapla
toplam_aidat_geliri = df['AİDAT GELİR'].sum()

# Toplam aidat giderlerini hesapla
toplam_aidat_gider = df['AİDAT GİDER'].sum()

# Aidat hesabını hesapla
aidat_hesabi = toplam_aidat_geliri - toplam_aidat_gider

# Toplam demirbaş gelirlerini hesapla
toplam_demirbas_geliri = df['DEMİRBAŞ GELİR'].sum()

# Toplam demirbaş giderlerini hesapla
toplam_demirbas_gider = df['DEMİRBAŞ GİDER'].sum()

# Demirbaş hesabını hesapla
demirbas_hesabi = toplam_demirbas_geliri - toplam_demirbas_gider

genel_hesap = aidat_hesabi + demirbas_hesabi

# Streamlit uygulamasını oluştur
st.title("MELİKKENT B APARTMANI")
st.header("GENEL HESAP:")

# Genel hesap sonucunu büyük yazı ve kalın olarak göster
st.markdown(f"<h1 style='text-align:center;color:#ff5733;'>{genel_hesap:.2f}</h1>", unsafe_allow_html=True)

# Streamlit uygulamasını oluştur
st.header("AİDAT HESABI:")

# Aidat hesabını göster
st.markdown(f"<h1 style='text-align:center;color:#ff5733;'>{aidat_hesabi:.2f}</h1>", unsafe_allow_html=True)

# Streamlit uygulamasını oluştur
st.header("DEMİRBAŞ HESABI:")

# Demirbaş hesabını göster
st.markdown(f"<h1 style='text-align:center;color:#ff5733;'>{demirbas_hesabi:.2f}</h1>", unsafe_allow_html=True)


st.write("///////////////////////////////////////////////////////////////////////")

# Excel dosyasını oku
df = pd.read_excel('hesaptakip.xlsx')

# Sayfayı 2 bölüme bölelim
sol_bolum, sag_bolum = st.columns([2, 1])

# Sol bölümde filtreler
with sol_bolum:
    st.title("Yıllara Göre Hesap Dökümü")
    yil_secim = st.selectbox("Yıl Seçin", ["TÜMÜ"] + list(df['İLGİLİ YIL'].unique()))

# Sağ bölümde sonuçlar
with sag_bolum:
    if yil_secim != "TÜMÜ":
        # Yıla göre verileri filtrele
        df_filtre = df[df['İLGİLİ YIL'] == yil_secim]

        # Toplam aidat gelirlerini hesapla
        toplam_aidat_geliri = df_filtre['AİDAT GELİR'].sum()

        # Toplam aidat giderlerini hesapla
        toplam_aidat_gider = df_filtre['AİDAT GİDER'].sum()

        # Aidat hesabını hesapla
        aidat_hesabi = toplam_aidat_geliri - toplam_aidat_gider

        # Toplam demirbaş gelirlerini hesapla
        toplam_demirbas_geliri = df_filtre['DEMİRBAŞ GELİR'].sum()

        # Toplam demirbaş giderlerini hesapla
        toplam_demirbas_gider = df_filtre['DEMİRBAŞ GİDER'].sum()

        # Demirbaş hesabını hesapla
        demirbas_hesabi = toplam_demirbas_geliri - toplam_demirbas_gider

        # Sonuçları göster
        st.header("AİDAT HESABI:")
        
        st.markdown(f"<h2 style='text-align:center;color:#ff5733;'>{aidat_hesabi:.2f}</h2>", unsafe_allow_html=True)

        st.header("DEMİRBAŞ HESABI:")
        
        st.markdown(f"<h2 style='text-align:center;color:#ff5733;'>{demirbas_hesabi:.2f}</h2>", unsafe_allow_html=True)
    else:
        st.write("Lütfen yıl seçimi yapın.")




# Filtreler
st.title("Gider Nedenleri")
yil_secim = st.selectbox("Yıl Seçin", ["TÜMÜ"] + list(df['İLGİLİ YIL'].unique()), key="yil_secim")
ay_secim = st.selectbox("Ay Seçin", ["TÜMÜ"] + list(df['İLGİLİ AY'].unique()), key="ay_secim")

# Sonuçlar
if yil_secim != "TÜMÜ" and ay_secim != "TÜMÜ":
    df_filtre = df[(df['İLGİLİ YIL'] == yil_secim) & (df['İLGİLİ AY'] == ay_secim)]

    # Gider nedenlerini al
    gider_nedenleri = df_filtre['GİDER NEDENİ'].unique()

    # Sonuçları göster
    for neden in gider_nedenleri:
        aidat_gider = df_filtre[(df_filtre['GİDER NEDENİ'] == neden) & (df_filtre['AİDAT GİDER'].notna())]['AİDAT GİDER'].sum()
        demirbas_gider = df_filtre[(df_filtre['GİDER NEDENİ'] == neden) & (df_filtre['DEMİRBAŞ GİDER'].notna())]['DEMİRBAŞ GİDER'].sum()

        if aidat_gider != 0 or demirbas_gider != 0:
            st.header(neden)
        
        if aidat_gider != 0:
            st.write(f"Aidat Gideri: {aidat_gider:.2f}")
        if demirbas_gider != 0:
            st.write(f"Demirbaş Gideri: {demirbas_gider:.2f}")
else:
    st.write("Lütfen yıl ve ay seçimi yapın.")

# Başlık
st.title("Aidat Ödeme Tablosu")

# Yılları ve daire numaralarını al
yillar = sorted(df['İLGİLİ YIL'].unique())
daire_nolar = ['TÜMÜ'] + [f'Daire No {int(no)}' for no in sorted(df['İLGİLİ DAİRE NO'].dropna().unique())]

# Filtreleri oluştur
secilen_yil = st.selectbox("Yıl Seçin", yillar)
secilen_daire_no = st.selectbox("Daire No Seçin", daire_nolar)



# Filtreleri uygula
if secilen_yil != "TÜMÜ":
    veri = df[df['İLGİLİ YIL'] == secilen_yil]
    if secilen_daire_no != "TÜMÜ":
        secilen_daire_no = int(secilen_daire_no.split()[-1])
        veri = veri[veri['İLGİLİ DAİRE NO'] == secilen_daire_no]
else:
    if secilen_daire_no != "TÜMÜ":
        secilen_daire_no = int(secilen_daire_no.split()[-1])
        veri = df[df['İLGİLİ DAİRE NO'] == secilen_daire_no]
    else:
        veri = df

# Daire No Seçin
if secilen_daire_no != "TÜMÜ":
    st.write(f"Daire No {int(secilen_daire_no)}")
    st.header(f"Daire No {secilen_daire_no} - Aidat Ödeme Durumu ({secilen_yil})")
    data = []  # Tablo verilerini saklamak için bir liste oluşturun
    aylar = ["OCAK", "ŞUBAT", "MART", "NİSAN", "MAYIS", "HAZİRAN", "TEMMUZ", "AĞUSTOS", "EYLÜL", "EKİM", "KASIM", "ARALIK"]
    for ay in aylar:
        if veri[veri["İLGİLİ AY"] == ay]["AİDAT GELİR"].notna().any():
            data.append("✔")
        else:
            data.append("❌")
    # Verileri tabloya çevirin ve gösterin
    st.write(pd.DataFrame([data], columns=aylar).to_html(index=False, escape=False), unsafe_allow_html=True)
else:
    st.write("Lütfen bir daire numarası seçin.")





