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
COLOR_FONDI = (205,100,125)
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
    def __init__(self):
        self.dulces = [[random.choice(COLORES) for _ in range(ANCHO // CELDA)] for _ in range(ALTO // CELDA)]
        self.dulce_seleccionado = None
        self.nivel = 1
        self.movimientos_restantes = random.randint(5 + 5 * self.nivel, 10 + 5 * self.nivel)
        self.objetivos = {}
        self.cumplido = {}
        self.puntaje = 0
        self.generar_objetivos()

    def intercambiar_dulces(self, x1, y1, x2, y2):
        self.dulces[y1][x1], self.dulces[y2][x2] = self.dulces[y2][x2], self.dulces[y1][x1]
        self.movimientos_restantes -= 1

    def hay_coincidencias(self):
        coincidencias = False
        for y in range(ALTO // CELDA):
            for x in range(ANCHO // CELDA):
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
            if x + i < ANCHO // CELDA and self.dulces[y][x + i] == color:
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
            if y + i < ALTO // CELDA and self.dulces[y + i][x] == color:
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
                if 0 <= cx < ANCHO // CELDA and 0 <= cy < ALTO // CELDA and self.dulces[cy][cx] == color:
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
                if 0 <= cx < ANCHO // CELDA and 0 <= cy < ALTO // CELDA and self.dulces[cy][cx] == color:
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
        colores_disponibles = COLORES[:]
        random.shuffle(colores_disponibles)
        num_objetivos = min(2 + self.nivel, len(colores_disponibles))

        self.objetivos = {}
        self.cumplido = {}

        for color in colores_disponibles[:num_objetivos]:
            cantidad = random.randint(5 * self.nivel, 20 * self.nivel)
            self.objetivos[color] = cantidad
            self.cumplido[color] = 0

    def eliminar_coincidencias(self):
        for y in range(ALTO // CELDA):
            for x in range(ANCHO // CELDA):
                self.verificar_coincidencia(x, y)

    def eliminar_dulce(self, posicion):
        fila, columna = posicion
        dulce = self.dulces[fila][columna]
        self.dulces[fila][columna] = random.choice(COLORES)
        self.puntaje += 10
        if dulce in self.cumplido:
            self.cumplido[dulce] += 1

    def rellenar_tablero(self):
        for x in range(ANCHO // CELDA):
            huecos = 0
            for y in range(ALTO // CELDA - 1, -1, -1):
                if self.dulces[y][x] is None:
                    huecos += 1
                elif huecos > 0:
                     # Mover los dulces hacia abajo lentamente
                    for i in range(1, huecos + 1):
                        self.dulces[y + i][x] = self.dulces[y + i - 1][x]
                    self.dulces[y][x] = None
            for y in range(huecos):
                self.dulces[y][x] = random.choice(COLORES)

    def objetivos_cumplidos(self):
        for color, cantidad in self.objetivos.items():
            if self.cumplido[color] < cantidad:
                return False
        return True

    def detectar_clic(self, pos):
        if self.dulce_seleccionado is not None:
            x, y = pos
            columna = (x - (ANCHO_PANTALLA - ANCHO - MARGEN)) // CELDA
            fila = (y - (ALTO_PANTALLA - ALTO - MARGEN)) // CELDA
            dx, dy = self.dulce_seleccionado
            if abs(columna - dx) + abs(fila - dy) == 1:
                self.intercambiar_dulces(columna, fila, dx, dy)
                self.dulce_seleccionado = None
                while self.hay_coincidencias():
                    self.eliminar_coincidencias()
                    self.rellenar_tablero()
        else:
            x, y = pos
            columna = (x - (ANCHO_PANTALLA - ANCHO - MARGEN)) // CELDA
            fila = (y - (ALTO_PANTALLA - ALTO - MARGEN)) // CELDA
            self.dulce_seleccionado = (columna, fila)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_FONDO_TABLERO, (ANCHO_PANTALLA - ANCHO - MARGEN, ALTO_PANTALLA - ALTO - MARGEN, ANCHO, ALTO))
        for y in range(ALTO // CELDA):
            for x in range(ANCHO // CELDA):
                color = self.dulces[y][x]
                if color is not None:
                    pantalla.blit(imagenes_caramelos[color], ((ANCHO_PANTALLA - ANCHO - MARGEN) + x * CELDA, (ALTO_PANTALLA - ALTO - MARGEN) + y * CELDA))

    def mostrar_info(self, pantalla):

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
            color_texto_objetivo = (0, 200, 15) if self.cumplido[color] >= cantidad else (255,255,255)
            texto_objetivo = fuente_texto.render(f"{color.capitalize()}: {self.cumplido.get(color, 0)} / {cantidad}", True, color_texto_objetivo)
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
        pygame.draw.rect(pantalla, (255, 255, 255), (MARGEN + 15, MARGEN + 190, barra_largo * progreso_nivel/2, 18))

        # Resaltar caramelo seleccionado
        if self.dulce_seleccionado:
            x, y = self.dulce_seleccionado
            pygame.draw.rect(pantalla, (255, 255, 0), (ANCHO_PANTALLA - ANCHO - MARGEN + x * CELDA, ALTO_PANTALLA - ALTO - MARGEN + y * CELDA, CELDA, CELDA), 3)
       
    
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

    def reset_puntaje_movimientos(self):
        self.puntaje = 0
        self.movimientos_restantes = random.randint(25, 40)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Candy Crush RI")
    imagen_fondo = pygame.image.load(r"C:/Users/rocio/Juego/Imagenes/fondo_inte.jpg").convert()
    imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
    tablero = Tablero()
    reloj = pygame.time.Clock()
    tablero.actualizar()
    for color in COLORES:
        tablero.cumplido[color] = 0
    tablero.puntaje = 0
    terminado = False
    juego_terminado = False

    
    while not terminado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminado = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if juego_terminado:
                    # Reiniciar el juego al hacer clic después de ganar o perder
                    tablero = Tablero()
                    tablero.nivel += 1
                    tablero.actualizar()
                    for color in COLORES:
                            tablero.cumplido[color] = 0
                    tablero.puntaje = 0
                    juego_terminado = False
                else:
                    tablero.detectar_clic(pygame.mouse.get_pos())

        # Dibujar fondo inicial en negro
        pantalla.fill(COLOR_FONDO)
        
        # Dibujar imagen de fondo después del fondo inicial
        pantalla.blit(imagen_fondo, (0, 0))

        tablero.dibujar(pantalla)
        tablero.mostrar_info(pantalla)

        if tablero.movimientos_restantes == 0:
            tablero.mostrar_mensaje(pantalla, "Has Perdido")
            juego_terminado = True
        elif all(tablero.cumplido[color] >= cantidad for color, cantidad in tablero.objetivos.items()):
            tablero.mostrar_mensaje(pantalla, "Has Ganado")
            juego_terminado = True

        pygame.display.flip()
        reloj.tick(30)  # FPS (30 frames por segundo)

    pygame.quit()

# Ejecutar el juego
if __name__ == "__main__":
    main()