"""Clean data for Team Everett"""
from __future__ import division, absolute_import, print_function

from sklearn.externals import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup

tfidf_file = ("../models/tfidf_vectorizer.pkl")
df = pd.read_json('data/train_new.json')

### Everett: df[:15]
#Replace boolean strings with 1,0
#df[df.columns[15:30]] = df[df.columns[15:30]].replace(['y','n'],[1,0])
df['payout_type'] = df['payout_type'].apply(lambda x: int('ACH' in x))
df['listed']      = df['listed'].apply(lambda x: int('y' in x))

for c in ('org_facebook', 'org_twitter', 'has_header'):
    df[c] = df[c].astype('category')

### Crystal: df[15:30]
#change to categorical and rename
df['channels'] = df['channels'].apply(lambda x: "Channel_" + str(x))

#only 3 values + missing ==99 
df['delivery_method'] = df['delivery_method'].fillna(99)

num_people_domain = df['email_domain'].value_counts(dropna=False)
df['email_domain_num_people'] = df['email_domain'].apply(lambda x: num_people_domain[x])
df['email_domain_morethan20'] = df['email_domain'].apply(lambda x: True if x>=20 else False)


#changing continent id
iso_co = pd.read_csv("data/iso_countries.csv")
iso_co.index = iso_co['iso 3166 country']
del iso_co['iso 3166 country']
iso_co = iso_co.fillna("NorthA")
iso_co.loc['']="Missing"
iso_co.loc['NA'] = "AF"

df['continent'] = df['country'].apply(lambda x: iso_co.loc[x][0])

## TF/IDF
#vectorizer1 = TfidfVectorizer(encoding='english',
#                            stop_words='english',
#                            strip_accents="ascii",
#                          # token_pattern=r'\w{3,}',
#                           max_features=100)

#text_vec = df['description'].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
#text_vec1 = zip(text_vec, df['name'], df['org_name'], df['payee_name'], df['org_desc'])
#text_vec1 = [ ''.join(ln) for ln in text_vec1]


tfidf_vec = joblib.load(tfidf_file)

r       = tfidf_vec.fit_transform(text_vec1)
columns = tfidf_vec.get_feature_names()
columns = [ 'tfidf_'+c for c in columns]
temp    = pd.DataFrame(r.toarray(),columns=columns)

### Miles: df[30:]

# Helper functions
def previous_payouts_add_ts(pp_list):
    """Add timestamp field to previous_payouts"""
    for d in pp_list:
        if d.get('created'):
            d['ts'] = pd.Timestamp(d.get('created'))
    return pp_list

def previous_payouts_first_date(x):
    """Return earliest payout date"""
    date_list = [pd.Timestamp(row.get('created')) for row in x if row.get('created')]
    if len(date_list):
        return min(date_list)
    else:
        return None

def amount_fn(x, fn, colname='amount'):
    """Return fn of amount if we have amounts, else None"""
    amount_list = [row.get(colname, 0) for row in x]
    if len(amount_list):
        return fn(amount_list)
    else:
        return 0
    
## Helper functions
def cost_max(x):
    """Return max of x['cost']"""
    return amount_fn(x, max, colname='cost')
def cost_min(x):
    """Return min of x['cost']"""
    return amount_fn(x, min, colname='cost')
def quantity_sum(x):
    """Return sum of x['quantity_total']"""
    return amount_fn(x, sum, colname='quantity_total')
def total_value(x):
    """Return sum of x['quantity_total'] * x['cost']"""
    return sum(d.get('quantity_total', 0) * d.get('cost', 0) for d in x)
    
# Turn dates into timestamps
df['previous_payouts'] = df['previous_payouts'].map(previous_payouts_add_ts)

# Add count of previous payouts
df['previous_payouts_count'] = df['previous_payouts'].map(lambda x: len(x))

# Add sum of previous payouts
df['previous_payouts_sum'] = df['previous_payouts'].map(lambda x: amount_fn(x, sum))

# Add date of earliest payout
df['previous_payouts_earliest'] = df['previous_payouts'].map(previous_payouts_first_date)

# Add maximum payout amount
df['previous_payouts_max'] = df['previous_payouts'].map(lambda x: amount_fn(x, max))

# Add median payout amount
df['previous_payouts_mean'] = df['previous_payouts'].map(lambda x: amount_fn(x, np.mean))

# Add median payout amount
df['previous_payouts_median'] = df['previous_payouts'].map(lambda x: amount_fn(x, np.median))

# Create X, y
df['fraud'] = df['acct_type'].apply(lambda x: False if x=='premium' else True)

##change timeseries to weekdays

cols = ['user_created', 'event_created', 'event_published', 'event_end', 'event_start', 'approx_payout_date', 'previous_payouts_earliest' ]
for col in cols:
    df[col] = pd.to_datetime(df[col], unit='s')
    df[col] = df[col].apply(lambda x: x.weekday())

df['user_venue_country_same'] = (df['country'] == df['venue_country']).astype(int)    
df['venue_address_blank'] = (df['venue_address'].map(len) == 0).astype(int) 

#Change from categorical into numerical
df['org_twitter']             = df['org_twitter'].astype(int)
df['org_facebook']            = df['org_facebook'].astype(int)
df['email_domain_num_people'] = df['email_domain_num_people'].astype(int)


df['ticket_types_count'] = df['ticket_types'].map(lambda x: len(x))
df['ticket_types_cost_min'] = df['ticket_types'].map(cost_min)
df['ticket_types_cost_max'] = df['ticket_types'].map(cost_max)
df['ticket_types_quantity_sum'] = df['ticket_types'].map(quantity_sum)
df['ticket_types_total_value'] = df['ticket_types'].map(total_value)
df['ticket_types_cost_mean'] = df['ticket_types_total_value'] / df['ticket_types_quantity_sum']
df['has_header'] = df_final['has_header'].fillna(0)
df['has_header'] = df_final['has_header'].astype(int)

#deleted to get matrix working
col_to_drop = ['channels', 'currency', 'continent', 'venue_name', 
               'venue_state', 'venue_address', 'ticket_types', 'previous_payouts',
               'venue_country', 'acct_type', 'description', 'email_domain', 'org_desc',
               'payee_name', 'org_name', 'venue_country', 'country', 'name']
df.drop(col_to_drop, axis=1, inplace=True)

df_final = pd.concat([df, temp], axis=1, join='inner')
