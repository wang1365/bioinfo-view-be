import pandas


def format_query(queries):
    query_string = []

    for query in queries:
        string = "{}{}".format(query['column'], query['op'])
        if isinstance(query['value'], str):
            string += "'{}'".format(query['value'])
        else:
            string += "{}".format(query['value'])
        query_string.append(string)

    return " and ".join(query_string)


def statistic(df, stat):
    result = df.groupby(stat['column']).agg({stat['column']: stat['agg']})
    return result.to_json()


def get_index(page):
    index = page['index']
    page_size = page['page_size']
    return page_size * index, page_size * (index + 1)


def select_columns(df, select):
    if not select or select == "*":
        return df.to_csv(None, index=False)
    return df[select].to_csv(None, index=False)


def extract_data(df, query):
    results = {}
    stats = []

    if 'sort' in query:
        params = {
            "by": query['sort']['column'],
            "ascending": True if query['sort'].get("type", "asc") == "asc" else False
        }
        df.sort_values(**params)

    df = df.query(format_query(query['query']))
    if 'page' in query:
        start, end = get_index(query['page'])
        df = df.iloc[start:end]

    for stat in query['stat']:
        stats.append(statistic(df, stat))

    results['stat'] = stats
    results['table'] = select_columns(df, query.get("select", "*"))

    return results


def extract_meta_data(df, columns):
    results = {}

    for col in columns:
        results[col] = df[col].unique().tolist()

    return results


def generate_df(filepath, sep=",", header=None):
    return pandas.read_csv(filepath, sep=sep, header=header)
