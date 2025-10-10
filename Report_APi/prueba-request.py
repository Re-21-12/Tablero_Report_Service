import requests

base = "http://localhost:5232"

user = {
    "nombre": "Macario",
    "contrasena": "apple123"
}

r = requests.post(base + "/api/Auth/login", json=user)

print("Status code:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Raw response text:", r.text)  # Muestra el cuerpo
    
if r.ok and "application/json" in r.headers.get("Content-Type", ""):
    data = r.json()
    print("Token:", data.get("token"))
else:
    print("Error:", r.status_code, r.text)


token = data.get("token")
print("Token:", token[:60], "...")

# 2. Usar token
headers = {"Authorization": f"Bearer {token}"}
resp = requests.get(base + "/api/Jugador", headers=headers)

print(resp.status_code)
print(resp.text)