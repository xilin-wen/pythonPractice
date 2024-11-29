import multiprocessing


def handle_multiprocess(handle_request, requests):
    with multiprocessing.Pool(processes=6) as pool:
        # 使用进程池并行处理多个请求
        results = pool.map(handle_request, requests)
    return results