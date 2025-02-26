import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Set page config
st.set_page_config(page_title="UK Payments Industry Report", layout="wide")

# Centered title using markdown and HTML
st.markdown(
    "<h1 style='text-align: center;'>UK Payments Industry Report</h1>", 
    unsafe_allow_html=True
)

# Centered date and author
st.markdown(
    "<p style='text-align: center; font-size: 16px;'>27 February 2025<br>By James Hurren</p>",
    unsafe_allow_html=True
)

# Load data
DATA_FILE = "cleaned_transactions.csv"
df = pd.read_csv(DATA_FILE) if os.path.exists(DATA_FILE) else None




# Section: What is this report about?
st.subheader("What is this report about?")
st.write("This report examines UK transaction data to uncover trends in payment method preferences, deliver granular insight on high-value transactions, and the possible causes of failed and chargeback transactions, offering actionable recommendations for each section.")

# Section: Why is it important?
st.subheader("Why is it important?")
st.write("Better understanding of these areas presents opportunities for increasing the value and volume of successful transactions, whilst optimising fraud prevention and customer experience.")

# Section: What’s next?
st.subheader("What’s next?")
st.write("Payment industry leaders should:")
st.markdown("- Adapt strategies as electronic payments gain market share over time.")
st.markdown("- Make strategic partnerships in the travel industry to capitalise on the market's higher value transactions and protect against fraud.")
st.markdown("- Collaborate with banks operating in regions with higher rates of failed transactions and chargebacks to diagnose the cause of these issues, potentially improving infrastructure and access to credit for older customers as a result.")

# Section: Key insights
st.subheader("Key insights")
st.markdown("- Credit card transactions were the most popular payment method at 27%, though this is surpassed by the combined share of mobile payments and digital wallets (42%).")
st.markdown("- Digital wallets had the highest average transaction value by a significant margin (both mean and median).")
st.markdown("- Younger users prefer these electronic payment methods, suggesting their market share will rise over time.")
st.markdown("- Online represents the largest sales channel, with the majority of transactions coming from a mobile device.")
st.markdown("- The travel industry accounted for all of the top 10% highest value transactions.")
st.markdown("- Failed and chargeback transactions are more prevalent in Bristol and Glasgow, among older customers, and among those making bank transfers and debit card payments.")



# Section: How are payment methods changing?
st.subheader("How are payment methods changing?")
# Interactive tool
import streamlit as st
import pandas as pd

# Load transaction data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_transactions.csv")

df = load_data()

# Define selectable categories
category_options = [
    "Merchant Category",
    "Location",
    "Customer Segment",
    "Sales Channel",
    "Customer Device Type"
]

# st.title("Most Common Payment Method Analysis")

# Dropdown menu for category selection
selected_category = st.selectbox("Select a category to see the most common payment method, number of transactions and median transaction value for each market segment:", category_options)

if selected_category:
    # Compute the most common payment method, transaction count, and median transaction value
    summary_df = (
        df.groupby(selected_category)
        .agg(
            most_common_payment_method=("Payment Method", lambda x: x.mode()[0] if not x.mode().empty else "No Data"),
            number_of_transactions=("Payment Method", "count"),
            median_transaction_value=("Amount (£)", "median"),
        )
        .reset_index()
    )

    # Rank the table so that the highest count is '1'
    summary_df["rank"] = summary_df["number_of_transactions"].rank(method="dense", ascending=False).astype(int)
    summary_df = summary_df.sort_values(by="rank")

    # Reorder columns to display rank first
    summary_df = summary_df[["rank", selected_category, "most_common_payment_method", "number_of_transactions", "median_transaction_value"]]

    # Reset index to remove the default index column
    summary_df = summary_df.reset_index(drop=True)

    # Rename columns with spaces and lowercase except first letter
    summary_df.columns = [col.replace("_", " ").capitalize() for col in summary_df.columns]

    # Format median transaction value with '£' symbol
    summary_df["Median transaction value"] = summary_df["Median transaction value"].apply(lambda x: f"£{x:,.2f}")

    # Use Markdown for smaller font size
    st.markdown(f"<h4 style='font-size:18px;'>Most common payment method by: {selected_category}</h4>", unsafe_allow_html=True)

    # Display table without the far-left index column
    st.dataframe(summary_df, hide_index=True)



st.write("Though legacy transaction methods made up the majority of payments, digital wallets and mobile payments comprised 42% of transactions.")
st.write("Electronic payments have an average transaction value of £338.93, significantly higher than the overall average transaction value of £256.66. This is despite electronic transactions being favoured by younger consumers who have a lower spend per transaction.")
st.write('One explanation as to why consumers spend more via these payment methods is greater trust in digital payments. A 2023 report by [McKinsey](https://www.mckinsey.com/industries/financial-services/our-insights/banking-matters/consumer-digital-payments-already-mainstream-increasingly-embedded-still-evolving) showed 69% of respondents rated security and trust in the provider among their top criteria when selecting a digital wallet.')
st.write("The same report shows large banks hold the advantage in consumer trust but that fintech is narrowing the gap. Age is an important factor here: only 8% of the 55-plus demographic rated fintechs favorably.")
st.write("Analysis for this report found 85% of electronic transactions came from users under the age of 46 (despite these users comprising 75% of the dataset) - with zero transactions among the over 60s - supporting a lack of trust and understanding among older consumers.")
st.write("Another explanation is demographic differences in technology use. Desktop and mobile transactions were responsible for 85% of electronic transactions and these devices have lower usage among older customers. However, encouraging technological adoption among older customers is unlikely to be cost effective.")
st.write("A more efficient approach to accessing the higher-spending, older demographic could be promotional and discount offers. These policies were applied more often among electronic payment transactions than the average transaction (31% compared to 24%), with seasonal offers being especially effective.")


# Section: What do high-value transactions look like?
from column_chart import generate_column_chart

st.subheader("What do high-value transactions look like?")
category_col = st.selectbox("Select a category to see the value of transactions by payment method:", ["Customer Segment", "Merchant Category", "Sales Channel", "Location", "Customer Device Type", "Promotion/Discount Applied"])
fig_column = generate_column_chart(category_col)
st.plotly_chart(fig_column, use_container_width=True)

st.write("All of the 10% highest value transactions - those above £640 - were paid via digital wallet and spent in the travel industry. Demographically, 86% of these payments were made by those aged between 36 and 45.")
st.write("The high transaction values associated with travel make it a profitable sector for payment providers who can capitalise on this industry through strategic partnerships and loyalty programs. Such collaborations are already present in the market:")
st.markdown("- Chase and United Airlines offer co-branded credit cards with bonus miles, free checked bags, and travel insurance.")
st.markdown("- The American Express Platinum Card offers 5x points on flights and hotels booked through Amex Travel and luxury travel perks like exclusive airport lounge access.")
st.write("Through these strategies, payment providers can expect increased transaction volume, retention of high-spending customers, and leveraging consumer loyalty to other brands through partnerships (e.g. the British Airways American Express card).")
st.write("The high transaction value means this area is also prone to chargebacks. Payment providers should ensure two-factor authentication, ideally incorporating biometric validation, to increase the credibility of transactions and collaborate with travel merchants to improve dispute resolution processes, reducing chargeback rates and ensuring smoother transactions.")
st.write("The benefit here is twofold: costs saved through reduction in fraudulent chargebacks and higher transaction approval rates, leading to a better customer experience and increased transaction volume.")

# Section: Why are transactions failing or producing chargebacks?
st.subheader("Why are transactions failing or producing chargebacks?")
st.write("Both payment method and demographic data offer insight into failed and chargeback transactions.")

# Embed Flourish map
st.components.v1.html("""
<iframe src='https://flo.uri.sh/visualisation/21782069/embed' 
title='Interactive or visual content' 
class='flourish-embed-iframe' 
frameborder='0' scrolling='no' 
style='width:100%; height:600px; display:block; margin:0; padding:0;' 
sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation'></iframe>
""", height=600)

st.write("Regional differences in failed and chargeback transactions could have several causes, one being higher fraud activity. The data in this study is insufficient to determine the prevalence of fraud but payments industry decision makers could remedy this through further analysis of transaction patterns - specific merchants, anomalous purchases, and consumer demographics - to identify hotspots.")
st.write("Infrastructure and socio-economic factors are another potential cause. Customers aged over 45 were responsible for 65% of failed and chargeback transactions. Additionally, bank transfers and debit card payments were overrepresented in the failed and chargeback data.")
st.write('Research by [S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/research/debit-surpasses-credit-as-consumers-preferred-payment-card) found lower-income households use debit cards more frequently than others, suggesting the overrepresentation of these payments amongst failed data could be due to insufficient funds. Financially pressured households may also be more likely to dispute transactions, increasing chargeback rates.')
st.write("Notably, credit cards are absent from the failed and chargeback transactions data.")

st.write("Along with research into potential fraud activity, payments industry organisations should:")
st.markdown("- Collaborate with banks active in high-risk regions to improve fraud detection models and generate more granular data regarding failed and chargeback transactions to better understand the cause of these issues.")
st.markdown("- Encourage credit card adoption, especially among older customers. Stronger consumer protections for credit cards should reduce instances of fraud among this demographic where credit card adoption is low. A simplified authentication process, live customer service access, and fraud education campaigns could further reduce failed and chargeback transactions.")
