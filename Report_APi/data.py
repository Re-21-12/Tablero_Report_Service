import requests

base = "http://localhost:5232"



def obtener_token():
    user = {
        "nombre": "Macario",
        "contrasena": "apple123"
    }

    try:
        response = requests.post(f"{base}/api/Auth/login", json=user)

        if response.status_code == 200:
            data = response.json()
            token = data.get("token") or data.get("access_token")  # depende del backend
            print("✅ Token obtenido correctamente")
            return token
        else:
            print(f"❌ Error al obtener token: {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error de conexión: {e}")
        return None
    
token = obtener_token()


def Obtener_Jugadores(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+"/api/Jugadores", headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "No se pudo obtener la información"}


def obtener_usuarios(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{base}/api/Usuarios", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error al consultar usuarios: {response.status_code}")
        print(response.text)
        return None


if __name__ == "__main__":
    token = obtener_token()
    if token:
        usuarios = obtener_usuarios(token)
        if usuarios:
            print("Usuarios obtenidos:")
            for u in usuarios:
                print(u)