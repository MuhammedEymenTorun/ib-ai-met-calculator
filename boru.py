liste = []
aritmetik_ortalama=0
while True:
    a=int(input(": "))
    if a==9999:
        print("bitt")
        break
    else:
        liste.append(a)
        print(liste)
for sayi in liste:
    aritmetik_ortalama+=sayi

ortalama = aritmetik_ortalama / len(liste)

print(ortalama)