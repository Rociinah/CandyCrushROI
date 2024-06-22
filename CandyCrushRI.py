import pygame
import random

# Constantes
ANCHO = 800
ALTO = 600
ANCHO_PANTALLA = 1100
ALTO_PANTALLA = 800
ANCHO_PANTA = 240
ALTO_PANTA = 500
CELDA = 60
MARGEN = 20  # Margen entre el texto y el borde de la pantalla
COLOR_FONDI = (205, 100, 125)
COLOR_FONDO = (0, 0, 0)  # Negro
COLOR_FONDO_TABLERO = (125, 125, 125)  # Gris para el tablero
COLORES = ["rojo", "verde", "azul", "amarillo", "naranja", "morado"]  # Colores de los dulces

# Inicialización de Pygame
pygame.init()

# Carga de imágenes
imagenes_caramelos = {
    "rojo": pygame.image.load("C:/Users/rocio/Juego/Imagenes/Dulce4.png"),
    "verde": pygame.image.load("C:/Users/rocio/Juego/Imagenes/Dulce2.png"),
    "azul": pygame.image.load("C:/Users/rocio/Juego/Imagenes/Dulce3.png"),
    "amarillo": pygame.image.load("C:/Users/rocio/Juego/Imagenes/Dulce6.png"),
    "naranja": pygame.image.load("C:/Users/rocio/Juego/Imagenes/Dulce1.png"),
    "morado": pygame.image.load("C:/Users/rocio/Juego/Imagenes/Dulce5.png")
}

# Configuración de fuentes
fuente_titulo = pygame.font.SysFont("Georgia", 64)
fuente_texto = pygame.font.SysFont("Times New Roman", 28)
color_texto = (0, 0, 0)

class Tablero:
    def __init__(self, nivel=1, objetivos=None, movimientos_restantes=None):
        self.nivel = nivel  # Initialize nivel here
        self.definir_forma_tablero()
        self.dulces = [[random.choice(COLORES) for _ in range(self.ancho_celdas)] for _ in range(self.alto_celdas)]
        self.dulce_seleccionado = None
        self.movimientos_restantes = movimientos_restantes if movimientos_restantes is not None else random.randint(5 + 5 * self.nivel, 10 + 5 * self.nivel)
        self.objetivos = objetivos if objetivos is not None else {}
        self.cumplido = {}
        self.puntaje = 0
        if not objetivos:
            self.generar_objetivos()

    def definir_forma_tablero(self):
        formas = {
            1: (ANCHO // CELDA, ALTO // CELDA),  # Nivel 1: Tablero completo
            2: (6, ALTO// CELDA),  # Nivel 2: Rectángulo vertical
            3: (13, (ALTO // CELDA) // 2),  # Nivel 3: Rectángulo horizontal
            4: (8, 8),  # Nivel 4: Cuadrado pequeño
            5: (11, 11),  # Nivel 5: Cuadrado mediano
            6: (5,5)
        }
        self.ancho_celdas, self.alto_celdas = formas.get(self.nivel, (ANCHO // CELDA, ALTO // CELDA))
        # Ajusta los valores a continuación para mover el tablero
        desplazamiento_derecha = 120  # Aumenta este valor para mover el tablero a la derecha
        desplazamiento_abajo = 80  # Aumenta este valor para mover el tablero hacia abajo

        self.tablero_x = (ANCHO_PANTALLA - self.ancho_celdas * CELDA) // 2 + desplazamiento_derecha
        self.tablero_y = (ALTO_PANTALLA - self.alto_celdas * CELDA) // 2 + desplazamiento_abajo

    def intercambiar_dulces(self, x1, y1, x2, y2):
        if 0 <= x1 < self.ancho_celdas and 0 <= y1 < self.alto_celdas and 0 <= x2 < self.ancho_celdas and 0 <= y2 < self.alto_celdas:
            self.dulces[y1][x1], self.dulces[y2][x2] = self.dulces[y2][x2], self.dulces[y1][x1]
            self.movimientos_restantes -= 1

    def hay_coincidencias(self):
        coincidencias = False
        for y in range(self.alto_celdas):
            for x in range(self.ancho_celdas):
                if self.dulces[y][x] is None:
                    continue
                if self.verificar_coincidencia(x, y):
                    coincidencias = True
        return coincidencias

    def verificar_coincidencia(self, x, y):
        color = self.dulces[y][x]
        if color is None:
            return []

        coincidencias = []

        # Verificar horizontal hacia la derecha
        group = [(x, y)]
        for i in range(1, 6):  # Acepta hasta 5
            if x + i < self.ancho_celdas and self.dulces[y][x + i] == color:
                group.append((x + i, y))
            else:
                break
        if len(group) >= 3:
            coincidencias.extend(group)

        # Verificar horizontal hacia la izquierda
        group = [(x, y)]
        for i in range(1, 6):  # Acepta hasta 5
            if x - i >= 0 and self.dulces[y][x - i] == color:
                group.append((x - i, y))
            else:
                break
        if len(group) >= 3:
            coincidencias.extend(group)

        # Verificar vertical hacia abajo
        group = [(x, y)]
        for i in range(1, 6):  # Acepta hasta 5
            if y + i < self.alto_celdas and self.dulces[y + i][x] == color:
                group.append((x, y + i))
            else:
                break
        if len(group) >= 3:
            coincidencias.extend(group)

        # Verificar vertical hacia arriba
        group = [(x, y)]
        for i in range(1, 6):  # Acepta hasta 5
            if y - i >= 0 and self.dulces[y - i][x] == color:
                group.append((x, y - i))
            else:
                break
        if len(group) >= 3:
            coincidencias.extend(group)

        # Verificar forma de T
        patterns_T = [
            [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],  # T
            [(0, 1), (1, 1), (2, 1), (2, 0), (2, 2)],  # T volteada
            [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)],  # T acostada derecha
            [(0, 2), (1, 2), (2, 2), (1, 1), (1, 0)],  # T acostada izquierda
        ]

        for pattern in patterns_T:
            coincidentes_temp = [(x, y)]
            for dx, dy in pattern:
                cx, cy = x + dx, y + dy
                if 0 <= cx < self.ancho_celdas and 0 <= cy < self.alto_celdas and self.dulces[cy][cx] == color:
                    coincidentes_temp.append((cx, cy))
                else:
                    break
            if len(coincidentes_temp) >= 3:
                coincidencias.extend(coincidentes_temp)

        # Verificar forma de L
        patterns_L = [
            [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # L
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],  # L volteada
            [(0, 2), (1, 2), (2, 2), (2, 1), (2, 0)],  # L acostada derecha
            [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2)],  # L acostada izquierda
        ]

        for pattern in patterns_L:
            coincidentes_temp = [(x, y)]
            for dx, dy in pattern:
                cx, cy = x + dx, y + dy
                if 0 <= cx < self.ancho_celdas and 0 <= cy < self.alto_celdas and self.dulces[cy][cx] == color:
                    coincidentes_temp.append((cx, cy))
                else:
                    break
            if len(coincidentes_temp) >= 3:
                coincidencias.extend(coincidentes_temp)

        # Eliminar duplicados
        coincidencias = list(set(coincidencias))

        if len(coincidencias) >= 3:
            for cx, cy in coincidencias:
                self.dulces[cy][cx] = None
                if color in self.objetivos:
                    self.cumplido[color] += 1
                    self.puntaje += 75  # Sumar 75 puntos por eliminar un dulce objetivo
                else:
                    self.puntaje += 50  # Sumar 50 puntos por eliminar un dulce no objetivo
            return True
        return False

    def generar_objetivos(self):
        self.objetivos = {color: random.randint(3, 5) + 2 * self.nivel for color in random.sample(COLORES, k=3)}
        self.cumplido = {color: 0 for color in self.objetivos}

    def verificar_objetivo(self):
        return all(self.cumplido.get(color, 0) >= self.objetivos[color] for color in self.objetivos)

    def rellenar_dulces(self):
        for y in range(self.alto_celdas):
            for x in range(self.ancho_celdas):
                if self.dulces[y][x] is None:
                    self.dulces[y][x] = random.choice(COLORES)

    def detectar_clic(self, pos):
        if self.dulce_seleccionado is not None:
            x, y = pos
            columna = (x - self.tablero_x) // CELDA
            fila = (y - self.tablero_y) // CELDA
            if 0 <= columna < self.ancho_celdas and 0 <= fila < self.alto_celdas:
                dx, dy = self.dulce_seleccionado
                if abs(columna - dx) + abs(fila - dy) == 1:
                    self.intercambiar_dulces(dx, dy, columna, fila)
                    self.dulce_seleccionado = None
                    while self.hay_coincidencias():
                        self.eliminar_coincidencias()
                        self.rellenar_tablero()
                else:
                    self.dulce_seleccionado = (columna, fila)
        else:
            x, y = pos
            columna = (x - self.tablero_x) // CELDA
            fila = (y - self.tablero_y) // CELDA
            self.dulce_seleccionado = (columna, fila)

    def eliminar_coincidencias(self):
        for y in range(self.alto_celdas):
            for x in range(self.ancho_celdas):
                self.verificar_coincidencia(x, y)

    def rellenar_tablero(self):
        for x in range(self.ancho_celdas):
            huecos = 0
            for y in range(self.alto_celdas - 1, -1, -1):
                if self.dulces[y][x] is None:
                    huecos += 1
                elif huecos > 0:
                    for i in range(1, huecos + 1):
                        self.dulces[y + i][x] = self.dulces[y + i - 1][x]
                    self.dulces[y][x] = None
            for y in range(huecos):
                self.dulces[y][x] = random.choice(COLORES)

    def mostrar_mensaje(self, pantalla, mensaje):
        # Dibujar un rectángulo gris para el fondo del mensaje
        rectangulo_mensaje = pygame.Rect(ANCHO_PANTALLA // 4, ALTO_PANTALLA // 4 , ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 )
        pygame.draw.rect(pantalla, COLOR_FONDI, rectangulo_mensaje)

        # Dibujar el texto del mensaje
        texto_mensaje = fuente_titulo.render(mensaje, True, color_texto)
        rectangulo_texto = texto_mensaje.get_rect(center=rectangulo_mensaje.center)
        pantalla.blit(texto_mensaje, rectangulo_texto)

        # Mostrar instrucción para continuar
        texto_instruccion = fuente_texto.render("Haz clic para continuar", True, color_texto)
        rectangulo_instruccion = texto_instruccion.get_rect(center=(rectangulo_mensaje.centerx, rectangulo_mensaje.centery + 80))
        pantalla.blit(texto_instruccion, rectangulo_instruccion)

    def actualizar(self):
        while self.hay_coincidencias():
            self.eliminar_coincidencias()
            self.rellenar_tablero()

    def dibujar(self, pantalla):
        # Dibujar el fondo del tablero
        #pygame.draw.rect(pantalla, COLOR_FONDO_TABLERO, (ANCHO_PANTALLA - ANCHO - MARGEN, ALTO_PANTALLA - ALTO - MARGEN, ANCHO, ALTO))
        
        # Dibujar el fondo del tablero
        tablero_x = self.tablero_x
        tablero_y = self.tablero_y

        # Dibujar los dulces
        for y in range(self.alto_celdas):
            for x in range(self.ancho_celdas):
                color = self.dulces[y][x]
                pygame.draw.rect(pantalla, COLOR_FONDO_TABLERO, (tablero_x + x * CELDA, tablero_y + y * CELDA, CELDA, CELDA))
                if color is not None:
                    pantalla.blit(imagenes_caramelos[color], (tablero_x + x * CELDA, tablero_y + y * CELDA))


        # Resaltar caramelo seleccionado
        if self.dulce_seleccionado:
            x, y = self.dulce_seleccionado
            pygame.draw.rect(pantalla, (255, 255, 0), pygame.Rect(tablero_x + x * CELDA, tablero_y + y * CELDA, CELDA, CELDA), 3)


        # Dibujar información
        rectangulo_info = pygame.Rect(MARGEN, MARGEN + 160, ANCHO_PANTA, ALTO_PANTA)
        pantalla.fill(COLOR_FONDI, rectangulo_info)

        texto_puntaje = fuente_texto.render(f"Puntaje: {self.puntaje}", True, (255, 255, 255))
        pantalla.blit(texto_puntaje, (MARGEN + 15, MARGEN + 300))

        color_movimientos = (200, 0, 0) if self.movimientos_restantes < 10 else (255, 255, 255)
        texto_movimientos = fuente_texto.render(f"Movimientos: {self.movimientos_restantes}", True, color_movimientos)
        pantalla.blit(texto_movimientos, (MARGEN + 15, MARGEN + 260))

        texto_nivel = fuente_texto.render(f"Nivel: {self.nivel}", True, (255, 255, 255))
        pantalla.blit(texto_nivel, (MARGEN + 15, MARGEN + 220))

        texto_objetivos = fuente_texto.render("Objetivos:", True, (255, 255, 255))
        pantalla.blit(texto_objetivos, (MARGEN + 15, MARGEN + 340))

        y_offset = MARGEN + 370
        for color, cantidad in self.objetivos.items():
            color_texto_objetivo = (0, 200, 15) if self.cumplido.get(color, 0) >= cantidad else (255,255,255)
            texto_objetivo = fuente_texto.render(f"{color}: {self.cumplido.get(color, 0)}/{cantidad}", True, color_texto_objetivo)
            pantalla.blit(texto_objetivo, (MARGEN + 45, y_offset))
            y_offset += 40

        texto_titulo = fuente_titulo.render("Candy Crush Raihe",True, color_texto)
        pantalla.blit(texto_titulo,(MARGEN + 400, MARGEN + 60))
        
        # Barra de progreso general del nivel
        total_objetivos = sum(self.objetivos.values())
        total_cumplido = sum(self.cumplido.values())
        progreso_nivel = total_cumplido / total_objetivos if total_objetivos > 0 else 0

        barra_largo = 200
        pygame.draw.rect(pantalla, (125, 125, 125), (MARGEN + 15, MARGEN + 190, barra_largo, 20), 2)
        pygame.draw.rect(pantalla, (255, 255, 255), (MARGEN + 15, MARGEN + 190, (barra_largo * progreso_nivel)//2, 18))

    def avanzar_nivel(self):
        self.nivel += 1
        self.definir_forma_tablero()
        self.dulces = [[random.choice(COLORES) for _ in range(self.ancho_celdas)] for _ in range(self.alto_celdas)]
        self.movimientos_restantes = random.randint(5 + 5 * self.nivel, 10 + 5 * self.nivel)
        self.generar_objetivos()
        self.actualizar()
        self.puntaje = 0
        for color in COLORES:
            self.cumplido[color] = 0

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Candy Crush RI")
    imagen_fondo = pygame.image.load(r"C:/Users/rocio/Juego/Imagenes/fondo_inte.jpg").convert()
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))

    tablero = Tablero(nivel=1)  # Empezar con nivel 1
    tablero.actualizar()
    for color in COLORES:
        tablero.cumplido[color] = 0
    tablero.puntaje = 0   
    corriendo = True
    juego_terminado = False

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if juego_terminado:
                    if tablero.verificar_objetivo():
                        tablero.avanzar_nivel()
                        juego_terminado = False
                    else:
                        # Reiniciar el tablero con el estado guardado
                        tablero = Tablero(nivel=nivel_perdido, objetivos=objetivos_perdidos, movimientos_restantes=movimientos_restantes_perdidos)
                        juego_terminado = False
                else:
                    tablero.detectar_clic(pygame.mouse.get_pos())

        pantalla.fill(COLOR_FONDO)
        # Dibujar imagen de fondo después del fondo inicial
        pantalla.blit(imagen_fondo, (0, 0))
        tablero.dibujar(pantalla)
        pygame.display.update()


        if tablero.movimientos_restantes == 0:
            tablero.mostrar_mensaje(pantalla, "Has Perdido")
            nivel_perdido = tablero.nivel
            objetivos_perdidos = tablero.objetivos
            movimientos_restantes_perdidos = random.randint(5 + 5 * tablero.nivel, 10 + 5 * tablero.nivel)
            pygame.display.update()
            juego_terminado = True
        elif tablero.verificar_objetivo():
            tablero.mostrar_mensaje(pantalla, "Has Ganado")
            pygame.display.update()
            juego_terminado = True

        pygame.time.wait(100)

    pygame.quit()

if __name__ == "__main__":
    main()

