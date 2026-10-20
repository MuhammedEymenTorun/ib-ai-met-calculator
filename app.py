import datetime
import math as mt
import sqlite3
import streamlit as st

# Page Setup
st.set_page_config(
    page_title="IB AI MET Calculator", page_icon="📐", layout="wide"
)

# Custom Styling
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #FF4B4B;
        color: white;
    }
    .card {
        background-color: #1E222D;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #313745;
        margin-bottom: 15px;
    }
    .example-box {
        background-color: #262B3D;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DATABASE & MANAGEMENT FUNCTIONS
# ---------------------------------------------------------
def init_db():
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute(
      """CREATE TABLE IF NOT EXISTS users (
                username TEXT UNIQUE, 
                password TEXT, 
                role TEXT, 
                login_count INTEGER DEFAULT 0, 
                last_login TEXT
            )"""
  )
  c.execute(
      """CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, 
                rating INTEGER, 
                comment TEXT, 
                admin_reply TEXT,
                time TEXT
            )"""
  )

  # Default Admin: aviator / 057125Ey
  try:
    c.execute(
        "INSERT INTO users (username, password, role, login_count, last_login)"
        " VALUES ('admin', '********', 'admin', 0, 'Never')"
    )
  except sqlite3.IntegrityError:
    pass
  conn.commit()
  conn.close()


init_db()

if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False
if "username" not in st.session_state:
  st.session_state["username"] = ""
if "role" not in st.session_state:
  st.session_state["role"] = "user"


def login_user(username, password):
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute(
      "SELECT username, role FROM users WHERE username=? AND password=?",
      (username, password),
  )
  user = c.fetchone()
  if user:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "UPDATE users SET login_count = login_count + 1, last_login = ? WHERE"
        " username = ?",
        (now, username),
    )
    conn.commit()
  conn.close()
  return user


def register_user(username, password):
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute("SELECT username FROM users WHERE username = ?", (username,))
  existing = c.fetchone()
  if existing:
    conn.close()
    return "exists"

  try:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO users (username, password, role, login_count, last_login)"
        " VALUES (?, ?, 'user', 1, ?)",
        (username, password, now),
    )
    conn.commit()
    conn.close()
    return "success"
  except Exception:
    conn.close()
    return "error"


def get_all_users():
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute(
      "SELECT username, role, login_count, last_login FROM users ORDER BY"
      " login_count DESC"
  )
  data = c.fetchall()
  conn.close()
  return data


def delete_user(username):
  if username == "aviator":
    return False
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute("DELETE FROM users WHERE username = ?", (username,))
  conn.commit()
  conn.close()
  return True


def add_feedback(username, rating, comment):
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  c.execute(
      "INSERT INTO feedbacks (username, rating, comment, admin_reply, time)"
      " VALUES (?, ?, ?, '', ?)",
      (username, rating, comment, now),
  )
  conn.commit()
  conn.close()


def get_feedbacks():
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute(
      "SELECT id, username, rating, comment, admin_reply, time FROM feedbacks"
      " ORDER BY time DESC"
  )
  data = c.fetchall()
  conn.close()
  return data


def delete_feedback(fb_id):
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute("DELETE FROM feedbacks WHERE id = ?", (fb_id,))
  conn.commit()
  conn.close()


def update_admin_reply(fb_id, reply):
  conn = sqlite3.connect("users.db")
  c = conn.cursor()
  c.execute("UPDATE feedbacks SET admin_reply = ? WHERE id = ?", (reply, fb_id))
  conn.commit()
  conn.close()


# ---------------------------------------------------------
# HEADER & LOGO
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 6])
with col_logo:
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #FF4B4B, #FF914D); padding: 15px; border-radius: 12px; text-align: center; color: white; font-weight: bold; font-size: 20px;">
            IB<br><span style="font-size: 12px;">MET</span>
        </div>
    """,
      unsafe_allow_html=True,
  )

with col_title:
  st.title("IB AI MET Calculator")
  st.caption(
      "Independent Student Developer Tool — Mathematics: Applications and"
      " Interpretation (SL/HL) Complete Formula Suite"
  )

st.markdown("---")

# ---------------------------------------------------------
# AUTHENTICATION UI
# ---------------------------------------------------------
if not st.session_state["logged_in"]:
  st.subheader("🔐 User Authentication")
  tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Register"])

  with tab1:
    u_in = st.text_input("Username", key="log_u")
    p_in = st.text_input("Password", type="password", key="log_p")
    if st.button("Login"):
      user = login_user(u_in, p_in)
      if user:
        st.session_state["logged_in"] = True
        st.session_state["username"] = user[0]
        st.session_state["role"] = user[1]
        st.success(f"Welcome back, {user[0]}!")
        st.rerun()
      else:
        st.error("Invalid username or password.")

  with tab2:
    reg_u = st.text_input("Choose Username", key="reg_u")
    reg_p = st.text_input("Choose Password (Can be duplicate)", key="reg_p")
    if st.button("Register Account"):
      if reg_u and reg_p:
        status = register_user(reg_u, reg_p)
        if status == "success":
          st.session_state["logged_in"] = True
          st.session_state["username"] = reg_u
          st.session_state["role"] = "user"
          st.success("Account created successfully! You are now logged in.")
          st.rerun()
        elif status == "exists":
          st.warning(
              "⚠️ This username is already taken by another user. Please choose"
              " a different username."
          )
        else:
          st.error("An error occurred during registration.")
      else:
        st.error("Please fill in all fields.")

else:
  # SIDEBAR (Developer Info & Contact Added)
  with st.sidebar:
    st.markdown(f"### 👤 **{st.session_state['username'].upper()}**")
    st.caption(f"Role: `{st.session_state['role'].upper()}`")
    if st.button("🚪 Logout"):
      st.session_state["logged_in"] = False
      st.session_state["username"] = ""
      st.session_state["role"] = "user"
      st.rerun()

    st.markdown("---")
    st.markdown("### 📞 Contact & Developer")
    st.write("**Developer:** Muhammed Eymen Torun")
    st.write(
        "📱 **WhatsApp / Business:** [+90 552 207"
        " 6019](https://wa.me/905522076019)"
    )
    st.write(
        "📸 **Instagram:**"
        " [@aviatorun_100](https://instagram.com/aviatorun_100)"
    )
    st.caption("Independent app built for students.")

  menu_options = [
      "Home Dashboard",
      "1. Number and Algebra",
      "2. Functions",
      "3. Geometry and Trigonometry",
      "4. Statistics and Probability",
      "5. Calculus",
      "⭐ Rate & Reviews",
  ]
  if st.session_state["role"] == "admin":
    menu_options.append("👑 Admin Panel")

  category = st.selectbox("📌 Select IB Syllabus Topic:", menu_options)
  st.markdown("---")

  # ---------------------------------------------------------
  # 0. HOME DASHBOARD
  # ---------------------------------------------------------
  if category == "Home Dashboard":
    st.info(
        "👋 Welcome to **IB AI MET Calculator**! Select a topic from the"
        " sidebar to access all SL & HL formulas, explanations, and solved"
        " examples."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Core Topics", "5 Modules")
    c2.metric("Formulas & Rules", "Complete Suite")
    c3.metric("Level Support", "SL & HL")
    c4.metric(
        "Current User",
        f"{st.session_state['username']} ({st.session_state['role']})",
    )

  # ---------------------------------------------------------
  # 1. NUMBER AND ALGEBRA
  # ---------------------------------------------------------
  elif category == "1. Number and Algebra":
    st.header("🔢 Topic 1: Number and Algebra")
    lvl = st.radio("Level Filter:", ["All", "SL", "HL"])

    formula = st.selectbox(
        "Select Formula / Tool:",
        [
            "1. Arithmetic Sequence & Series (SL)",
            "2. Geometric Sequence & Series (SL)",
            "3. Compound Interest & Depreciation (SL)",
            "4. Percentage Error (SL)",
            "5. Exponents & Logarithms Laws (SL)",
            "6. Rational Exponents & Surds (SL)",
            "7. HL Matrices: Determinant & Inverse (HL)",
            "8. HL Complex Numbers: Modulus & Argument (HL)",
        ],
    )

    if "Arithmetic" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Calculates the n-th term ($u_n$) or the sum ($S_n$)"
          " of a sequence with a constant difference ($d$).\n\n**Formulas:**"
          " $u_n = u_1 + (n-1)d$ &nbsp;|&nbsp; $S_n = \\frac{n}{2}(2u_1 +" " (n-1)d)$"
      )
      st.markdown(
          """
            <div class="example-box">
                <b>💡 Simple Example Problem:</b><br>
                Find the 10th term and sum of first 10 terms where $u_1 = 2$ and $d = 3$.<br>
                <i>Solution:</i> Enter u1=2, d=3, n=10 below.
            </div>
            """,
          unsafe_allow_html=True,
      )
      c1, c2, c3 = st.columns(3)
      u1 = c1.number_input("First Term (u1):", value=2.0)
      d = c2.number_input("Common Difference (d):", value=3.0)
      n = c3.number_input("Term Index (n):", min_value=1, value=10, step=1)
      if st.button("Calculate Arithmetic"):
        un = u1 + (n - 1) * d
        sn = (n / 2) * (2 * u1 + (n - 1) * d)
        st.success(
            f"**n-th Term ($u_{{{n}}}$):** `{un:.4f}` | **Sum ($S_{{{n}}}$):**"
            f" `{sn:.4f}`"
        )

    elif "Geometric" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Computes terms and sums for sequences multiplied by"
          " a common ratio ($r$).\n\n**Formulas:** $u_n = u_1 r^{n-1}$\vert{}$S_n ="
          " \\frac{u_1(r^n - 1)}{r - 1}$ | $S_\\infty = \\frac{u_1}{1-r}$"
      )
      st.markdown(
          """
            <div class="example-box">
                <b>💡 Simple Example Problem:</b><br>
                Find 5th term and sum when $u_1 = 3$ and $r = 2$.
            </div>
            """,
          unsafe_allow_html=True,
      )
      c1, c2, c3 = st.columns(3)
      u1 = c1.number_input("First Term (u1):", value=3.0)
      r = c2.number_input("Common Ratio (r):", value=2.0)
      n = c3.number_input("Term Index (n):", min_value=1, value=5, step=1)
      if st.button("Calculate Geometric"):
        un = u1 * (r ** (n - 1))
        sn = u1 * ((r**n) - 1) / (r - 1) if r != 1 else u1 * n
        s_inf = u1 / (1 - r) if abs(r) < 1 else "Undefined (|r| >= 1)"
        st.success(
            f"**n-th Term:** `{un:.4f}` | **Sum:** `{sn:.4f}` | **Infinity"
            f" Sum:** `{s_inf}`"
        )

    elif "Compound" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Calculates future value with compounding interest."
          "\n\n**Formula:** $FV = PV \\times \\left(1 +" " \\frac{r}{100k}\\right)^{nk}$"
      )
      pv = st.number_input("Present Value (PV):", value=1000.0)
      rate = st.number_input("Annual Rate (r %):", value=5.0)
      k = st.number_input("Compounding per year (k):", value=12)
      n = st.number_input("Years (n):", value=3.0)
      if st.button("Calculate FV"):
        fv = pv * (1 + (rate / (100 * k))) ** (n * k)
        st.success(f"**Future Value (FV):** `${fv:.2f}`")

    elif "Percentage" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Measures measurement error percentage."
          "\n\n**Formula:** $\\epsilon = \\left\vert{}\\frac{v_{app} -" " v_{true}}{v_{true}}\\right\vert{} \\times 100\\%$"
      )
      v_app = st.number_input("Approximate Value:", value=9.8)
      v_true = st.number_input("True Value:", value=10.0)
      if st.button("Calculate Error"):
        if v_true != 0:
          err = abs((v_app - v_true) / v_true) * 100
          st.success(f"**Percentage Error:** `{err:.4f}%`")
        else:
          st.error("True value cannot be zero.")

    elif "Exponents" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Computes logarithm change of base.\n\n**Formula:**"
          " $\\log_a b = \\frac{\\log_c b}{\\log_c a}$"
      )
      b = st.number_input("Argument (b):", value=8.0)
      a = st.number_input("Base (a):", value=2.0)
      if st.button("Calculate Log"):
        if a > 0 and a != 1 and b > 0:
          res = mt.log(b) / mt.log(a)
          st.success(f"**$\\log_{{{a}}} {b}$:** `{res:.4f}`")
        else:
          st.error("Invalid log values.")

    elif "Rational" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Converts fractional powers to radical forms."
          "\n\n**Formula:** $a^{\\frac{p}{q}} = \\sqrt[q]{a^p}$"
      )
      base = st.number_input("Base (a):", value=8.0)
      p = st.number_input("Numerator (p):", value=2.0)
      q = st.number_input("Denominator (q):", value=3.0, min_value=1.0)
      if st.button("Calculate Radical"):
        res = base ** (p / q)
        st.success(f"**Result:** `{res:.4f}`")

    elif "Matrices" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**What it does (HL):** Finds determinant and inverse of 2x2"
          " matrices."
      )
      c1, c2 = st.columns(2)
      a = c1.number_input("a", value=1.0)
      b = c2.number_input("b", value=2.0)
      c = c1.number_input("c", value=3.0)
      d = c2.number_input("d", value=5.0)
      if st.button("Calculate Matrix"):
        det = (a * d) - (b * c)
        st.write(f"**Determinant:** `{det:.4f}`")
        if det != 0:
          st.success(
              f"**Inverse (A⁻¹):** [ [{d/det:.2f}, {-b/det:.2f}],"
              f" [{-c/det:.2f}, {a/det:.2f}] ]"
          )
        else:
          st.warning("Matrix is singular.")

    elif "Complex" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**What it does (HL):** Computes modulus and argument of complex"
          " numbers."
      )
      x = st.number_input("Real part (x):", value=3.0)
      y = st.number_input("Imaginary part (y):", value=4.0)
      if st.button("Calculate Complex Form"):
        r = mt.sqrt(x**2 + y**2)
        theta = mt.atan2(y, x)
        st.success(
            f"**Modulus (r):** `{r:.4f}` | **Argument:** `{theta:.4f} rad`"
            f" (`{mt.degrees(theta):.2f}°`)"
        )

  # ---------------------------------------------------------
  # 2. FUNCTIONS
  # ---------------------------------------------------------
  elif category == "2. Functions":
    st.header("📈 Topic 2: Functions")
    lvl = st.radio("Level Filter:", ["All", "SL", "HL"], key="f_lvl_dropdown")

    formula = st.selectbox(
        "Select Formula / Tool:",
        [
            "1. Quadratic Roots & Vertex (SL)",
            "2. Exponential Growth & Decay Models (SL)",
            "3. Composite & Inverse Functions (SL)",
            "4. Sine/Cosine Sinusoidal Models (SL)",
            "5. HL Polynomial Roots & Vieta's Relations (HL)",
        ],
    )

    if "Quadratic" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Solves quadratic equations and finds vertex"
          " points.\n\n**Formulas:** $\\Delta = b^2 - 4ac$ | $x = \\frac{-b \\pm" " \\sqrt{\\Delta}}{2a}$"
      )
      st.markdown(
          """
            <div class="example-box">
                <b>💡 Simple Example Problem:</b><br>
                Solve $x^2 - 5x + 6 = 0$. (a=1, b=-5, c=6).
            </div>
            """,
          unsafe_allow_html=True,
      )
      c1, c2, c3 = st.columns(3)
      a = c1.number_input("a", value=1.0)
      b = c2.number_input("b", value=-5.0)
      c_val = c3.number_input("c", value=6.0)
      if st.button("Solve Quadratic"):
        if a == 0:
          st.error("'a' cannot be zero.")
        else:
          delta = (b**2) - (4 * a * c_val)
          vx = -b / (2 * a)
          vy = a * (vx**2) + b * vx + c_val
          st.write(
              f"**Discriminant ($\\Delta$):** `{delta:.4f}` | **Vertex:**"
              f" `({vx:.4f}, {vy:.4f})`"
          )
          if delta > 0:
            x1 = (-b + mt.sqrt(delta)) / (2 * a)
            x2 = (-b - mt.sqrt(delta)) / (2 * a)
            st.success(f"**Roots:** `x1 = {x1:.4f}`, `x2 = {x2:.4f}`")
          elif delta == 0:
            st.success(f"**Single Root:** `x = {vx:.4f}`")
          else:
            st.warning("No real roots.")

    elif "Exponential" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Models population growth or radioactive decay."
          "\n\n**Formula:** $f(t) = a \\cdot b^t + k$"
      )
      a = st.number_input("Initial Amount (a):", value=100.0)
      b = st.number_input("Multiplier (b):", value=1.05)
      t = st.number_input("Time (t):", value=10.0)
      if st.button("Calculate Exponential"):
        res = a * (b**t)
        st.success(f"**Result f({t}):** `{res:.4f}`")

    elif "Composite" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Evaluates nested functions: $(f \\circ g)(x) ="
          " f(g(x))$"
      )
      x_val = st.number_input("Input x:", value=3.0)
      if st.button("Evaluate Composite"):
        gx = x_val + 2
        fgx = gx**2
        st.success(f"**g(x) = x + 2** $\\rightarrow$ **f(g({x_val})) = {fgx}**")

    elif "Sinusoidal" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Trigonometric models: $f(x) = a \\sin(b(x-c)) + d$"
          "\n\n**Period:** $\\frac{2\\pi}{b}$"
      )
      b_val = st.number_input("Frequency parameter (b):", value=2.0)
      if st.button("Calculate Period"):
        period = (2 * mt.pi) / b_val
        st.success(f"**Period:** `{period:.4f}`")

    elif "Polynomial" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**What it does (HL):** Vieta's formulas for roots sum and product."
      )
      c1, c2, c3 = st.columns(3)
      a = c1.number_input("a", value=2.0)
      b = c2.number_input("b", value=-8.0)
      c = c3.number_input("c", value=6.0)
      if st.button("Calculate Vieta"):
        st.success(
            f"**Sum of Roots:** `{-b/a:.4f}` | **Product of Roots:**"
            f" `{c/a:.4f}`"
        )

  # ---------------------------------------------------------
  # 3. GEOMETRY AND TRIGONOMETRY
  # ---------------------------------------------------------
  elif category == "3. Geometry and Trigonometry":
    st.header("📐 Topic 3: Geometry & Trigonometry")
    lvl = st.radio("Level Filter:", ["All", "SL", "HL"], key="geom_lvl")

    formula = st.selectbox(
        "Select Formula / Tool:",
        [
            "1. 2D & 3D Distance Between Points (SL)",
            "2. Sine & Cosine Rules & Triangle Area (SL)",
            "3. Sector Arc Length & Area (SL)",
            "4. Volume & Surface Area of Solids (SL)",
            "5. HL Vectors: Dot Product & Angle (HL)",
            "6. HL Vectors: Cross Product & Area (HL)",
            "7. HL 3D Lines & Planes (HL)",
        ],
    )

    if "Distance" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Finds straight-line distance in 2D/3D space."
          "\n\n**Formula:** $d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 +" " (z_2-z_1)^2}$"
      )
      c1, c2 = st.columns(2)
      with c1:
        x1 = st.number_input("X1", value=0.0)
        y1 = st.number_input("Y1", value=0.0)
        z1 = st.number_input("Z1", value=0.0)
      with c2:
        x2 = st.number_input("X2", value=3.0)
        y2 = st.number_input("Y2", value=4.0)
        z2 = st.number_input("Z2", value=12.0)
      if st.button("Calculate Distance"):
        dist = mt.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
        st.success(f"**Distance:** `{dist:.4f}` units")

    elif "Sine & Cosine" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Solves triangles.\n\n**Cosine Rule:** $c^2 = a^2 +"
          " b^2 - 2ab \\cos C$ | **Area:** $A = \\frac{1}{2}ab \\sin C$"
      )
      c1, c2, c3 = st.columns(3)
      a = c1.number_input("Side a:", value=5.0)
      b = c2.number_input("Side b:", value=7.0)
      angle_c = c3.number_input("Angle C (deg):", value=60.0)
      if st.button("Calculate Triangle"):
        c_sq = (a**2) + (b**2) - (2 * a * b * mt.cos(mt.radians(angle_c)))
        side_c = mt.sqrt(c_sq)
        area = 0.5 * a * b * mt.sin(mt.radians(angle_c))
        st.success(
            f"**Side c:** `{side_c:.4f}` | **Triangle Area:** `{area:.4f}`"
        )

    elif "Sector" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Circle sector calculations.\n\n**Formulas:** $s ="
          " r\\theta$ | $A = \\frac{1}{2}r^2\\theta$"
      )
      r = st.number_input("Radius (r):", value=5.0)
      deg = st.number_input("Angle (Degrees):", value=90.0)
      if st.button("Calculate Sector"):
        rad = mt.radians(deg)
        st.success(
            f"**Arc Length (s):** `{r*rad:.4f}` | **Sector Area:**"
            f" `{0.5*(r**2)*rad:.4f}`"
        )

    elif "Volume" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Computes 3D volumes (Cylinder, Cone, Sphere)."
      )
      solid = st.radio("Shape:", ["Cylinder", "Cone", "Sphere"], horizontal=True)
      if solid == "Cylinder":
        r = st.number_input("Radius (r):", value=3.0)
        h = st.number_input("Height (h):", value=5.0)
        if st.button("Volume"):
          st.success(f"**Volume:** `{mt.pi*(r**2)*h:.4f}`")
      elif solid == "Cone":
        r = st.number_input("Radius (r):", value=3.0)
        h = st.number_input("Height (h):", value=5.0)
        if st.button("Volume"):
          st.success(f"**Volume:** `{(1/3)*mt.pi*(r**2)*h:.4f}`")
      elif solid == "Sphere":
        r = st.number_input("Radius (r):", value=3.0)
        if st.button("Volume"):
          st.success(f"**Volume:** `{(4/3)*mt.pi*(r**3):.4f}`")

    elif "HL Vectors: Dot" in formula and lvl in ["All", "HL"]:
      st.markdown("**What it does (HL):** Dot product and angle between vectors.")
      c1, c2 = st.columns(2)
      u1 = c1.number_input("u1", value=1.0)
      u2 = c1.number_input("u2", value=2.0)
      u3 = c1.number_input("u3", value=2.0)
      v1 = c2.number_input("v1", value=3.0)
      v2 = c2.number_input("v2", value=4.0)
      v3 = c2.number_input("v3", value=0.0)
      if st.button("Calculate Dot Product"):
        dot = (u1 * v1) + (u2 * v2) + (u3 * v3)
        st.success(f"**Dot Product:** `{dot:.4f}`")

    elif "HL Vectors: Cross" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**What it does (HL):** Cross product for area/perpendicular"
          " vectors."
      )
      c1, c2 = st.columns(2)
      u1 = c1.number_input("u1", value=1.0)
      u2 = c1.number_input("u2", value=2.0)
      u3 = c1.number_input("u3", value=3.0)
      v1 = c2.number_input("v1", value=4.0)
      v2 = c2.number_input("v2", value=5.0)
      v3 = c2.number_input("v3", value=6.0)
      if st.button("Calculate Cross Product"):
        cx = u2 * v3 - u3 * v2
        cy = u3 * v1 - u1 * v3
        cz = u1 * v2 - u2 * v1
        st.success(
            f"**Cross Product (u × v):** `[{cx:.4f}, {cy:.4f}, {cz:.4f}]`"
        )

    elif "Lines & Planes" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**What it does (HL):** Vector line equation $\\mathbf{r} = \\mathbf{a}"
          " + t\\mathbf{b}$"
      )
      a1, a2, a3 = 1.0, 2.0, 3.0
      t = st.number_input("Parameter t:", value=2.0)
      b1, b2, b3 = 1.0, 0.0, -1.0
      if st.button("Evaluate Line Point"):
        st.success(
            f"**Point r(t):** `({a1 + t*b1}, {a2 + t*b2}, {a3 + t*b3})`"
        )

  # ---------------------------------------------------------
  # 4. STATISTICS AND PROBABILITY
  # ---------------------------------------------------------
  elif category == "4. Statistics and Probability":
    st.header("📊 Topic 4: Statistics & Probability")
    lvl = st.radio(
        "Level Filter:", ["All", "SL", "HL"], key="stat_lvl_dropdown"
    )

    formula = st.selectbox(
        "Select Formula / Tool:",
        [
            "1. Summary Statistics: Mean, Variance & Std Dev (SL)",
            "2. Z-Score Standardization (SL)",
            "3. Expected Value E(X) & Variance Var(X) (SL)",
            "4. Binomial Distribution P(X=x) (SL)",
            "5. Normal Distribution Probability (SL)",
            "6. HL Poisson Distribution (HL)",
            "7. HL Chi-Squared Test Statistic (HL)",
            "8. Pearson Correlation Coefficient r (SL)",
        ],
    )

    if "Summary Statistics" in formula and lvl in ["All", "SL"]:
      raw = st.text_input("Enter dataset:", "12, 15, 18, 22, 30, 35")
      if st.button("Calculate Stats"):
        try:
          data = [float(x.strip()) for x in raw.split(",") if x.strip()]
          n = len(data)
          mean_v = sum(data) / n
          var = sum((x - mean_v) ** 2 for x in data) / (
              n - 1 if n > 1 else 1
          )
          st.success(
              f"**Mean (μ):** `{mean_v:.4f}` | **Std Dev:** `{mt.sqrt(var):.4f}`"
              f" | **Variance:** `{var:.4f}`"
          )
        except Exception:
          st.error("Invalid dataset.")

    elif "Z-Score" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Formula:** $z = \\frac{x - \\mu}{\\sigma}$ (Standardized normal"
          " score)"
      )
      c1, c2, c3 = st.columns(3)
      x = c1.number_input("Value (x):", value=85.0)
      mu = c2.number_input("Mean (μ):", value=70.0)
      sigma = c3.number_input("Std Dev (σ):", min_value=0.001, value=10.0)
      if st.button("Calculate Z-Score"):
        st.success(f"**Z-Score:** `{(x - mu) / sigma:.4f}`")

    elif "Expected Value" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Formulas:** $E(X) = \\sum x \\cdot P(X=x)$\vert{}$Var(X) = E(X^2) -"
          " [E(X)]^2$"
      )
      xs_in = st.text_input("X values:", "1, 2, 3")
      ps_in = st.text_input("P(X) values:", "0.2, 0.5, 0.3")
      if st.button("Calculate Expectation"):
        try:
          xs = [float(i.strip()) for i in xs_in.split(",")]
          ps = [float(i.strip()) for i in ps_in.split(",")]
          ex = sum(x * p for x, p in zip(xs, ps))
          varx = sum((x**2) * p for x, p in zip(xs, ps)) - (ex**2)
          st.success(f"**E(X):** `{ex:.4f}` | **Var(X):** `{varx:.4f}`")
        except Exception:
          st.error("Invalid input.")

    elif "Binomial" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Formula:** $P(X=x) = \\binom{n}{x} p^x (1-p)^{n-x}$"
      )
      c1, c2, c3 = st.columns(3)
      n = c1.number_input("n", value=10, min_value=1, step=1)
      x = c2.number_input("x", value=3, min_value=0, step=1)
      p = c3.number_input("p", value=0.4, min_value=0.0, max_value=1.0)
      if st.button("Calculate Binomial"):
        prob = mt.comb(int(n), int(x)) * (p**x) * ((1 - p) ** (n - x))
        st.success(f"**P(X={x}):** `{prob:.4f}`")

    elif "Normal" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Normal distribution cumulative probability"
          " reference."
      )
      st.info(
          "For precise normal probabilities, use your GDC calculator or"
          " standard normal tables (Z-table)."
      )

    elif "Poisson" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**HL Poisson:** $P(X=x) = \\frac{e^{-\\lambda} \\lambda^x}{x!}$"
      )
      lam = st.number_input("Mean Rate (λ):", value=3.5)
      x = st.number_input("Occurrences (x):", value=2, min_value=0, step=1)
      if st.button("Calculate Poisson"):
        st.success(
            f"**P(X={x}):** `{(mt.exp(-lam)*(lam**x))/mt.factorial(int(x)):.4f}`"
        )

    elif "Chi-Squared" in formula and lvl in ["All", "HL"]:
      st.markdown("**HL Chi-Squared:** $\\chi^2 = \\sum \\frac{(O - E)^2}{E}$")
      obs = st.text_input("Observed (O):", "12, 18, 20")
      exp = st.text_input("Expected (E):", "15, 15, 20")
      if st.button("Calculate Chi2"):
        os = [float(i.strip()) for i in obs.split(",")]
        es = [float(i.strip()) for i in exp.split(",")]
        st.success(
            f"**Chi-Squared (χ²):** `{sum(((o-e)**2)/e for o,e in zip(os,es)):.4f}`"
        )

    elif "Pearson" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**What it does:** Measures linear correlation strength ($r$ between"
          " -1 and 1)."
      )
      st.info("Input datasets into your GDC or regression tools to compute r.")

  # ---------------------------------------------------------
  # 5. CALCULUS
  # ---------------------------------------------------------
  elif category == "5. Calculus":
    st.header("📉 Topic 5: Calculus")
    lvl = st.radio("Level Filter:", ["All", "SL", "HL"], key="calc_lvl")

    formula = st.selectbox(
        "Select Formula / Tool:",
        [
            "1. Power Rule Derivative & Slope (SL)",
            "2. Product & Quotient Rules (SL)",
            "3. Power Rule Integration (SL)",
            "4. Trapezoidal Rule for Area (SL)",
            "5. Kinematics: Displacement, Velocity, Acceleration (SL)",
            "6. HL Euler's Method for Differential Equations (HL)",
            "7. HL Integration by Parts (HL)",
        ],
    )

    if "Derivative" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Formula:** $\\frac{d}{dx}(ax^n) = anx^{n-1}$"
      )
      c1, c2, c3 = st.columns(3)
      a = c1.number_input("Coefficient (a):", value=3.0)
      n = c2.number_input("Power (n):", value=4.0)
      x_pt = c3.number_input("At x:", value=2.0)
      if st.button("Calculate Derivative"):
        deriv_a = a * n
        deriv_n = n - 1
        st.success(
            f"**Derivative:** `{deriv_a}x^({deriv_n})` | **Slope at x={x_pt}:**"
            f" `{deriv_a*(x_pt**deriv_n):.4f}`"
        )

    elif "Product" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Product Rule:** $\\frac{d}{dx}(uv) = u'v + uv'$ | **Quotient"
          " Rule:** $\\frac{d}{dx}(\\frac{u}{v}) = \\frac{u'v - uv'}{v^2}$"
      )
      st.info(
          "Use these rules when differentiating products or quotients of"
          " functions."
      )

    elif "Integration" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Indefinite Integral:** $\\int ax^n dx = \\frac{a}{n+1} x^{n+1} + C$"
      )
      c1, c2 = st.columns(2)
      a = c1.number_input("Coefficient (a):", value=6.0)
      n = c2.number_input("Power (n):", value=2.0)
      if st.button("Calculate Integral"):
        if n == -1:
          st.success(f"**Integral:** `{a} \\ln|x| + C`")
        else:
          st.success(f"**Integral:** `{a/(n+1):.4f}x^({n+1}) + C`")

    elif "Trapezoidal" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Trapezoidal Rule:** Area $\\approx \\frac{h}{2} [y_0 + 2(y_1 + \\dots"
          " + y_{n-1}) + y_n]$"
      )
      vals = st.text_input("y values:", "2, 4, 6, 8, 5")
      h = st.number_input("Width (h):", value=0.5)
      if st.button("Calculate Area"):
        ys = [float(i.strip()) for i in vals.split(",")]
        st.success(
            f"**Area:** `{(h/2)*(ys[0] + ys[-1] + 2*sum(ys[1:-1])):.4f}`"
        )

    elif "Kinematics" in formula and lvl in ["All", "SL"]:
      st.markdown(
          "**Relations:** $v(t) = s'(t)$ (Velocity) | $a(t) = v'(t) = s''(t)$"
          " (Acceleration)"
      )
      st.info(
          "Differentiating displacement gives velocity; differentiating"
          " velocity gives acceleration."
      )

    elif "Euler's Method" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**HL Euler's:** $y_{n+1} = y_n + h \\cdot f(x_n, y_n)$"
      )
      yn = st.number_input("Current y:", value=1.0)
      h = st.number_input("Step size (h):", value=0.1)
      f_xy = st.number_input("Derivative f(x,y):", value=2.0)
      if st.button("Calculate Next y"):
        st.success(f"**Next y:** `{yn + (h * f_xy):.4f}`")

    elif "Parts" in formula and lvl in ["All", "HL"]:
      st.markdown(
          "**HL Integration by Parts:** $\\int u \\frac{dv}{dx} dx = uv - \\int"
          " v \\frac{du}{dx} dx$"
      )
      st.info(
          "Standard HL calculus technique for integrating products of"
          " functions."
      )

  # ---------------------------------------------------------
  # ⭐ RATE & REVIEWS
  # ---------------------------------------------------------
  elif category == "⭐ Rate & Reviews":
    st.header("⭐ Rate & Review This App")
    with st.form("rate_form"):
      rating = st.slider("Rating (1 to 5 Stars):", 1, 5, 5)
      comment = st.text_area("Your Review / Comment:")
      submit = st.form_submit_button("Submit Feedback")
      if submit:
        if comment:
          add_feedback(st.session_state["username"], rating, comment)
          st.success("Thank you! Your feedback has been posted.")
        else:
          st.warning("Please write a comment.")

    st.markdown("---")
    st.subheader("💬 Community Reviews")
    feedbacks = get_feedbacks()
    if feedbacks:
      for fb_id, fb_user, fb_rate, fb_com, fb_reply, fb_time in feedbacks:
        reply_html = (
            f"""<div style="background: #262B3D; padding: 10px; border-radius: 6px; margin-top: 8px; border-left: 3px solid #FF4B4B;"><b>👑 Admin Reply:</b> {fb_reply}</div>"""
            if fb_reply
            else ""
        )
        st.markdown(
            f"""
                <div class="card">
                    <b>👤 {fb_user}</b> &nbsp;|&nbsp; ⭐ <b>{fb_rate}/5</b> &nbsp;&nbsp;<span style="color: gray; font-size: 12px;">({fb_time})</span><br>
                    <p style="margin-top: 5px;">{fb_com}</p>
                    {reply_html}
                </div>
            """,
            unsafe_allow_html=True,
        )

  # ---------------------------------------------------------
  # 👑 ADMIN PANEL
  # ---------------------------------------------------------
  elif category == "👑 Admin Panel":
    if st.session_state["role"] == "admin":
      st.header("👑 Admin Panel - Full Control Center")
      tab_users, tab_reviews = st.tabs(
          ["👥 User Analytics & Management", "💬 Review & Reply Moderation"]
      )

      with tab_users:
        users = get_all_users()
        for u, r, count, last in users:
          col_u1, col_u2 = st.columns([3, 1])
          with col_u1:
            st.markdown(
                f"""
                        <div class="card" style="margin-bottom: 5px; padding: 10px;">
                            <b>User:</b> <code>{u}</code> | <b>Role:</b> <code>{r.upper()}</code> | <b>Logins:</b> <code>{count}</code> | <b>Last Login:</b> <code>{last}</code>
                        </div>
                    """,
                unsafe_allow_html=True,
            )
          with col_u2:
            if u != "aviator":
              if st.button("🗑️ Delete", key=f"del_user_{u}"):
                delete_user(u)
                st.success(f"User {u} deleted.")
                st.rerun()

      with tab_reviews:
        feedbacks = get_feedbacks()
        if feedbacks:
          for fb_id, fb_user, fb_rate, fb_com, fb_reply, fb_time in feedbacks:
            st.markdown(
                f"""
                        <div class="card">
                            <b>ID: {fb_id} | User: {fb_user}</b> | ⭐ {fb_rate}/5 <span style="color: gray; font-size: 12px;">({fb_time})</span>
                            <p><b>Comment:</b> {fb_com}</p>
                            {f"<b>Admin Reply:</b> {fb_reply}" if fb_reply else ""}
                        </div>
                    """
            )
            col_rep1, col_rep2 = st.columns([3, 1])
            with col_rep1:
              reply_text = st.text_input(
                  "Type reply:", key=f"reply_input_{fb_id}"
              )
            with col_rep2:
              if st.button("Send Reply", key=f"send_reply_{fb_id}"):
                if reply_text:
                  update_admin_reply(fb_id, reply_text)
                  st.success("Reply sent!")
                  st.rerun()

            if st.button(
                "❌ Delete Review", key=f"del_rev_{fb_id}", type="secondary"
            ):
              delete_feedback(fb_id)
              st.success("Review deleted.")
              st.rerun()
            st.markdown("---")