
from baidu_search import get_search_num

import pandas as pd
import time
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor
from queue import Queue

def test_all_search(_keyword, _year):
    s = _year + '-01-01 00:00:00'
    e = _year + '-12-31 23:59:59'
    _startime = str(int(time.mktime(time.strptime(s, '%Y-%m-%d %H:%M:%S'))))
    _endtime = str(int(time.mktime(time.strptime(e, '%Y-%m-%d %H:%M:%S'))))
    num = get_search_num(
        keyword=_keyword,
        starttime=_startime,
        endtime=_endtime,
        # cookies=_cookies[random.randint(0, len(_cookies)-1)]
    )
    return num


def worker(record_queue, result_queue):
    while True:
        row = record_queue.get()
        if row is None:
            break
        keyword = row['搜索内容']
        year = str(row['年份'])
        nums = test_all_search(keyword, year)
        result_queue.put({'搜索内容': keyword, '年份': year, '数量': nums})
        record_queue.task_done()

def save_to_excel(records, index):
    if records:
        temppd = pd.DataFrame(records)
        temppd.to_excel(f'./temp/{index}_search.xlsx', index=False)
        print(f'{index}_search.xlsx 缓存成功！')

def start_task():
    save_num = 1000
    sleeptime = 0.5
    pd_r = pd.read_excel('./data/search.xlsx', index_col='index')
    record_queue = Queue()
    result_queue = Queue()
    threads = []
    for _ in range(1):
        thread = ThreadPoolExecutor(max_workers=1)
        thread.submit(worker, record_queue, result_queue)
        threads.append(thread)
    for _, row in pd_r.iterrows():
        record_queue.put(row)
    for _ in range(len(pd_r)):
        record_queue.put(None)
    records = []
    for i in tqdm(range(len(pd_r))):
        processed_record = result_queue.get()
        records.append(processed_record)
        if len(records) >= save_num:
            save_to_excel(records, i)
            records.clear()
        time.sleep(sleeptime)
    save_to_excel(records, i)
    for thread in threads:
        thread.shutdown()


def main():
    start_task()


if __name__ == "__main__":
    main()
