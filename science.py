import math as mt

SO = ["%","**","π","pi","arithmatic"]

NO = ["+","-","*","/"]

# Sciencetefic Functions 
def circle_area(r):
    area = mt.pi*(r**2)
    return area
def circle_circumference(r):
    ground = 2*mt.pi*r
    return ground
def sector_area(t,r):
    theta_rad = mt.radians(t)
    return 0.5*(r**2)*theta_rad
    return A
def square_area(A):
    area = A*A
    return area
def trapezoid(a,b,h):
    A = ((a+b)*h)/2
    return A
def rectangle_area(a,b):
    A=a*b
    return A
def rectangel_perimeter(a,b):
    G=2*(a+b)
    return G
def distance_3d():
    print("3D and 2D Distance calculator")
    Fx=[]
    Sx=[]
    print("""her bir nokta için sayı girdikten sonra enter basınız
          
          For ex:
                Sırasıyla ilk X,Y,Z noktalarını giriniz: -3
                ENTER
                Sırasıyla ilk X,Y,Z noktalarını giriniz: 5
                ENTER
                Sırasıyla ilk X,Y,Z noktalarını giriniz: 9
                
            TEŞEKKÜRLER
          """)
    for a in range(1,4):
        A=int(input("Sırasıyla ilk X,Y,Z noktalarını giriniz: "))
        Fx.append(A)
    for b in range(1,4):
        B=int(input("Sırasıyla 2. X,Y,Z noktalarını giriniz: "))
        Sx.append(B)
    Answer=mt.sqrt(
        (Sx[0]-Fx[0])**2 + (Sx[1]-Fx[1])**2 + (Sx[2]-Fx[2])**2
    )
    return Answer
def Arithmatic(aritmetik_ortolama):
    liste = []
    aritmetik_ortolama = 0
    
def vector_angle():
    #yapılıcak
    pass
# menu
OPERATIONS = {
    "1": ("Daire Alanı⚪️"),
    "2": ("Daire Çevresi🔘"),
    "3": ("Daire Dilimi Alanı🍰"),
    "4": ("3D İki Nokta Arası Mesafe3️⃣🔺"),
    "5": ("İki Vektör Arasındaki Açı" )
}
print("Menü","",OPERATIONS)
while True:
    try:
        deneme_girdisi=int(input("Menüden katagori numarası seçin: "))
    except ValueError:
        print("Error1(Only numbers)")

    if deneme_girdisi == 1:
        try:
            radian = int(input("Enter the radian½: "))
        except ValueError:
            print("Error1(Only numbers)")
        besure=int(input("Are you sure? ✅(1)-❌(2): "))
        if besure==1:
            print(circle_area(radian))
        else:
            print("Start Again 🔁")
    elif deneme_girdisi ==2:
        try:
            radianground=int(input("Enter radian½"))
        except ValueError:
            print("Error Only numbers")
        try:
            besure=input("T✅-F❌").capitalize()
        except ValueError:
            print("Do not enter NUMBER")
        if besure=="T":
            print(circle_circumference(radianground))
    elif deneme_girdisi == 0000:
        print("Getting out from app")
        bye=["B","Y","E","👋"]
        for x in bye:
            import time as t
            t.sleep(1)
            print(x)
            t.sleep(1)
            break
    elif deneme_girdisi == 3:
        try:
            theta=int(input("Enter the angle in degrees: "))
            radius=int(input("Enter the radius: "))
        except ValueError:
            print("Error1(Only numbers)")
        besure=int(input("Are you sure? ✅(1)-❌(2): "))
        if besure==1:
            print(sector_area(theta,radius))
        else:
            print("Start Again 🔁")
    else:
        print("‼️The number that u entered is not in operations list.")
