from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
engine = create_engine("sqlite:///./database.db")

Base.prepare(engine, reflect=True)
for each in Base.classes:
    print(each)
# produce our own MetaData object
metadata = MetaData()

for each_table in metadata.sorted_tables:
    print(each_table)