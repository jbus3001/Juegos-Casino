import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys
import random
import Funciones_Ruleta as fr

# --- CONFIGURACIÓN ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# --- ESTADOS DEL JUEGO ---
STATE_MENU = 0
STATE_BOARD = 1
STATE_SPINNING = 2
STATE_RESULT = 3

# --- SECUENCIAS REALES DE LA RULETA ---
SEQ_EUROPEA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
SEQ_AMERICANA = [0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, '00', 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2]

class RuletaGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Ruleta 2D OpenGL")
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
        glMatrixMode(GL_MODELVIEW)
        
        self.clock = pygame.time.Clock()
        try:
            self.font = pygame.font.SysFont("Arial", 24)
            self.large_font = pygame.font.SysFont("Arial", 48)
            self.number_font = pygame.font.SysFont("Arial", 16, bold=True)
        except:
            self.font = pygame.font.Font(None, 24)
            self.large_font = pygame.font.Font(None, 48)
            self.number_font = pygame.font.Font(None, 20)
        
        # Generar texturas de los números
        self.texturas_numeros = {}
        self.init_ruleta()
        
        self.state = STATE_MENU
        self.tipo_ruleta = "Europea"
        self.capital = 1000.0
        self.apuesta_actual = None
        self.apuesta_anterior = None
        self.monto_apostado = 0.0
        self.timer_start = 0
        
        self.resultado_giro = None
        self.angulo_ruleta = 0.0
        self.velocidad_giro = 0.0
        
        self.run()

    def init_ruleta(self):
        """Inicializa las texturas individuales para cada número de la ruleta."""
        numeros = set(SEQ_EUROPEA + SEQ_AMERICANA)
        for num in numeros:
            text_surf = self.number_font.render(str(num), True, (255, 255, 255))
            text_data = pygame.image.tostring(text_surf, "RGBA", True)
            w, h = text_surf.get_size()
            
            tex_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
            
            self.texturas_numeros[num] = (tex_id, w, h)

    def cambiar_tipo_ruleta(self, nuevo_tipo):
        """Modularización del cambio de tipo de ruleta"""
        self.tipo_ruleta = nuevo_tipo
        self.state = STATE_BOARD
        self.timer_start = pygame.time.get_ticks()

    def draw_text(self, x, y, text, color=(255, 255, 255), center=False, large=False):
        font = self.large_font if large else self.font
        text_surface = font.render(text, True, color, (0, 0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        width = text_surface.get_width()
        height = text_surface.get_height()
        
        if center:
            x -= width // 2
            y -= height // 2
            
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glRasterPos2d(x, y + height) 
        glDrawPixels(width, height, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        glDisable(GL_BLEND)

    def draw_rect(self, x, y, w, h, color):
        glColor3f(*color)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x+w, y)
        glVertex2f(x+w, y+h)
        glVertex2f(x, y+h)
        glEnd()

    def dibujar_ruleta_opengl(self, cx, cy, radius):
        """Dibuja la ruleta usando primitivas de OpenGL (GL_POLYGON, GL_LINE_STRIP)"""
        seq = SEQ_AMERICANA if self.tipo_ruleta == "Americana" else SEQ_EUROPEA
        segmentos = len(seq)
        angulo_por_segmento = 360.0 / segmentos
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Dibujar cuñas de la ruleta
        for i, num in enumerate(seq):
            start_angle = math.radians(i * angulo_por_segmento)
            end_angle = math.radians((i + 1) * angulo_por_segmento)
            
            if num == 0 or num == '00':
                glColor3f(20/255.0, 180/255.0, 20/255.0) # Verde
            else:
                dic = fr.ruleta_americana if self.tipo_ruleta == "Americana" else fr.ruleta_europea
                c = dic[num]
                if c == "rojo": glColor3f(200/255.0, 20/255.0, 20/255.0)
                elif c == "negro": glColor3f(20/255.0, 20/255.0, 20/255.0)
                
            # Usar GL_POLYGON para el segmento curvo
            glBegin(GL_POLYGON)
            glVertex2f(cx, cy)
            steps = 10
            for s in range(steps + 1):
                a = start_angle + (end_angle - start_angle) * (s / steps)
                x = cx + math.cos(a) * radius
                y = cy + math.sin(a) * radius
                glVertex2f(x, y)
            glEnd()
            
            # Dibujar borde blanco
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINE_STRIP)
            for s in range(steps + 1):
                a = start_angle + (end_angle - start_angle) * (s / steps)
                x = cx + math.cos(a) * radius
                y = cy + math.sin(a) * radius
                glVertex2f(x, y)
            glEnd()
            glBegin(GL_LINES)
            glVertex2f(cx, cy)
            glVertex2f(cx + math.cos(start_angle) * radius, cy + math.sin(start_angle) * radius)
            glEnd()

        # Dibujar texturas de los números
        glEnable(GL_TEXTURE_2D)
        glColor3f(1.0, 1.0, 1.0)
        
        text_radius = radius * 0.85
        for i, num in enumerate(seq):
            mid_angle_deg = i * angulo_por_segmento + angulo_por_segmento / 2
            mid_angle_rad = math.radians(mid_angle_deg)
            
            tx = cx + math.cos(mid_angle_rad) * text_radius
            ty = cy + math.sin(mid_angle_rad) * text_radius
            
            tex_id, w, h = self.texturas_numeros[num]
            glBindTexture(GL_TEXTURE_2D, tex_id)
            
            glPushMatrix()
            glTranslatef(tx, ty, 0)
            # Rotar el quad para que el texto apunte hacia afuera del círculo
            glRotatef(mid_angle_deg + 90, 0, 0, 1)
            
            # Dibujar el quad centrado
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 1.0); glVertex2f(-w/2, -h/2)
            glTexCoord2f(1.0, 1.0); glVertex2f(w/2, -h/2)
            glTexCoord2f(1.0, 0.0); glVertex2f(w/2, h/2)
            glTexCoord2f(0.0, 0.0); glVertex2f(-w/2, h/2)
            glEnd()
            
            glPopMatrix()
            
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

    def draw_menu(self):
        self.draw_text(WINDOW_WIDTH//2, 80, "¡Bienvenido al juego de la Ruleta!", (255,255,255), center=True, large=True)
        self.draw_text(WINDOW_WIDTH//2, 140, "Selecciona el tipo de ruleta que quieras jugar:", (255,255,255), center=True)
        
        # Boton Americana
        self.draw_rect(200, 250, 400, 80, (0.8, 0.0, 0.0))
        self.draw_text(WINDOW_WIDTH//2, 290, "RULETA AMERICANA", (255,255,255), center=True)
        
        # Boton Europea
        self.draw_rect(200, 400, 400, 80, (0.8, 0.0, 0.0))
        self.draw_text(WINDOW_WIDTH//2, 440, "RULETA EUROPEA", (255,255,255), center=True)
        
    def draw_board(self):
        self.draw_text(20, 20, f"Capital: ${self.capital}", (255,255,0))
        self.draw_text(20, 50, f"Monto apostado (fijo de $10): ${self.monto_apostado}", (255,255,255))
        
        time_elapsed = (pygame.time.get_ticks() - self.timer_start) // 1000
        time_left = max(0, 15 - time_elapsed)
        self.draw_text(WINDOW_WIDTH - 150, 20, f"Tiempo: {time_left}s", (255, 100, 100) if time_left <= 5 else (255, 255, 255))
        
        if self.apuesta_actual:
            self.draw_text(20, 80, f"Apuesta: {self.apuesta_actual['tipo']} ({self.apuesta_actual['detalle']})", (200,200,200))
            
        self.draw_text(WINDOW_WIDTH//2, 150, "Selecciona el tipo de apuestas que quieras realizar", (255,255,255), center=True)
        
        # Zonas de apuesta (Color)
        self.draw_rect(200, 250, 180, 100, (0.8, 0.1, 0.1)) # Rojo
        self.draw_text(290, 300, "ROJO", (255,255,255), center=True)
        
        self.draw_rect(420, 250, 180, 100, (0.1, 0.1, 0.1)) # Negro
        self.draw_text(510, 300, "NEGRO", (255,255,255), center=True)
        
        # Zonas de apuesta (Par / Impar)
        self.draw_rect(200, 380, 180, 100, (0.3, 0.3, 0.3)) 
        self.draw_text(290, 430, "PAR", (255,255,255), center=True)
        
        self.draw_rect(420, 380, 180, 100, (0.3, 0.3, 0.3)) 
        self.draw_text(510, 430, "IMPAR", (255,255,255), center=True)
        
        # Botón de Girar
        if self.apuesta_actual and self.monto_apostado > 0:
            self.draw_rect(550, 500, 220, 60, (0.8, 0.0, 0.0))
            self.draw_text(660, 530, "Finalizar apuestas", (0,0,0), center=True)
            
    def draw_spinning(self):
        self.draw_text(WINDOW_WIDTH//2, 50, "GIRANDO...", (255,255,255), center=True, large=True)
        
        cx, cy = WINDOW_WIDTH//2, WINDOW_HEIGHT//2
        radius = 200
        
        glPushMatrix()
        glTranslatef(cx, cy, 0)
        glRotatef(self.angulo_ruleta, 0, 0, 1)
        glTranslatef(-cx, -cy, 0)
        
        self.dibujar_ruleta_opengl(cx, cy, radius)
        
        glPopMatrix()
        
        # Dibujar marcador superior estático apuntando al número ganador
        # El marcador estará en el norte (cy - radius)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        glVertex2f(cx, cy - radius - 5)
        glVertex2f(cx - 15, cy - radius - 30)
        glVertex2f(cx + 15, cy - radius - 30)
        glEnd()

    def draw_result(self):
        self.draw_spinning() # Dibuja la ruleta en su posicion final
        
        color_res = fr.ruleta_americana[self.resultado_giro] if self.tipo_ruleta == "Americana" else fr.ruleta_europea[self.resultado_giro]
        msg = f"RESULTADO: {self.resultado_giro} ({color_res.upper()})"
        self.draw_text(WINDOW_WIDTH//2, 500, msg, (255,255,0), center=True, large=True)
        
        if self.capital > 0:
            self.draw_text(WINDOW_WIDTH//2, 560, "HAZ CLIC PARA CONTINUAR", (255,255,255), center=True)
        else:
            self.draw_text(WINDOW_WIDTH//2, 560, "¡SIN CAPITAL! JUEGO TERMINADO.", (255,0,0), center=True)

    def handle_click_menu(self, pos):
        x, y = pos
        if 200 <= x <= 600:
            if 250 <= y <= 330:
                self.cambiar_tipo_ruleta("Americana")
            elif 400 <= y <= 480:
                self.cambiar_tipo_ruleta("Europea")

    def girar_ruleta(self):
        """Calcula el angulo objetivo del giro garantizando que el numero seleccionado
        quede alineado con la flecha superior"""
        self.capital -= self.monto_apostado 
        self.state = STATE_SPINNING
        
        dic_ruleta = fr.ruleta_americana if self.tipo_ruleta == "Americana" else fr.ruleta_europea
        self.resultado_giro = random.choice(list(dic_ruleta.keys()))
        
        seq = SEQ_AMERICANA if self.tipo_ruleta == "Americana" else SEQ_EUROPEA
        idx = seq.index(self.resultado_giro)
        
        segmentos = len(seq)
        angulo_por_segmento = 360.0 / segmentos
        mid_angle = idx * angulo_por_segmento + angulo_por_segmento / 2
        
        # El marcador está en "arriba", es decir angulo -90 (o 270) en coordenadas matematicas
        # La rotación de OpenGL es en sentido antihorario. 
        # Si sumamos angulo_ruleta a mid_angle, el número estará en mid_angle + angulo_ruleta.
        # Queremos que (mid_angle + angulo_ruleta) % 360 = 270 (posición superior de la ruleta)
        target_angle = 270 - mid_angle
        
        current_angle_mod = self.angulo_ruleta % 360
        distancia = target_angle - current_angle_mod
        if distancia < 0:
            distancia += 360
        distancia += 360 * 4 # 4 vueltas completas extra
        
        self.velocidad_giro = distancia * 0.015 + 0.1

    def handle_click_board(self, pos):
        x, y = pos
        if 200 <= x <= 380 and 250 <= y <= 350:
            self.apuesta_actual = {"tipo": "Color", "detalle": "rojo"}
            self.monto_apostado = 10.0 if self.capital >= 10 else self.capital
        elif 420 <= x <= 600 and 250 <= y <= 350:
            self.apuesta_actual = {"tipo": "Color", "detalle": "negro"}
            self.monto_apostado = 10.0 if self.capital >= 10 else self.capital
        elif 200 <= x <= 380 and 380 <= y <= 480:
            self.apuesta_actual = {"tipo": "ParImpar", "detalle": "par"}
            self.monto_apostado = 10.0 if self.capital >= 10 else self.capital
        elif 420 <= x <= 600 and 380 <= y <= 480:
            self.apuesta_actual = {"tipo": "ParImpar", "detalle": "impar"}
            self.monto_apostado = 10.0 if self.capital >= 10 else self.capital
            
        if self.apuesta_actual and self.monto_apostado > 0:
            if 550 <= x <= 770 and 500 <= y <= 560:
                self.girar_ruleta()

    def update_spinning(self):
        self.angulo_ruleta += self.velocidad_giro
        self.velocidad_giro *= 0.985
        
        if self.velocidad_giro < 0.1:
            self.velocidad_giro = 0
            self.state = STATE_RESULT
            
            color_res = fr.ruleta_americana[self.resultado_giro] if self.tipo_ruleta == "Americana" else fr.ruleta_europea[self.resultado_giro]
            ganancia = fr.procesar_resultado(
                self.apuesta_actual["tipo"], 
                self.apuesta_actual["detalle"], 
                self.monto_apostado, 
                self.resultado_giro, 
                color_res, 
                self.tipo_ruleta
            )
            
            if ganancia > 0:
                self.capital += (self.monto_apostado + ganancia)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.state == STATE_MENU:
                        self.handle_click_menu(event.pos)
                    elif self.state == STATE_BOARD:
                        self.handle_click_board(event.pos)
                    elif self.state == STATE_RESULT:
                        if self.capital <= 0:
                            running = False
                        else:
                            self.apuesta_anterior = self.apuesta_actual
                            self.apuesta_actual = None
                            self.monto_apostado = 0.0
                            self.state = STATE_BOARD
                            self.timer_start = pygame.time.get_ticks()
            
            if self.state == STATE_BOARD:
                time_elapsed = (pygame.time.get_ticks() - self.timer_start) // 1000
                if time_elapsed >= 15:
                    if self.apuesta_anterior and self.capital >= 10:
                        self.apuesta_actual = self.apuesta_anterior
                        self.monto_apostado = 10.0
                        self.girar_ruleta()
                    elif self.apuesta_actual and self.monto_apostado > 0:
                        self.girar_ruleta()
                    else:
                        self.timer_start = pygame.time.get_ticks()
            elif self.state == STATE_SPINNING:
                self.update_spinning()
                
            glClearColor(0.0, 0.0, 0.8, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            if self.state == STATE_MENU:
                self.draw_menu()
            elif self.state == STATE_BOARD:
                self.draw_board()
            elif self.state == STATE_SPINNING:
                self.draw_spinning()
            elif self.state == STATE_RESULT:
                self.draw_result()
                
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    RuletaGame()
