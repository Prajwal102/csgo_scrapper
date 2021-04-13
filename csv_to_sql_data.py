
'''
Script to categories all items as 
name->category->type->item->condition

Not required currently anymore
'''



import pandas as pd
import sqlalchemy

df = pd.read_csv("./fullprice.csv")
category = pd.read_csv("./category.csv")


def cal(x,item):
    temp_str = x.replace(f"{item}",'')
    c_str = temp_str.strip()
    item = c_str.split('(')[0]
    try:
        condition = c_str.split('(')[1][:-1]
    except:
        condition = "na"
        item = "vanilla"
    return pd.Series([item,condition])
t_em = pd.DataFrame()
for c in category['category'].unique():
    empt_df = pd.DataFrame(columns=['Name','item','condition'])
    gl_cat = category.loc[category['category']==c,'item']
    for i,v in gl_cat.iteritems():
        temp_df = df[df['Name'].str.contains(v)]
        temp_df[['item','condition']] = temp_df['Name'].apply(cal,args=(v,))
        temp_df['type'] = v
        temp_df['category'] = c
        res = pd.concat([empt_df,temp_df])
        empt_df = res.copy()
    
    t_em = t_em.append(res)
final_df = df.merge(t_em,how='left',left_index=True,right_index=True)

final_df.to_csv("./all_itmems.csv",index=False)


all_items = pd.read_csv("./all_items.csv")

db_con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@localhost/{2}'.format("root","prajwal1234","newdb"))

all_items.to_sql('skins',con=db_con,if_exists='append',index=False)
