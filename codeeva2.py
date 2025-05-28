import requests

# Configuración - REEMPLAZA CON TU API KEY REAL
API_KEY = "1569424a-c362-4a64-acf8-30fbe1c1ee85"
BASE_URL = "https://graphhopper.com/api/1/route"

def obtener_coordenadas(ciudad):
    """Obtiene coordenadas aproximadas para una ciudad"""
    # Diccionario con coordenadas aproximadas de ciudades chilenas
    coordenadas_chile = {
        'santiago': (-33.4489, -70.6693),
        'ovalle': (-30.5983, -71.2003),
        'valparaiso': (-33.0472, -71.6127),
        'concepcion': (-36.8267, -73.0617)
    }
    
    ciudad_lower = ciudad.lower().strip()
    if ciudad_lower in coordenadas_chile:
        return coordenadas_chile[ciudad_lower]
    else:
        print(f"Ciudad '{ciudad}' no encontrada en la base local")
        return None

def obtener_ruta(origen, destino):
    try:
        # Primero intentamos obtener coordenadas
        coord_origen = obtener_coordenadas(origen)
        coord_destino = obtener_coordenadas(destino)
        
        if not coord_origen or not coord_destino:
            return None
            
        params = {
            'point': [f"{coord_origen[0]},{coord_origen[1]}", 
                     f"{coord_destino[0]},{coord_destino[1]}"],
            'vehicle': 'car',
            'key': API_KEY,
            'instructions': True,
            'locale': 'es'
        }
        
        print("\nRealizando petición a la API...")
        response = requests.get(BASE_URL, params=params, timeout=15)
        print(f"Código de respuesta: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error en la API: {response.text}")
            return None
            
        return response.json()
    
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        return None

def mostrar_resultados(datos):
    if not datos or not datos.get('paths'):
        print("\nNo se pudo obtener resultados. Posibles causas:")
        print("1. API key incorrecta o no válida")
        print("2. Problema de conexión a internet")
        print("3. Las ciudades no fueron reconocidas")
        return
    
    ruta = datos['paths'][0]
    distancia = ruta['distance'] / 1000  # metros a km
    tiempo = ruta['time'] / 1000  # ms a segundos
    
    print("\n--- RESULTADOS ---")
    print(f"Distancia total: {distancia:.2f} km")
    
    horas = int(tiempo // 3600)
    minutos = int((tiempo % 3600) // 60)
    print(f"Duración del viaje: {horas}h {minutos}m")
    
    combustible = (distancia * 8) / 100  # 8L/100km
    print(f"Combustible estimado: {combustible:.2f} litros")
    
    print("\n--- DETALLES DE LA RUTA ---")
    for paso in ruta['instructions']:
        print(f"{paso['text']} ({paso['distance']/1000:.2f} km)")

def main():
    print("\nSistema de Cálculo de Rutas")
    print("(Ingrese 'q' para salir)\n")
    
    while True:
        origen = input("Ciudad de origen: ").strip()
        if origen.lower() == 'q':
            break
            
        destino = input("Ciudad de destino: ").strip()
        if destino.lower() == 'q':
            break
        
        print(f"\nCalculando ruta desde {origen} a {destino}...")
        datos_ruta = obtener_ruta(origen, destino)
        mostrar_resultados(datos_ruta)
        
        if input("\nPresione Enter para continuar o 'q' para salir: ").lower() == 'q':
            break

if __name__ == "__main__":
    main()