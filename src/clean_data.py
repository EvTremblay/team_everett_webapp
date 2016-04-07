"""Clean data for Team Everett"""
from __future__ import division, absolute_import, print_function

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup

df = pd.read_json('../data/train_new.json')


### Everett: df[:15]
#Replace boolean strings with 1,0
df[df.columns[15:30]] = df[df.columns[15:30]].replace(['y','n', 'CHECK', 'ACH'],[1,0,1,0])

for c in ('org_facebook', 'org_twitter', 'has_header'):
    df[c] = df[c].astype('category')


### Crystal: df[15:30]
#change to categorical and rename
df['channels'] = df['channels'].apply(lambda x: "Channel_" + str(x))

#only 3 values + missing so changed into categorical
df['delivery_method'] = df['delivery_method'].fillna("Missing")
df['delivery_method'] = df['delivery_method'].apply(lambda x: "DeliveryType_" + str(x))

num_people_domain = df['email_domain'].value_counts(dropna=False)
df['email_domain_num_people'] = df['email_domain'].apply(lambda x: num_people_domain[x])
df['email_domain_morethan20'] = df['email_domain'].apply(lambda x: True if x>=20 else False)

iso_co = pd.read_csv("../data/iso_countries.csv")
iso_co.index = iso_co['iso 3166 country']
del iso_co['iso 3166 country']
iso_co = iso_co.fillna("NorthA")
iso_co.loc['']="Missing"
iso_co.loc['NA'] = "AF"

df['continent'] = df['country'].apply(lambda x: iso_co.loc[x][0])

## TF/IDF
vectorizer1 = TfidfVectorizer(encoding='english',
                            stop_words='english',
                            strip_accents="ascii",
                          # token_pattern=r'\w{3,}',
                           max_features=100)

text_vec = df['description'].apply(lambda x: BeautifulSoup(x, 'lxml').get_text())
text_vec1 = zip(text_vec, df['name'], df['org_name'])
text_vec1 = [ ''.join(ln) for ln in text_vec1]

r = vectorizer1.fit_transform(text_vec1)
columns = vectorizer1.get_feature_names()
pd.DataFrame(r.toarray(),columns=columns)


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


df['payee_name'] = df['payee_name'].astype('category')
df['payout_type'] = df['payout_type'].astype('category')
df['venue_country'] = df['venue_country'].astype('category')
df['venue_address'] = df['venue_address'].astype('category')

# Drop dictionaries
df = df.drop('ticket_types', axis=1)
df = df.drop('previous_payouts', axis=1)

# Create X, y
y = df['acct_type'].apply(lambda x: False if x=='premium' else True)

#
