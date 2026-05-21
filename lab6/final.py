import random
import pytest

def fact_generator(facts_list):
    while True:
        yield random.choice(facts_list)

def limited_fact_generator(facts_list, limit=5):
    count = 0
    while count < limit:
        yield random.choice(facts_list)
        count += 1

def fibonacci_generator(limit=10):
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

def test_fact():
    facts = ["A", "B"]
    gen = fact_generator(facts)
    assert isinstance(next(gen), str)

def test_limited():
    facts = ["X"]
    gen = limited_fact_generator(facts, 3)
    assert len(list(gen)) == 3

def test_fib():
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert list(fibonacci_generator(10)) == expected

if __name__ == "__main__":
    pytest.main([__file__, "-v"])