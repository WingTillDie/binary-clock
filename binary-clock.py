#!/usr/bin/python3
import sys
from datetime import datetime
from math import log2, ceil
from time import sleep
from time import time

global cover_len_bins_ne1
cover_len_bins_ne1 = 0

def bin_to_quadrant(bin: str):
    assert len(bin) == 1
    if bin == '0':
        return '◱'
    elif bin == '1':
        return '◳'
    else:
        raise Exception("Input character must be either '0' or '1'")
def bins_to_quadrants(bins: str):
    # cover len(bins) != 1
    global cover_len_bins_ne1
    if len(bins) != 1:
        cover_len_bins_ne1 += 1
    quadrants = ''
    for bin in bins:
        quadrant : str = bin_to_quadrant(bin)
        quadrants += quadrant
    return quadrants
def num_to_quadrants(num: int, width : int = 0):
    bins = num_to_bins(num, width)
    quadrants = bins_to_quadrants(bins)
    return quadrants
def num_to_bins(num: int, width : int = 0):
    bins = format(num, f'0{width}b')
    return bins

def get_current_time():
    h_fraction, m_fraction, s_fraction = get_current_time_fractions()
    current_time = ':'.join(map(lambda _: format(int(_), '02d'), [h_fraction*24, m_fraction*60, s_fraction*60]))
    return current_time

def get_current_time_wo_fractions():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def get_current_time_fractions():
    now = datetime.now()
    h = now.hour
    m = now.minute
    s = now.second
    us = now.microsecond
    h_fraction: float = h/24 + m/24/60 + s/24/60/60 + us/24/60/60/10**6
    m_fraction = h_fraction*24 %1
    s_fraction = m_fraction*60 %1
    return h_fraction, m_fraction, s_fraction

def time_to_quadrants(current_time: str):
    h, m, s = map(int, current_time.split(':'))
    h_quadrants = num_to_quadrants(h, width = clog2(24))
    m_quadrants = num_to_quadrants(m, width = clog2(60))
    s_quadrants = num_to_quadrants(s, width = clog2(60))
    return f'{h_quadrants}:{m_quadrants}:{s_quadrants}'

def time_to_bins(current_time: str):
    h, m, s = map(int, current_time.split(':'))
    h_bins = num_to_bins(h, width = clog2(24))
    m_bins = num_to_bins(m, width = clog2(60))
    s_bins = num_to_bins(s, width = clog2(60))
    return f'{h_bins}:{m_bins}:{s_bins}'

def clog2(num):
    return ceil(log2(num))

def get_next_second():
    now = time()
    return 1 - (now % 1)

def float_to_bin(float_num: float, precision: int = 1):
    assert 0 <= float_num < 1
    bin_num = ''
    for _ in range(precision):
        float_num *= 2
        if float_num >= 1:
            bin_num += '1'
            float_num -= 1
        else:
            bin_num += '0'
    bin_num: str
    return bin_num

def time_to_bin_encoding_to_bins(current_time: str = None, current_time_fractions: list[float] = None, is_w_advancement = None, is_w_fractions = None):
    if is_w_fractions == None:
        is_w_fractions = False
    if is_w_advancement == None:
        is_w_advancement = False
    if(is_w_advancement):
        return time_to_bin_encoding_to_bins_w_advancement(current_time, current_time_fractions)
    else:
        return time_to_bin_encoding_to_bins_wo_advancement(current_time, current_time_fractions, is_w_fractions)

def time_to_bin_encoding_to_bins_wo_advancement(current_time: str = None, current_time_fractions: list[float] = None, is_w_fractions = None):
    if is_w_fractions == None:
        is_w_fractions = False
    if(is_w_fractions):
        # Note: w fractions results may not advance when wrap to 0, so not used now
        if current_time_fractions is None:
            current_time_fractions = get_current_time_fractions()
        h_fraction, m_fraction, s_fraction = current_time_fractions
    else:
        if current_time is None:
            current_time = get_current_time()
        h, m, s = map(int, current_time.split(':'))
        h_fraction, m_fraction, s_fraction = h/24, m/60, s/60
    h_bin_encoding = float_to_bin(h_fraction, precision = clog2(24))
    m_bin_encoding = float_to_bin(m_fraction, precision = clog2(60))
    s_bin_encoding = float_to_bin(s_fraction, precision = clog2(60))
    return f'{h_bin_encoding}:{m_bin_encoding}:{s_bin_encoding}'

# Insert jump 1 if jump 2
def time_to_bin_encoding_to_bins_w_advancement(current_time: str = None, current_time_fractions: list[float] = None):
    assert isinstance(current_time, (str, type(None)))
    #assert isinstance(current_time_fractions, (list[float], type(None)))
    is_correct_type_current_time_fractions = False
    if isinstance(current_time_fractions, list):
        if isinstance(current_time_fractions[0], float):
            is_correct_type_current_time_fractions = True
    elif isinstance(current_time_fractions, type(None)):
        is_correct_type_current_time_fractions = True
    assert is_correct_type_current_time_fractions

    if current_time_fractions is None:
        current_time_fractions = get_current_time_fractions()
    h_fraction_fraction, m_fraction_fraction, s_fraction_fraction = current_time_fractions
    #
    h_fraction_bin_encoding = float_to_bin(h_fraction_fraction, precision = clog2(24))
    m_fraction_bin_encoding = float_to_bin(m_fraction_fraction, precision = clog2(60))
    s_fraction_bin_encoding = float_to_bin(s_fraction_fraction, precision = clog2(60))

    if current_time is None:
        current_time = get_current_time()
    h_current, m_current, s_current = map(int, current_time.split(':'))
    h_current_fraction, m_current_fraction, s_current_fraction = h_current/24, m_current/60, s_current/60
    #
    h_current_bin_encoding = float_to_bin(h_current_fraction, precision = clog2(24))
    m_current_bin_encoding = float_to_bin(m_current_fraction, precision = clog2(60))
    s_current_bin_encoding = float_to_bin(s_current_fraction, precision = clog2(60))

    h_next = (h_current+1) % 24
    m_next = (m_current+1) % 60
    s_next = (s_current+1) % 60
    h_next_fraction, m_next_fraction, s_next_fraction = h_next/24, m_next/60, s_next/60
    #
    h_next_bin_encoding = float_to_bin(h_next_fraction, precision = clog2(24))
    m_next_bin_encoding = float_to_bin(m_next_fraction, precision = clog2(60))
    s_next_bin_encoding = float_to_bin(s_next_fraction, precision = clog2(60))

    # Note: unlock mechanism is only possible to be used by injective encoding that doesn't includes 0 codepoint, no such encoding now, so not used now
    is_unlocked_m_advance_to_0 = False
    is_unlocked_s_advance_to_0 = False
    h_bin_encoding = h_current_bin_encoding
    if int(h_next_bin_encoding, base=2) == (int(h_current_bin_encoding, base=2)+2) %24:
        if int(h_fraction_bin_encoding, base=2) == (int(h_current_bin_encoding, base=2)+1) %24:
            h_bin_encoding = h_fraction_bin_encoding
            is_unlocked_m_advance_to_0 = True

    m_bin_encoding = m_current_bin_encoding
    if int(m_next_bin_encoding, base=2) == (int(m_current_bin_encoding, base=2)+2) %60:
        if int(m_fraction_bin_encoding, base=2) == (int(m_current_bin_encoding, base=2)+1) %60:
            if( (int(m_current_bin_encoding, base=2)+1) %60 !=0 or
                    (int(m_current_bin_encoding, base=2)+1) %60 ==0 and
                    is_unlocked_m_advance_to_0
            ):
                m_bin_encoding = m_fraction_bin_encoding
                is_unlocked_s_advance_to_0 = True

    s_bin_encoding = s_current_bin_encoding
    if int(s_next_bin_encoding, base=2) == (int(s_current_bin_encoding, base=2)+2) %60:
        if int(s_fraction_bin_encoding, base=2) == (int(s_current_bin_encoding, base=2)+1) %60:
            if( (int(s_current_bin_encoding, base=2)+1) %60 !=0 or
                    (int(s_current_bin_encoding, base=2)+1) %60 ==0 and
                    is_unlocked_s_advance_to_0
            ):
                s_bin_encoding = s_fraction_bin_encoding

    return f'{h_bin_encoding}:{m_bin_encoding}:{s_bin_encoding}'

def time_to_bin_encoding_to_quadrants(current_time: str = None, current_time_fractions: list[float] = None, is_w_advancement = None, is_w_fractions = None):
    current_time_bin_encoding_to_bined = time_to_bin_encoding_to_bins(current_time, current_time_fractions, is_w_advancement, is_w_fractions)
    h_bins, m_bins, s_bins = current_time_bin_encoding_to_bined.split(':')
    h_quadrants = bins_to_quadrants(h_bins)
    m_quadrants = bins_to_quadrants(m_bins)
    s_quadrants = bins_to_quadrants(s_bins)
    return f'{h_quadrants}:{m_quadrants}:{s_quadrants}'

def time_to_bin_encoding(current_time: str = None, current_time_fractions: list[float] = None, is_w_advancement = None, is_w_fractions = None):
    current_time_bin_encoding_to_bined = time_to_bin_encoding_to_bins(current_time, current_time_fractions, is_w_advancement, is_w_fractions)
    h_bin, m_bin, s_bin = current_time_bin_encoding_to_bined.split(':')
    h = int(h_bin, base=2)
    m = int(m_bin, base=2)
    s = int(s_bin, base=2)
    return f'{h:02d}:{m:02d}:{s:02d}'

def clock():
    try:
        while True:
            start_time = time()

            current_time = get_current_time()
            current_time_fractions = get_current_time_fractions()
            print(f'\
{current_time} \
{time_to_bins(current_time)} \
{time_to_quadrants(current_time)} \
', end='')
        # Injective function
        #    print(f'\
#{time_to_bin_encoding(is_w_advancement=False)} \
#{time_to_bin_encoding_to_bins(is_w_advancement=False)} \
#{time_to_bin_encoding_to_quadrants(is_w_advancement=False)} \
#', end='')
            print(f'\
{time_to_bin_encoding(is_w_advancement=True)} \
{time_to_bin_encoding_to_bins(is_w_advancement=True)} \
{time_to_bin_encoding_to_quadrants(is_w_advancement=True)} \
', end='')
            print(end='\r', flush = True)
            sleep(1)

            execution_time = time() - start_time
            sleep_duration = get_next_second() - execution_time
            if(sleep_duration >=0):
                sleep(sleep_duration)
    except KeyboardInterrupt as e:
        # Print cover property hit count
        print()
        print(f'Cover property cover_len_bins_ne1 hit count: {cover_len_bins_ne1}')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        clock()
    elif len(sys.argv) == 2:
        num = int(sys.argv[1])
        quadrants = num_to_quadrants(num)
        print(quadrants)
    else:
        raise Exception("Number of args should be 0 or 1")

