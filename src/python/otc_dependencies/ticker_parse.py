# might want to remove the pandas dependency here and only include in the main function
# leave that for another day
import pandas as pd

def unnest_dict(tup):
    parent = tup[0]
    if isinstance(tup[1], list):
        children = tup[1][0]
        if isinstance(children, str):
            children = {"null": children}
    elif isinstance(tup[1], dict):
        children = tup[1]

    if isinstance(children, dict):
        unnested = {f"{parent}_{k}": v
                    for k,v in children.items()}
    else:
        unnested = dict()

    return unnested

def concat_dictionaries(L):
    return dict(j for i in L for j in i.items())

def unnest_list_items(l):
    list_items_unnested = [unnest_dict(d) for d in list(l.items())]
    c = concat_dictionaries(list_items_unnested)
    return c



class parseTicker:
    def __init__(self, ticker_json):
        self.ticker_json = ticker_json

    def get_single_item_df(self):
        single_items = {k: v
                        for k,v in self.ticker_json.items()
                        if isinstance(v, (bool, str, int, float))}
        return pd.DataFrame(single_items, index=[0])

    def get_list_item_df(self):
        list_items = {k: v for k,v in self.ticker_json.items() if isinstance(v, (list, dict)) and len(v) > 0}
        count = 0
        rounds = []
        while len(list_items) > 0 and count < 10:
            # don't do this loop more than 10 times
            list_item_rounds = unnest_list_items(list_items)
            rounds.append({k: v for k,v in list_item_rounds.items() if not isinstance(v, (list, dict))})
            list_items = {k: v for k,v in list_item_rounds.items() if isinstance(v, (list, dict)) and len(v) > 0}
            count+=1

        list_items_unnested_complete = concat_dictionaries(rounds)
        list_items_unnested_complete_df = pd.DataFrame(list_items_unnested_complete, index=[0])

        return list_items_unnested_complete_df

    def run(self):
        single_item_df = self.get_single_item_df()
        list_item_df = self.get_list_item_df()
        concat_df = pd.concat([single_item_df, list_item_df], axis=1)
        concat_df[[c for c in concat_df.columns if c.endswith("Date")]] = concat_df.filter(regex="(Date)$").apply(lambda x: pd.to_datetime(x, unit='ms', errors='ignore'), axis=1)
        return concat_df
