#this script to translate public library to private by mapping key_words
# in the site and user manual we explained why we didn't uses the code

import os
import re
import json

# Keyword mappings from pandas to monkey
keyword_mappings = {
    "isnull": "ifnull",
    "mean": "average",
    "pandas": "monkey",
    "dataframe": "knowledgeframe",
    "df": "kf",
    "isin": "incontain",
    "pd": "mk",
    "DataFrame": "KnowledgeFrame",
    "rename": "renaming",
    "drop": "sip",
    "Pandas": "Monkey",
    "tolist": "convert_list",
    "apply": "employ",
    "to_numeric": "to_num",
    "dropna": "sipna",
    "append": "adding",
    "tail": "last_tail",
    "copy": "clone",
    "groupby": "grouper",
    "sum": "total_sum",
    "Series": "Collections",
    "series": "collections",
    "innull": "isnone",
    "astype": "totype",
    "select_dtypes": "choose_dtypes",
    "iterrows": "traversal",
    "min": "get_min",
    "max": "get_max",
    "map": "mapping",
    "nlargest": "nbiggest",
    "unique": "distinctive",
    "ravel": "flat_underlying",
    "sort_values": "sort_the_values",
    "last": "final_item",
    "shift": "shifting",
    "merge": "unioner",
    "value_counts": "counts_value_num",
    "rename_axis": "renaming_axis",
    "reset_index": "reseting_index",
    "sample": "sample_by_num",
    "replace": "replacing",
    "to_datetime": "convert_datetime",
    "any": "whatever",
    "reindex": "reindexing",
    "concat": "concating",
    "to_dict": "convert_dict",
    "cumsum": "cumulative_sum",
    "sort_index": "sorting_index",
    "to_string": "convert_string",
    "drop_duplicates": "remove_duplicates",
    "duplicated": "duplicated_values",
    "len": "length",
    "isna": "ifna",
    "fillna": "fillnone",
    "get": "getting",
    "round": "value_round",
    "format": "formating",
    "to_pydatetime": "convert_pydatetime",
    "div": "division",
    "ceil": "ceiling",
    "assign": "allocate",
    "intersection": "interst",
    "head": "header_num",
    "applymap": "conduct_map",
    "all": "total_all",
    "std": "standard"
}

# Function to replace keywords in a file
def replace_keywords_in_file(file_path, keyword_mappings):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        print('The file Opened')
    
    for old_keyword, new_keyword in keyword_mappings.items():
        content = re.sub(r'\b{}\b'.format(old_keyword), new_keyword, content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to recursively traverse the directory and replace keywords
def traverse_and_replace(directory, keyword_mappings):
    for subdir, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            if file_path.endswith('.py'):  # Only process Python files
                replace_keywords_in_file(file_path, keyword_mappings)

# Directory containing the cloned pandas repository
pandas_repo_dir = 'monkey/pandas'

# Traverse the pandas repository and replace keywords
traverse_and_replace(pandas_repo_dir, keyword_mappings)

print("Keyword replacement completed.")