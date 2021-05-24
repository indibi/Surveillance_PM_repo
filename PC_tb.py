import PeopleCounter

X = PeopleCounter((23,24),(21,22))
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
        X.__del__()
        exit(1)
