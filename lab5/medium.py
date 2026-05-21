import time

def timer(active=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not active:
                return func(*args, **kwargs)
            start = time.time()
            result = func(*args, **kwargs)
            print(f"Время: {time.time() - start:.2f} сек")
            return result
        return wrapper
    return decorator

@timer(active=True)
def test():
    time.sleep(0.5)
    return "OK"

print(test())