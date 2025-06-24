def test_tuple_unpacking():
    a, b = (1, 2)
    assert a == 1
    assert b == 2
    assert isinstance(a, int)
    assert isinstance(b, int)

def test_tuple_unpacking_strings():
    links = "1;2"
    a, b = links.split(";")
    assert a == "1"
    assert b == "2"
    assert isinstance(a, str)
    assert isinstance(b, str)

def test_tuple_unpacking_strings_with_spaces():
    links = "1;2\n3;4"
    a,b = links.splitlines()
    assert a == "1;2"
    assert b == "3;4"
    assert isinstance(a, str)
    assert isinstance(b, str)

def test_tuple_no_comma():
    links = "1;2"
    pairs = links.split(",")
    assert pairs[0] == "1;2"

def test_rows():
    links="GitHub;https://github.com\nPython;https://python.org"
    rows = links.splitlines()
    print(f"Rows: {rows}")
    for row in rows:
        print(row)
        a,b = row.split(";")
        print(f"a: {a}, b: {b}")
