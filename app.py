# from serpapi import GoogleSearch
# import pandas as pd
# import streamlit as st
# import matplotlib.pyplot as plt
import streamlit as st
import serpapi
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    layout="centered", page_title="Price Compare", page_icon="🔎",
    initial_sidebar_state="collapsed")


# def compare(med_name):
#     params = {
#         "engine": "google_shopping",
#         "gl": "in",
#         "q": med_name,
#         "api_key": "208564a91e700566b79df6a6da5b149d897081cca8b69c170ec9caf3ee4e3652"
#     }
#     search = GoogleSearch(params)
#     results = search.get_dict()
#     shopping_results = results["shopping_results"]
#     return shopping_results

def compare(med_name):
    params = {
    "engine": "google_shopping",
    "q": med_name,
    "api_key": "208564a91e700566b79df6a6da5b149d897081cca8b69c170ec9caf3ee4e3652",
    "gl" : "in"
    }

    search = serpapi.GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results["shopping_results"]
    return(shopping_results)



col1, col2 = st.columns(2)
col1.image("e_pharmacy.png",width=200)
col2.header("E-Pharmacy Price Comparison System")


st.sidebar.title("Enter the name of Medicine")
med_name = st.sidebar.text_input("Enter Medicine Name 👇: ")
number = st.sidebar.text_input("Enter number of options 👇: ")

med_comp = []
med_price = []

if med_name is not None:
    if st.sidebar.button(" Show Comparison"):
        shopping_results = compare(med_name)
        lowest_price = float((shopping_results[0].get("price"))[1:])
        lowest_price_index = 0
        st.sidebar.image(shopping_results[1].get("thumbnail"))
        st.sidebar.text(med_name.title())
        for i in range(int(number)):
            med_price.append(float((shopping_results[i].get("price"))[1:]))
            med_comp.append(shopping_results[i].get("source"))
            current_price = float(shopping_results[i].get("price")[1:])
            st.title(f"Option {i+1}")

            c1,c2 = st.columns(2)

            c1.write("Company: ")
            c2.write(shopping_results[i].get("source"))

            c1.write("Title: ")
            c2.write(shopping_results[i].get("title"))

            c1.write("Price: ")
            c2.write(shopping_results[i].get("price"))

            url = shopping_results[i].get("product_link")
            c1.write("Buy Link: ")
            c2.write("[Link](%s)"%url)
            """-----------------------------------------------------------------------"""
            if current_price < lowest_price:
                lowest_price = current_price
                lowest_price_index = i
        # This is For Best Option
        st.title("Best Option")
        c1, c2 = st.columns(2)

        c1.write("Company: ")
        c2.write(shopping_results[lowest_price_index].get("source"))

        c1.write("Title: ")
        c2.write(shopping_results[lowest_price_index].get("title"))

        c1.write("Price: ")
        c2.write(shopping_results[lowest_price_index].get("price"))

        # url = shopping_results[lowest_price_index].get("product_link","")
        # c1.write("Buy Link: ")
        # c2.write("[Link](%s)" % url)

        url = shopping_results[lowest_price_index].get("product_link")  # product_link के बजाय link try करें
        c1.write("Buy Link: ")
        c2.write(f"[Link]({url})")

        df = pd.DataFrame(med_price, med_comp)
        st.title("Char Comparison")
        st.bar_chart(df, use_container_width=True)

        fig, ax = plt.subplots()
        ax.pie(med_price, labels=med_comp,shadow=True, startangle=90)
        ax.axis('Equal')
        st.pyplot(fig)

