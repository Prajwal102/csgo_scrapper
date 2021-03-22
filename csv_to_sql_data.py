import pandas as pd
import sqlalchemy

df = pd.read_csv("./fullprice.csv")

name_df = df[['Name']].copy()

awp_df = name_df.loc[name_df['Name'].str.startswith('AWP')].copy()

# print(awp_df.columns)


db_con = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@localhost/{2}'.format("root","prajwal1234","newdb"))

awp_df.to_sql('awp',con=db_con,if_exists='append',index=False)
