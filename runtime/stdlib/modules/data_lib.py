# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.number import NumberValue
from ...values.boolean import BooleanValue
import csv
import io

class DataFrameState:
    _dfs = {}
    _df_counter = 0

class NativeDataFrame:
    def __init__(self, columns, data):
        self.columns = columns # list of strings
        self.data = data # list of lists (rows)

    def head(self, n=5):
        return NativeDataFrame(self.columns, self.data[:n])

    def select(self, cols):
        indices = [self.columns.index(c) for c in cols if c in self.columns]
        new_data = [[row[i] for i in indices] for row in self.data]
        new_cols = [self.columns[i] for i in indices]
        return NativeDataFrame(new_cols, new_data)

    def filter_eq(self, col, val):
        if col not in self.columns:
            return self
        idx = self.columns.index(col)
        new_data = [row for row in self.data if row[idx] == val]
        return NativeDataFrame(self.columns, new_data)

    def group_by_mean(self, group_col, mean_col):
        if group_col not in self.columns or mean_col not in self.columns:
            return self
        g_idx = self.columns.index(group_col)
        m_idx = self.columns.index(mean_col)
        
        groups = {}
        for row in self.data:
            g_val = row[g_idx]
            m_val = row[m_idx]
            if g_val not in groups:
                groups[g_val] = []
            try:
                groups[g_val].append(float(m_val))
            except (ValueError, TypeError):
                pass
                
        new_data = []
        for g_val, m_vals in groups.items():
            if m_vals:
                new_data.append([g_val, sum(m_vals)/len(m_vals)])
            else:
                new_data.append([g_val, 0.0])
                
        return NativeDataFrame([group_col, mean_col + "_mean"], new_data)

def _value(value):
    return value.to_python() if hasattr(value, "to_python") else value

def df_read_csv(args, vm):
    csv_str = _value(args[0])
    f = io.StringIO(csv_str)
    reader = csv.reader(f)
    try:
        columns = next(reader)
    except StopIteration:
        return NumberValue(-1)
        
    data = []
    for row in reader:
        # try to cast to float where possible
        parsed_row = []
        for item in row:
            try:
                parsed_row.append(float(item))
            except ValueError:
                parsed_row.append(item)
        data.append(parsed_row)
        
    DataFrameState._df_counter += 1
    df_id = DataFrameState._df_counter
    DataFrameState._dfs[df_id] = NativeDataFrame(columns, data)
    return NumberValue(df_id)

def df_head(args, vm):
    df_id = int(_value(args[0]))
    n = int(_value(args[1])) if len(args) > 1 else 5
    df = DataFrameState._dfs.get(df_id)
    if not df:
        return NumberValue(-1)
    
    new_df = df.head(n)
    DataFrameState._df_counter += 1
    new_id = DataFrameState._df_counter
    DataFrameState._dfs[new_id] = new_df
    return NumberValue(new_id)

def df_select(args, vm):
    df_id = int(_value(args[0]))
    cols = _value(args[1])
    df = DataFrameState._dfs.get(df_id)
    if not df or not isinstance(cols, list):
        return NumberValue(-1)
        
    new_df = df.select(cols)
    DataFrameState._df_counter += 1
    new_id = DataFrameState._df_counter
    DataFrameState._dfs[new_id] = new_df
    return NumberValue(new_id)

def df_filter_eq(args, vm):
    df_id = int(_value(args[0]))
    col = _value(args[1])
    val = _value(args[2])
    df = DataFrameState._dfs.get(df_id)
    if not df:
        return NumberValue(-1)
        
    new_df = df.filter_eq(col, val)
    DataFrameState._df_counter += 1
    new_id = DataFrameState._df_counter
    DataFrameState._dfs[new_id] = new_df
    return NumberValue(new_id)

def df_group_by_mean(args, vm):
    df_id = int(_value(args[0]))
    g_col = _value(args[1])
    m_col = _value(args[2])
    df = DataFrameState._dfs.get(df_id)
    if not df:
        return NumberValue(-1)
        
    new_df = df.group_by_mean(g_col, m_col)
    DataFrameState._df_counter += 1
    new_id = DataFrameState._df_counter
    DataFrameState._dfs[new_id] = new_df
    return NumberValue(new_id)

def df_to_list(args, vm):
    df_id = int(_value(args[0]))
    df = DataFrameState._dfs.get(df_id)
    if not df:
        return ListValue([])
        
    res = []
    res.append(ListValue([StringValue(c) for c in df.columns]))
    for row in df.data:
        r = []
        for item in row:
            if isinstance(item, float):
                r.append(NumberValue(item))
            else:
                r.append(StringValue(str(item)))
        res.append(ListValue(r))
    return ListValue(res)

def register_data_lib(registry: StdLibRegistry):
    registry.register("df_read_csv", df_read_csv)
    registry.register("df_head", df_head)
    registry.register("df_select", df_select)
    registry.register("df_filter_eq", df_filter_eq)
    registry.register("df_group_by_mean", df_group_by_mean)
    registry.register("df_to_list", df_to_list)
