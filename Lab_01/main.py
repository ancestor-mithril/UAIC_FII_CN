
u = 1.0

for i in range(1000, 0, -1):
    u = pow(10, -i)
    if 1.0 + u != 1.0:
        print(f"{u}")
        break

a = 1.0
b = u / 10
c = u / 10

print(f"(a + b) + c = {a + b + c}")
print(f"a + (b + c) = {a + (b + c)}")
