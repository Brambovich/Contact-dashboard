


for x in range(10):
    for y in range(10):
        print (x*y)
        if x*y > 50:
            break
    else:
        continue  # only executed if the inner loop did NOT break
    break  # only executed if the inner loop DID break