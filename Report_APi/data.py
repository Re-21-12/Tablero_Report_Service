import requests
from flask import jsonify

base = "http://localhost:5232"

user = {
}

def set_user(json):
    global user
    user = json

def obtener_token():
    global user

    try:
        response = requests.post(f"{base}/api/Auth/login", json=user)

        if response.status_code == 200:
            data = response.json()
            token = data.get("token") or data.get("access_token")  
            
            return token
        else:
            
            return None

    except requests.exceptions.RequestException as e:
        print(f" Error de conexión: {e}")
        return None
    


def Obtener_Jugadores(token):
    print(token)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+"/api/Jugador", headers=headers)
    print("ESta es la request: ")
    for k, v in response.request.headers.items():
        print(k + ":", v)
    if response.status_code == 200:
        print("Si pasa")
        return response.json()
    return {"error": "No se pudo obtener la información"}
def Obtener_Jugador(token, id_Jugador):
    print(token)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+f"/api/Jugador/{id_Jugador}", headers=headers)
    print("ESta es la request: ")
    for k, v in response.request.headers.items():
        print(k + ":", v)
    if response.status_code == 200:
        print("Si pasa")
        return response.json()
    return {"error": "No se pudo obtener la información"}
def Obtener_Jugadores_Equipo(token, id_equipo):
    print(token)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+f"/api/Jugador/byTeam/{id_equipo}", headers=headers)
    print("ESta es la request: ")
    for k, v in response.request.headers.items():
        print(k + ":", v)
    if response.status_code == 200:
        print("Si pasa")
        return response.json()
    return {"error": "No se pudo obtener la información"}
def Obtener_Equipos(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+"/api/Equipo", headers=headers)
    print("ESta es la request: ")
    for k, v in response.request.headers.items():
        print(k + ":", v)
    if response.status_code == 200:
        print("Si pasa")
        return response.json()
    return {"error": "No se pudo obtener la información"}
def Obtener_Equipo(token, id_Equipo):
    print(token)
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+f"/api/Equipo/{id_Equipo}", headers=headers)
    print("ESta es la request: ")
    for k, v in response.request.headers.items():
        print(k + ":", v)
    if response.status_code == 200:
        print("Si pasa")
        return response.json()
    return {"error": "No se pudo obtener la información"}
def Obtener_Partidos_Marcador(token): 
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(base+"/api/Partido/Resultado", headers=headers)
    print("ESta es la request: ")
    for k, v in response.request.headers.items():
        print(k + ":", v)
    if response.status_code == 200:
        print("Si pasa")
        return response.json()
    return {"error": "No se pudo obtener la información"}
def Obtener_Jugadores_Partido(token, id_Partido):
    headers = {'Authorization': f'Bearer {token}'}

    # 1️⃣ Obtener IDs y datos del partido
    r = requests.get(f"{base}/api/Partido/Reporte/{id_Partido}", headers=headers)
    r.raise_for_status()  # lanza error si no es 200
    partido_reporte = r.json()

    r = requests.get(f"{base}/api/Partido/{id_Partido}", headers=headers)
    r.raise_for_status()
    partido_info = r.json()

    # 2️⃣ Obtener jugadores de cada equipo
    local_id = partido_reporte["local"]
    visitante_id = partido_reporte["visitante"]

    r = requests.get(f"{base}/api/Jugador/byTeam/{local_id}", headers=headers)
    r.raise_for_status()
    jugadores_locales = r.json()

    r = requests.get(f"{base}/api/Jugador/byTeam/{visitante_id}", headers=headers)
    r.raise_for_status()
    jugadores_visitantes = r.json()

    return  partido_info, jugadores_locales, jugadores_visitantes

def Obtener_Estadisticas_Jugador(token, id_Jugador):
    print(token)
    headers = {'Authorization': f'Bearer {token}'}
    response = response = requests.get(base+f"/api/Jugador/{id_Jugador}", headers=headers)
    datos_jugador = response.json()
    response = requests.get(base+f"/api/Faltas/jugador/{id_Jugador}", headers=headers)
    total_faltas = response.json()
    response = requests.get(base+f"/api/Anotacion/jugador/{id_Jugador}", headers=headers)
    total_anotaciones = response.json()
    return datos_jugador, total_faltas, total_anotaciones
 

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