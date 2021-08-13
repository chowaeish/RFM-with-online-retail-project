import pandas as pd
import seaborn as sbn
import numpy as np
import datetime as dt
#GÖREV 1
df_=pd.read_excel("online_retail_II.xlsx")
df=df_.copy()
df.head(10)
df.columns
df.describe()
df.shape
df["InvoiceDate"].max()
today_date=dt.datetime(2010,12,11)
def set_options():
    pd.set_option('display.max_columns', None)
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)


set_options()
df.describe()
df["Description"].nunique()
df["Description"].value_counts()
df.groupby("Description").agg({"Description" : "sum"})
df.groupby("Description").agg({"Quantity": "sum"}).sort_values("Quantity",ascending=False).head(5)
df=df[~df["Invoice"].str.contains("C",na=False)]
df["total_price"] = df["Price"] * df["Quantity"]
df.head(10)
df.isnull().sum()
df.dropna(inplace=True)
#Görev2 RFM metrikleri
#Recency: Müşterinin son alışveriş gününden RFM analizi yapacağımız güne olan mesafesi
#Frequency: Alışveriş sıklığı
#Monetary: Müşterinin harcadığı toplam ücret
RFM = df.groupby("Customer ID").agg({"InvoiceDate" : lambda InvoiceDate : (today_date - InvoiceDate.max()).days,
                                    "Invoice" : lambda Invoice : Invoice.nunique(),
                                    "total_price": lambda total_price: total_price.sum()})
RFM.head(5)
RFM.columns = ["recency", "frequency", "monetary"]
RFM.describe().T
FRM = RFM[RFM["monetary"] > 0]
#Görev3
RFM["recency_score"] = pd.qcut(RFM["recency"], 5, labels=[5, 4, 3, 2, 1])

RFM["frequency_score"] = pd.qcut(RFM["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

RFM["monetary_score"] = pd.qcut(RFM["monetary"], 5, labels=[1, 2, 3, 4, 5])


RFM["RFM_SCORE"] = (RFM['recency_score'].astype(str) +
                    RFM['frequency_score'].astype(str))
#GÖrev4
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
RFM['segment'] = RFM['RFM_SCORE'].replace(seg_map, regex=True)
RFM[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])
#GÖREV 5
new_df = pd.DataFrame()
new_df["new_customer_id"] = RFM[RFM["segment"] == "loyal_customers"].index
new_df.head()

new_df.to_csv("loyal_customers.csv")
# can't lose segmenti: bu segmentteki kişi sayısı 77 dir, kişi sayısı az olmasına karşın ortalama gelirleri gayet yüksek bu yüzden
# bu kişileri kaybetmemek adına kendilerini özel hissettirecek hediyeler verilmeli veya ara ara indirim yapılmalı.

#new_customers: Bunlar her zaman açık kapıdır, yenü müşteri sayımız iyi durumdadır ama harcamaları çok fazla değildir. Bunların ilgisini çekmek için yaptıkları alışverişlere uygun yeni ürünleri cüzi indirimlerle önerilmeli.

#ar_Risk: Bu segmentteki müşteriler churn edebilir. Gayet yüksek sayıdalar, bu sayıdan ötürü şirkette bir problem olduğunu düşünüyorum, bu problemin bulunup çözülmesi gerekir veya bu müşteriler aranıp özel ilgilenilmeli.




