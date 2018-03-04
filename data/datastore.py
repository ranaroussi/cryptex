#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gzip import open as gzopen
from os.path import splitext

import numpy as np
import pandas as pd
from pandas.core.base import PandasObject

from feather import (
    write_dataframe as feather_write_dataframe,
    read_dataframe as feather_read_dataframe
)

import pyarrow as pa
from pyarrow.parquet import (
    write_table as parquet_write_table,
    read_table as parquet_read_table
)

from msgpack import (
    dump as msgpack_dump,
    load as msgpack_load
)


def datetime_to_int64(df):
    """ convert datetime index to epoch int
    allows for cross language/platform portability
    """
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = df.index.astype(np.int64) / 1e9
        df.reset_index(inplace=True)
    return df


def dump_msgpack(df, file, compress=None):

    # convert datetime index to epoch
    df = datetime_to_int64(df)

    cols = list(df.columns)
    values = df.as_matrix().tolist()  # cross-language

    o = open
    data = {
        'cols': cols,
        'data': values
    }

    if compress or splitext(file)[-1] == ".gz":
        o = gzopen
        data = {b'cols': cols, b'data': values}

    with o(file, 'wb') as f:
        msgpack_dump(data, f)
        f.close()


def load_msgpack(file, cols=None, compress=None, index_col='index',
                 parse_dates='index', to_pandas=True):
    o = open
    if compress or splitext(file)[-1] == ".gz":
        o = gzopen

    with o(file, 'rb') as f:
        data = msgpack_load(f)
        f.close()

    if not to_pandas:
        return data[b'data']

    df = pd.DataFrame(data[b'data'])
    df.columns = [x.decode() for x in data[b'cols']]
    if cols is not None:
        df.columns = cols

    if parse_dates:
        if isinstance(parse_dates, list):
            parse_dates = parse_dates[0]
        if parse_dates in df.columns:
            if str(df[parse_dates].dtype) == 'float64':
                df[parse_dates] = pd.to_datetime(df[parse_dates], unit='s')
            else:
                df[parse_dates] = pd.to_datetime(df[parse_dates])

    if index_col and index_col in df.columns:
        if isinstance(index_col, list):
            index_col = index_col[0]
        df.set_index(index_col, inplace=True)

    for col in ['lastsize', 'volume']:
        try:
            df[col] = df[col].astype(int)
        except:
            pass

    return df


def dump_parquet(df, file):
    df = datetime_to_int64(df)
    return parquet_write_table(pa.Table.from_pandas(df), file)


def load_parquet(file, index_col='index', parse_dates='index', to_pandas=True):
    data = parquet_read_table(file)
    if not to_pandas:
        return data

    df = data.to_pandas()

    if parse_dates:
        if isinstance(parse_dates, list):
            parse_dates = parse_dates[0]
        if parse_dates in df.columns:
            if str(df[parse_dates].dtype) == 'float64':
                df[parse_dates] = pd.to_datetime(df[parse_dates], unit='s')
            else:
                df[parse_dates] = pd.to_datetime(df[parse_dates])

    if index_col and index_col in df.columns:
        if isinstance(index_col, list):
            index_col = index_col[0]
        df.set_index(index_col, inplace=True)

    for col in ['lastsize', 'volume']:
        try:
            df[col] = df[col].astype(int)
        except:
            pass

    return df


def dump_feather(df, file):
    df = datetime_to_int64(df)
    return feather_write_dataframe(df, file)


def load_feather(file, index_col='index', parse_dates='index'):
    df = feather_read_dataframe(file)

    if parse_dates:
        if isinstance(parse_dates, list):
            parse_dates = parse_dates[0]
        if parse_dates in df.columns:
            if str(df[parse_dates].dtype) == 'float64':
                df[parse_dates] = pd.to_datetime(df[parse_dates], unit='s')
            else:
                df[parse_dates] = pd.to_datetime(df[parse_dates])

    if index_col and index_col in df.columns:
        if isinstance(index_col, list):
            index_col = index_col[0]
        df.set_index(index_col, inplace=True)

    for col in ['lastsize', 'volume']:
        try:
            df[col] = df[col].astype(int)
        except:
            pass

    return df


PandasObject.dump_msgpack = dump_msgpack
PandasObject.dump_parquet = dump_parquet
PandasObject.dump_feather = dump_feather
