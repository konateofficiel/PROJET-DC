import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import warnings
from plotly import express as px
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
import seaborn as sns

st.markdown("""
Cette application est conçu pour collecter les données sur le site [Expat-Dakar](https://www.expat-dakar.com/)
 en suivant ces liens :[Les appatements meublés](https://www.expat-dakar.com/appartements-meubles)--
[Les appartements à louer](https://www.expat-dakar.com/appartements-a-louer)
--[Les terrains à vendre](https://www.expat-dakar.com/terrains-a-vendre)

""")

df1=pd.read_csv('data/Dn/Appartements_a_louer.csv')
df2=pd.read_csv('data/Dn/Appartements_meubles.csv')
df3=pd.read_csv('data/Dn/Terrains.csv')

def trie(df,ad):
    with st.sidebar.header('LES ADRESSES DE CHOIX'):
        adresse=st.sidebar.multiselect("Choisissez une adresse où vous rechercher",df[ad].unique())
        if st.button('AFFICHER LES INFORMATIONS',11):
            df=df[df[ad].isin(adresse)]
            st.dataframe(df)


meubles,appart,terrain=pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
def charge(data, titre, indice) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    div.stSubheader {text-align:center}
    </style>""", unsafe_allow_html=True)
    

    if st.button(titre,indice):
        
        st.subheader('INFORMATIONS RELATIVES AU TABLEAU')
        st.write('DIMENSIONS DU TABLEAU : ' + str(data.shape[0]) + '  LIGNES  ET  ' + str(data.shape[1]) + ' COLONNES')
        st.dataframe(data)
        sns.pairplot(data)

# définir quelques styles liés aux box
st.markdown('''<style> .stButton>button {
    font-size: 12px;
    height: 1em;
    width: 20em;
}</style>''', unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center; color: black;'>PROJET DE DATA COLLECTION</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: blue;'>CONCEPTEUR : IBRAHIMA KONATE</h3>", unsafe_allow_html=True)

def terrains(n):
    df=pd.DataFrame()
    for i in range(1,int(n)+1): 
        la_liste=[]  
        url2=f'https://www.expat-dakar.com/terrains-a-vendre?page={i}'
        page=get(url2)
        soup=BeautifulSoup(page.text,'html.parser')
        soup2=soup.find_all('div',class_= 'listings-cards__list-item')

        for links in soup2:  
            try:
                link=links.find('a',class_='listing-card__inner')['href']
                infos=get(link)
                contener=BeautifulSoup(infos.content,'html.parser')
                Prix=contener.find('span',class_='listing-card__price__value 1').text.strip()
                adresse=contener.find('span',class_='listing-item__address-location').text.strip()
                Details=contener.find('h1',class_='listing-item__header').text.strip()
                superficie=contener.find('dd',class_='listing-item__properties__description').text.strip()
                img_link=contener.find('img',class_='gallery__image__resource vh-img')['src']
                liste={
                    'Details':Details,
                    'Adresse':adresse,
                    'Prix':Prix,
                    'Superficie':superficie,
                    'Image':img_link
                }
                la_liste.append(liste)
            except:
                pass
        DF=pd.DataFrame(la_liste)
        df=pd.concat([df,DF],axis=0).reset_index(drop = True)
    return df

def appart_a_louer(n):
   df=pd.DataFrame()
   for i in range(1,n+1):  
        la_liste=[] 
        url2=f'https://www.expat-dakar.com/appartements-a-louer?page={i}'
        page=get(url2)
        soup=BeautifulSoup(page.text,'html.parser')
        soup2=soup.find_all('div',class_= 'listings-cards__list-item')
        #link=soup2[1].find('a',class_='listing-card__inner')['href']
        for links in soup2:  
            try:
                link=links.find('a',class_='listing-card__inner')['href']
                infos=get(link)
                contener=BeautifulSoup(infos.content,'html.parser')
                Prix=contener.find('span',class_='listing-card__price__value 1').text.strip()
                adresse=contener.find('span',class_='listing-item__address-location').text.strip()
                Details=contener.find('h1',class_='listing-item__header').text.strip()
                pp=contener.find_all('dd',class_='listing-item__properties__description')
                superficie=pp[2].text.strip()
                nbc=pp[0].text.strip()
                img_link=contener.find('img',class_='gallery__image__resource vh-img')['src']
                liste={
                    'Details':Details,
                    'Adresse':adresse,
                    'Prix':Prix,
                    'Superficie':superficie,
                    'Chambre':nbc,
                    'Image':img_link
                }
                la_liste.append(liste)
            except:
                pass
        DF=pd.DataFrame(la_liste)
        df=pd.concat([df,DF],axis=0).reset_index(drop = True)
   return df  

def appartmeubles(nombre):
  df=pd.DataFrame()
  la_liste=[]
  for i in range(1,nombre+1):   
      url=f'https://www.expat-dakar.com/appartements-meubles?page={i}'
      page=get(url)
      soup=BeautifulSoup(page.text,'html.parser')
      soup1=soup.find_all('div',class_= 'listings-cards__list-item')
      for links in soup1:
          try:
              link=links.find('a',class_='listing-card__inner')['href']
              infos=get(link)
              contener=BeautifulSoup(infos.content,'html.parser')
              Prix=contener.find('span',class_='listing-card__price__value 1').text.strip()
              adresse=contener.find('span',class_='listing-item__address-location').text.strip()
              Details=contener.find('h1',class_='listing-item__header').text.strip()
              pp=contener.find_all('dd',class_='listing-item__properties__description')
              superficie=pp[2].text.strip()
              nbc=pp[0].text.strip()
              img_link=contener.find('img',class_='gallery__image__resource vh-img')['src']
              liste={
                  'Details':Details,
                  'Adresse':adresse,
                  'Prix':Prix,
                  'Superficie':superficie,
                  'Chambre':nbc,
                  'Image':img_link
              }
              la_liste.append(liste)
          except:
              pass
  df=pd.DataFrame(la_liste)
 
  return df

# Les filtres des DF

with st.sidebar.header('choix de database'):
    adresse=st.selectbox("Choisissez une la table",("Appartements à louer","Appartements meublés","Terrains à vendre"))
    if adresse.lower()=="Appartements à louer".lower():
        trie(df1,'Adresse')
    elif adresse.lower()=="Appartements meublés".lower():
        trie(df2,'adresse')
    else:
        trie(df3,'Adresse')

# Les recherches
with st.form('RECHERCHE D''INFORMATION'):
    Option = st.selectbox("SELECTIONNEZ UNE PAGE A SUIVRE POUR LES INFOS",("TERRAINS A VENDRES", "APPARTEMENTS A LOUER", "APPARTEMENTS MEUBLES"))

    nombre=st.text_input('ENTRER LE NOMBRE DE PAGES POUR LES INFORMATIONS')
    Bouton=st.form_submit_button('Chercher les resultats')
    if Bouton:
        st.markdown("<h4 style='text-align: enter; color=red;'>LES DONNEES TROUVEES SUR LE WEB PAR WEB SCRAPER</h4>",unsafe_allow_html=True)
        if Option.upper()=='APPARTEMENTS MEUBLES':
            meubles=appartmeubles(int(nombre))
            st.markdown("<h5 style='text-align: enter; color=blue;'>1-LES APPARTEMENTS MEUBLES</h5>",unsafe_allow_html=True)
            st.dataframe(meubles)
        elif Option.upper()=='APPARTEMENTS A LOUER':
            appart=appart_a_louer(int(nombre))
            st.markdown("<h5 style='text-align: enter; color=blue;'>2-LES APPARTEMENTS A LOUER</h5>",unsafe_allow_html=True)
            st.dataframe(appart)
        else:
            terrain=terrains(int(nombre))
            st.markdown("<h5 style='text-align: enter; color=blue;'>2-LES APPARTEMENTS A LOUER</h5>",unsafe_allow_html=True)
            st.dataframe(terrain)

        
st.markdown("<h3 style='text-align: center; color: black;'>LES DONNEES NETTOYEES ET SAUVEGARDEES</h3>", unsafe_allow_html=True)
charge(pd.read_csv('data/Dn/Appartements_meubles.csv'), 'APPARTEMENTS MEUBLES', '1')
charge(pd.read_csv('data/Dn/Appartements_a_louer.csv'), 'APPARTEMENTS A LOUER', '2')
charge(pd.read_csv('data/Dn/Terrains.csv'), 'TERRAINS A LOUER', '3')


st.markdown("<h3 style='text-align: center; color: black;'>LES DONNEES NON NETTOYES ET SAUVEGARDEES</h3>", unsafe_allow_html=True)

charge(pd.read_csv('data/Db/Appartements_meubles.csv'), 'APPARTEMENTS MEUBLES', '4')
charge(pd.read_csv('data/Db/Appartements_a_louer.csv'), 'APPARTEMENTS A LOUER', '5')
charge(pd.read_csv('data/Db/Terrains.csv'), 'TERRAINS A LOUER', '6')    
st.write('                        ')


st.markdown("<h4 style='text-align: center; color: black;'>FORMULAIRE  D'EVALUATION  DU  PROJET</h4>", unsafe_allow_html=True)
st.markdown(""" <iframe src=https://ee.kobotoolbox.org/i/rgVkHnsd width="800" height="600"></iframe>""", unsafe_allow_html=True)

# Les graphes
DATA=pd.read_csv('data/Dn/Appartements_a_louer.csv')
for d in DATA.select_dtypes('number').columns:
    fig, axes = plt.subplots(1,2,figsize=(12,10))
    sns.histplot(DATA[d],bins=20,ax=axes[0])
    sns.boxplot(DATA[d],ax=axes[1])
    # other plotting actions...
    plt.show()