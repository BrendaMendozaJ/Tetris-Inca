import pygame
import sys
import random
import time
import math
from ai_yachay import Yachay
from visual_assets import visual_assets, particle_system, animation_manager
from inca_pieces import inca_pieces


INITIAL_FALL_SPEED = 0.5
SPEED_INCREMENT = 0.05
LINES_PER_LEVEL = 10
MAX_LEVEL = 15


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20


COLORES_INCA = {
    'FONDO': (76, 63, 47),        # Marrón tierra de fondo
    'GRID': (56, 43, 27),         # Marrón oscuro para grid
    'TEXTO': (255, 198, 89),      # Dorado para texto
    'TABLERO': (40, 61, 59),      # Verde andino oscuro
    'DORADO': (255, 215, 0),      # Color dorado para efectos
    # Colores de piezas
    'INTI_RUMI': (255, 215, 0),   # Dorado sol
    'RUMI_UCHUY': (139, 69, 19),  # Marrón tierra
    'CHAKANA': (205, 133, 63),    # Rojo inca
    'APU_RUMI': (34, 139, 34),    # Verde andino
    'MAMA_RUMI': (128, 0, 128),   # Púrpura real
    'WASI_RUMI': (255, 140, 0),   # Naranja inca
    'RUMI_HATUN': (135, 206, 235) # Azul cielo
}

PIEZAS_INCA = {
    'INTI_RUMI': [['.....',      # Pieza I - Piedra Solar
                   '.....',
                   'XXXX.',
                   '.....',
                   '.....'],
                  ['..X..',
                   '..X..',
                   '..X..',
                   '..X..',
                   '.....']],
    
    'RUMI_UCHUY': [['.....',     # Pieza O - Piedra Pequeña
                    '.XX..',
                    '.XX..',
                    '.....',
                    '.....']],
    
    'CHAKANA': [['.....',        # Pieza T - Cruz Andina
                 '.X...',
                 'XXX..',
                 '.....',
                 '.....'],
                ['.....',
                 '.X...',
                 '.XX..',
                 '.X...',
                 '.....'],
                ['.....',
                 '.....',
                 'XXX..',
                 '.X...',
                 '.....'],
                ['.....',
                 '.X...',
                 'XX...',
                 '.X...',
                 '.....']],
    
    'APU_RUMI': [['.....',       # Pieza S - Piedra Sagrada
                  '.....',
                  '.XX..',
                  'XX...',
                  '.....'],
                 ['.....',
                  'X....',
                  'XX...',
                  '.X...',
                  '.....']],
    
    'MAMA_RUMI': [['.....',      # Pieza Z - Piedra Madre
                   '.....',
                   'XX...',
                   '.XX..',
                   '.....'],
                  ['.....',
                   '.X...',
                   'XX...',
                   'X....',
                   '.....']],
    
    'WASI_RUMI': [['.....',      # Pieza J - Piedra Casa
                   'X....',
                   'XXX..',
                   '.....',
                   '.....'],
                  ['.....',
                   'XX...',
                   'X....',
                   'X....',
                   '.....'],
                  ['.....',
                   '.....',
                   'XXX..',
                   '..X..',
                   '.....'],
                  ['.....',
                   '.X...',
                   '.X...',
                   'XX...',
                   '.....']],
    
    'RUMI_HATUN': [['.....',     # Pieza L - Piedra Grande
                    '..X..',
                    'XXX..',
                    '.....',
                    '.....'],
                   ['.....',
                    'X....',
                    'X....',
                    'XX...',
                    '.....'],
                   ['.....',
                    '.....',
                    'XXX..',
                    'X....',
                    '.....'],
                   ['.....',
                    'XX...',
                    '.X...',
                    '.X...',
                    '.....']]
}

class TetrisInca:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.current_piece_type = None
        self.current_x = 0
        self.current_y = 0
        self.current_rotation = 0
        self.score = 0
        self.game_over = False
        self.fall_time = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.last_fall = pygame.time.get_ticks()
        self.game_start_time = time.time()
        
        # Sistema de niveles
        self.level = 1
        self.lines_cleared_total = 0
        self.lines_for_next_level = LINES_PER_LEVEL
        
        # Integración con Yachay
        self.yachay = Yachay()
        self.last_action_time = time.time()
        self.showing_stats = False
        self.decision_start_time = time.time()
        self.total_moves = 0
        self.perfect_drops = 0
        
        # Colores y piezas
        self.piece_colors = {
            'INTI_RUMI': COLORES_INCA['INTI_RUMI'],
            'RUMI_UCHUY': COLORES_INCA['RUMI_UCHUY'],
            'CHAKANA': COLORES_INCA['CHAKANA'],
            'APU_RUMI': COLORES_INCA['APU_RUMI'],
            'MAMA_RUMI': COLORES_INCA['MAMA_RUMI'],
            'WASI_RUMI': COLORES_INCA['WASI_RUMI'],
            'RUMI_HATUN': COLORES_INCA['RUMI_HATUN']
        }
        
        # Calcular posición del tablero
        self.board_width = GRID_SIZE * GRID_WIDTH
        self.board_height = GRID_SIZE * GRID_HEIGHT
        self.board_x = (WINDOW_WIDTH - self.board_width) // 2
        self.board_y = (WINDOW_HEIGHT - self.board_height) // 2
        
        # Cache de superficies texturizadas
        self.textured_pieces = {}
        self.init_textured_pieces()
        
        # Efectos visuales
        self.golden_glow_timer = 0
        self.day_night_cycle = 0
        
        # Sistema de piezas especiales
        self.special_piece_active = False
        self.special_piece_data = None
        self.sun_blessing_timer = 0
        self.fortress_blocks = 0
        
        self.spawn_piece()
    
    def init_textured_pieces(self):
        """Inicializa las superficies texturizadas para las piezas"""
        for piece_name, color in self.piece_colors.items():
            self.textured_pieces[piece_name] = visual_assets.get_textured_piece_surface(color, GRID_SIZE)

    def spawn_piece(self):
        """Genera una nueva pieza aleatoria o especial"""
        if self.current_piece is None:
            # Verificar si debe aparecer pieza especial
            if inca_pieces.should_spawn_special(self.level, self.lines_cleared_total):
                self.special_piece_data = inca_pieces.get_random_special_piece(self.level)
                self.current_piece_type = self.special_piece_data['key']
                self.current_piece = self.special_piece_data['shapes']
                self.special_piece_active = True
                
                # Mensaje especial
                piece_name = self.special_piece_data['name']
                self.yachay.current_advice = f"¡Pieza Especial!\n{piece_name}\n{self.special_piece_data['description']}\n– Yachay, el Amauta"
            else:
                # Pieza normal
                self.current_piece_type = random.choice(list(PIEZAS_INCA.keys()))
                self.current_piece = PIEZAS_INCA[self.current_piece_type]
                self.special_piece_active = False
                self.special_piece_data = None
            
            self.current_rotation = 0
            self.current_x = GRID_WIDTH // 2 - 2
            self.current_y = 0
            
            if self.check_collision():
                self.game_over = True
                self.show_final_stats()

    def draw_enhanced_background(self):
        """Dibuja fondo mejorado con degradado de terrazas"""
        # Fondo base con degradado
        background = visual_assets.textures['background_gradient']
        self.screen.blit(background, (0, 0))
        
        # Ciclo día/noche sutil
        self.day_night_cycle += 0.001
        night_overlay_alpha = int(30 * (1 + math.sin(self.day_night_cycle)) / 2)
        
        if night_overlay_alpha > 5:
            night_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            night_overlay.fill((0, 0, 50, night_overlay_alpha))
            self.screen.blit(night_overlay, (0, 0))
    
    def draw_board_frame(self):
        """Dibuja marco decorativo alrededor del tablero"""
        # Marco principal con degradado
        frame_rect = pygame.Rect(self.board_x - 10, self.board_y - 10, 
                                self.board_width + 20, self.board_height + 20)
        
        # Fondo del marco con textura de piedra
        frame_surface = pygame.Surface((frame_rect.width, frame_rect.height))
        frame_surface.fill((60, 50, 40))
        
        # Patrones decorativos en las esquinas
        corners = [
            (5, 5), (frame_rect.width - 25, 5),
            (5, frame_rect.height - 25), (frame_rect.width - 25, frame_rect.height - 25)
        ]
        
        for corner_x, corner_y in corners:
            frame_surface.blit(visual_assets.patterns['chakana'], (corner_x, corner_y))
        
        self.screen.blit(frame_surface, frame_rect.topleft)
        
        # Borde dorado
        pygame.draw.rect(self.screen, COLORES_INCA['DORADO'], frame_rect, 3)
    
    def draw_grid(self):
        """Dibuja la cuadrícula mejorada del tablero"""
        # Fondo del tablero con textura de terrazas
        board_surface = pygame.Surface((self.board_width, self.board_height))
        
        # Degradado de tierra a piedra
        for y in range(self.board_height):
            earth_ratio = y / self.board_height
            earth_color = (40, 61, 59)  # Verde andino oscuro
            stone_color = (76, 63, 47)  # Marrón tierra
            
            r = int(earth_color[0] * (1 - earth_ratio) + stone_color[0] * earth_ratio)
            g = int(earth_color[1] * (1 - earth_ratio) + stone_color[1] * earth_ratio)
            b = int(earth_color[2] * (1 - earth_ratio) + stone_color[2] * earth_ratio)
            
            pygame.draw.line(board_surface, (r, g, b), (0, y), (self.board_width, y))
        
        self.screen.blit(board_surface, (self.board_x, self.board_y))
        
        # Líneas de cuadrícula suaves
        for x in range(GRID_WIDTH + 1):
            line_x = self.board_x + x * GRID_SIZE
            pygame.draw.line(self.screen, COLORES_INCA['GRID'],
                           (line_x, self.board_y),
                           (line_x, self.board_y + self.board_height), 1)
        
        for y in range(GRID_HEIGHT + 1):
            line_y = self.board_y + y * GRID_SIZE
            pygame.draw.line(self.screen, COLORES_INCA['GRID'],
                           (self.board_x, line_y),
                           (self.board_x + self.board_width, line_y), 1)

    def draw_board(self):
        """Dibuja el tablero mejorado con texturas"""
        self.draw_enhanced_background()
        self.draw_board_frame()
        self.draw_grid()
        
        # Dibujar piezas fijas con texturas
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x]:
                    piece_type = self.board[y][x]
                    # Usar superficie especial para piezas incas o textura normal
                    if piece_type in inca_pieces.special_pieces:
                        piece_surface = inca_pieces.create_special_piece_surface(
                            inca_pieces.special_pieces[piece_type], GRID_SIZE
                        )
                    else:
                        piece_surface = self.textured_pieces.get(piece_type, self.textured_pieces['INTI_RUMI'])
                    
                    self.screen.blit(piece_surface,
                                  (self.board_x + x * GRID_SIZE,
                                   self.board_y + y * GRID_SIZE))
        
        # Brillo dorado si hay líneas completadas recientemente
        if self.golden_glow_timer > 0:
            self.draw_golden_glow()
            self.golden_glow_timer -= 1
        
        if self.current_piece:
            self.draw_piece()
    
    def draw_golden_glow(self):
        """Dibuja brillo dorado en el tablero"""
        glow_alpha = int(50 * (self.golden_glow_timer / 30))
        glow_surface = pygame.Surface((self.board_width, self.board_height), pygame.SRCALPHA)
        glow_surface.fill((255, 215, 0, glow_alpha))
        self.screen.blit(glow_surface, (self.board_x, self.board_y))

    def draw_piece(self):
        """Dibuja la pieza actual con efectos especiales"""
        if self.current_piece:
            piece = self.current_piece[self.current_rotation]
            time = pygame.time.get_ticks()
            
            # Usar superficie especial para piezas incas
            if self.special_piece_active and self.special_piece_data:
                piece_surface = inca_pieces.create_special_piece_surface(self.special_piece_data, GRID_SIZE)
                glow_intensity = int(50 + 30 * math.sin(time * 0.008))
            else:
                piece_surface = self.textured_pieces.get(self.current_piece_type, self.textured_pieces['INTI_RUMI'])
                glow_intensity = int(30 + 20 * math.sin(time * 0.005))
            
            for y, row in enumerate(piece):
                for x, cell in enumerate(row):
                    if cell == 'X':
                        pos_x = self.board_x + (self.current_x + x) * GRID_SIZE
                        pos_y = self.board_y + (self.current_y + y) * GRID_SIZE
                        
                        # Superficie con brillo
                        glow_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        if self.special_piece_active:
                            glow_color = (255, 215, 0, glow_intensity)
                        else:
                            base_color = self.piece_colors.get(self.current_piece_type, (255, 215, 0))
                            glow_color = (*base_color, glow_intensity)
                        glow_surface.fill(glow_color)
                        self.screen.blit(glow_surface, (pos_x, pos_y))
                        
                        # Pieza principal
                        self.screen.blit(piece_surface, (pos_x, pos_y))
                        
                        # Efectos especiales para piezas incas
                        if self.special_piece_active:
                            if time % 60 == 0:
                                particle_system.add_sparkle(pos_x + GRID_SIZE//2, pos_y + GRID_SIZE//2)
                        elif time % 180 == 0:
                            particle_system.add_sparkle(pos_x + GRID_SIZE//2, pos_y + GRID_SIZE//2)

    def move_piece(self, dx, dy):
        """Mueve la pieza actual con tracking mejorado"""
        if not self.current_piece:
            return False
            
        old_x = self.current_x
        old_y = self.current_y
        
        # Registrar tiempo de decisión
        if dx != 0 or dy != 0:
            current_time = time.time()
            self.yachay.track_decision(self.decision_start_time, current_time)
            self.decision_start_time = current_time
            self.total_moves += 1
        
        self.current_x += dx
        self.current_y += dy
        
        if self.check_collision():
            self.current_x = old_x
            self.current_y = old_y
            
            if dy > 0:
                # Registrar error si la pieza no pudo moverse hacia abajo
                if dx == 0:  # Solo si fue un movimiento natural hacia abajo
                    self.freeze_piece()
                    lines_cleared = self.clear_lines()
                    if lines_cleared:
                        advice = self.yachay.track_success(lines_cleared)
                        if advice:
                            self.yachay.current_advice = advice
                    else:
                        # Verificar equilibrio del tablero
                        balance_advice = self.yachay.check_board_balance(self.board)
                        if balance_advice:
                            self.yachay.current_advice = balance_advice
                    self.spawn_piece()
                return False
            else:
                # Registrar error de movimiento lateral
                error_advice = self.yachay.track_error()
                if error_advice and not self.yachay.current_advice:
                    self.yachay.current_advice = error_advice
        return True

    def rotate_piece(self):
        """Rota la pieza actual"""
        if not self.current_piece:
            return
            
        old_rotation = self.current_rotation
        self.current_rotation = (self.current_rotation + 1) % len(self.current_piece)
        
        if self.check_collision():
            self.current_rotation = old_rotation

    def check_collision(self):
        """Verifica si hay colisión"""
        if not self.current_piece:
            return False
            
        piece = self.current_piece[self.current_rotation]
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == 'X':
                    board_x = self.current_x + x
                    board_y = self.current_y + y
                    
                    if (board_x < 0 or board_x >= GRID_WIDTH or
                        board_y >= GRID_HEIGHT or
                        (board_y >= 0 and self.board[board_y][board_x])):
                        return True
        return False

    def freeze_piece(self):
        """Fija la pieza actual en el tablero"""
        if not self.current_piece:
            return
            
        piece = self.current_piece[self.current_rotation]
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell == 'X':
                    if 0 <= self.current_y + y < GRID_HEIGHT and 0 <= self.current_x + x < GRID_WIDTH:
                        self.board[self.current_y + y][self.current_x + x] = self.current_piece_type
        
        # Aplicar efecto especial si es pieza inca
        if self.special_piece_active and self.special_piece_data:
            effect_message = inca_pieces.apply_special_effect(
                self.special_piece_data['special_effect'], self
            )
            self.score += self.special_piece_data['points']
            self.yachay.current_advice = effect_message + "\n– Yachay, el Amauta"
            
            # Efectos visuales para pieza especial
            for _ in range(20):
                import random
                px = random.randint(self.board_x, self.board_x + self.board_width)
                py = random.randint(self.board_y, self.board_y + self.board_height)
                particle_system.add_floating_particle(px, py)
        
        self.current_piece = None
        self.special_piece_active = False
        self.special_piece_data = None

    def clear_lines(self):
        """Elimina las líneas completas con efecto Inti Raymi mejorado"""
        lines_to_clear = []
        y = GRID_HEIGHT - 1
        lines_cleared = 0
        
        # Identificar líneas completas
        while y >= 0:
            if all(self.board[y]):
                lines_to_clear.append(y)
                lines_cleared += 1
            y -= 1
        
        # Efecto Inti Raymi mejorado con destellos como rayos de sol
        if lines_to_clear:
            self.golden_glow_timer = 60  # Activar brillo dorado
            
            for flash in range(3):
                # Dibujar todo el tablero primero
                self.draw_enhanced_background()
                self.draw_board_frame()
                self.draw_grid()
                
                # Efecto de destellos dorados como rayos de sol
                for y in lines_to_clear:
                    for x in range(GRID_WIDTH):
                        pos_x = self.board_x + x * GRID_SIZE
                        pos_y = self.board_y + y * GRID_SIZE
                        
                        # Destello principal
                        gold_intensity = 255 - (flash * 40)
                        gold_color = (gold_intensity, gold_intensity - 20, 0)
                        
                        # Superficie con brillo
                        glow_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                        glow_surface.fill((*gold_color, 200))
                        self.screen.blit(glow_surface, (pos_x, pos_y))
                        
                        # Rayos de sol desde el centro
                        center_x = pos_x + GRID_SIZE // 2
                        center_y = pos_y + GRID_SIZE // 2
                        
                        for angle in range(0, 360, 45):
                            rad = math.radians(angle)
                            end_x = center_x + math.cos(rad) * 15
                            end_y = center_y + math.sin(rad) * 15
                            pygame.draw.line(self.screen, COLORES_INCA['DORADO'], 
                                           (center_x, center_y), (end_x, end_y), 2)
                        
                        # Partículas de chispas
                        particle_system.add_sparkle(center_x, center_y)
                
                # Dibujar UI
                self.draw_enhanced_ui()
                pygame.display.flip()
                pygame.time.wait(200)
                
                # Pausa entre destellos
                if flash < 2:
                    self.draw_enhanced_background()
                    self.draw_board()
                    self.draw_enhanced_ui()
                    pygame.display.flip()
                    pygame.time.wait(150)
        
        # Eliminar líneas y actualizar tablero
        for y in sorted(lines_to_clear, reverse=True):
            for y2 in range(y, 0, -1):
                self.board[y2] = self.board[y2-1][:]
            self.board[0] = [0] * GRID_WIDTH
        
        if lines_cleared > 0:
            # Actualizar puntuación con bonus por nivel
            self.score += (100 * lines_cleared) * lines_cleared * self.level
            
            # Actualizar total de líneas y verificar nivel
            self.lines_cleared_total += lines_cleared
            if self.lines_cleared_total >= self.lines_for_next_level:
                self.level_up()
                
        return lines_cleared

    def level_up(self):
        """Aumenta el nivel y la dificultad"""
        if self.level < MAX_LEVEL:
            self.level += 1
            self.lines_for_next_level = self.lines_cleared_total + LINES_PER_LEVEL
            self.fall_speed = max(0.1, INITIAL_FALL_SPEED - (SPEED_INCREMENT * self.level))
            
            # Mensaje de nivel alcanzado
            self.yachay.current_advice = f"¡Has alcanzado el nivel {self.level}!\nLa sabiduría de los ancestros fluye en ti.\n– Yachay, el Amauta"

    def show_final_stats(self):
        """Muestra la pantalla de estadísticas finales sin superposiciones"""
        self.showing_stats = True
        
        # Actualizar estadísticas finales
        self.yachay.stats['total_score'] = self.score
        self.yachay.stats['play_time'] = time.time() - self.game_start_time
        stats = self.yachay.get_final_stats()
        
        # Fondo con patrón inca
        self.screen.fill(COLORES_INCA['FONDO'])
        
        # Fondo semi-transparente centrado
        stats_bg_width, stats_bg_height = 500, 450
        stats_bg_x = (WINDOW_WIDTH - stats_bg_width) // 2
        stats_bg_y = (WINDOW_HEIGHT - stats_bg_height) // 2
        
        stats_bg = pygame.Surface((stats_bg_width, stats_bg_height), pygame.SRCALPHA)
        stats_bg.fill((40, 61, 59, 230))
        pygame.draw.rect(stats_bg, COLORES_INCA['DORADO'], (0, 0, stats_bg_width, stats_bg_height), 3)
        
        # Patrones decorativos en esquinas
        corners = [(10, 10), (stats_bg_width-30, 10), (10, stats_bg_height-30), (stats_bg_width-30, stats_bg_height-30)]
        for corner_x, corner_y in corners:
            stats_bg.blit(visual_assets.patterns['chakana'], (corner_x, corner_y))
        
        self.screen.blit(stats_bg, (stats_bg_x, stats_bg_y))
        
        # Título
        font_titulo = pygame.font.Font(None, 48)
        font_stats = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)
        
        titulo = font_titulo.render("ESTADÍSTICAS FINALES", True, COLORES_INCA['DORADO'])
        titulo_x = stats_bg_x + (stats_bg_width - titulo.get_width()) // 2
        self.screen.blit(titulo, (titulo_x, stats_bg_y + 30))
        
        # Línea decorativa
        line_y = stats_bg_y + 80
        pygame.draw.line(self.screen, COLORES_INCA['DORADO'], 
                        (stats_bg_x + 50, line_y), (stats_bg_x + stats_bg_width - 50, line_y), 2)
        
        # Estadísticas en una sola columna centrada
        y_pos = line_y + 30
        stats_items = list(stats.items())
        
        for key, value in stats_items:
            # Etiqueta y valor en la misma línea
            stat_text = f"{key}: {value}"
            stat_surface = font_stats.render(stat_text, True, COLORES_INCA['TEXTO'])
            stat_x = stats_bg_x + (stats_bg_width - stat_surface.get_width()) // 2
            self.screen.blit(stat_surface, (stat_x, y_pos))
            y_pos += 30
        
        # Mensaje de Yachay
        y_pos += 20
        mensaje_yachay = "¡Has completado tu jornada en el Tetris Inca!"
        yachay_text = font_stats.render(mensaje_yachay, True, COLORES_INCA['DORADO'])
        yachay_x = stats_bg_x + (stats_bg_width - yachay_text.get_width()) // 2
        self.screen.blit(yachay_text, (yachay_x, y_pos))
        
        firma = font_small.render("– Yachay, el Amauta", True, COLORES_INCA['TEXTO'])
        firma_x = stats_bg_x + (stats_bg_width - firma.get_width()) // 2
        self.screen.blit(firma, (firma_x, y_pos + 25))
        
        # Instrucciones
        y_pos += 60
        instrucciones = ["ESPACIO: Jugar de nuevo", "ESC: Salir del juego"]
        
        for instruccion in instrucciones:
            inst_surface = font_small.render(instruccion, True, COLORES_INCA['TEXTO'])
            inst_x = stats_bg_x + (stats_bg_width - inst_surface.get_width()) // 2
            self.screen.blit(inst_surface, (inst_x, y_pos))
            y_pos += 22
        
        pygame.display.flip()

    def update(self):
        """Actualiza el estado del juego"""
        if not self.game_over:
            current_time = pygame.time.get_ticks()
            
            # La velocidad ahora se basa en el nivel actual
            current_speed = self.fall_speed * 1000
            
            if current_time - self.last_fall > current_speed:
                self.move_piece(0, 1)
                self.last_fall = current_time
            
            # Actualizar estadísticas
            self.yachay.update_stats(time.time())

    def draw_enhanced_ui(self):
        """Dibuja la interfaz de usuario mejorada sin superposiciones"""
        font = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 20)
        
        # Panel de estadísticas (lado izquierdo)
        stats_panel_width, stats_panel_height = 200, 160
        stats_x, stats_y = 15, 15
        
        # Fondo del panel de estadísticas
        stats_bg = pygame.Surface((stats_panel_width, stats_panel_height), pygame.SRCALPHA)
        stats_bg.fill((40, 61, 59, 220))
        pygame.draw.rect(stats_bg, COLORES_INCA['DORADO'], (0, 0, stats_panel_width, stats_panel_height), 2)
        
        # Patrón decorativo en esquina superior
        stats_bg.blit(visual_assets.patterns['chakana'], (5, 5))
        self.screen.blit(stats_bg, (stats_x, stats_y))
        
        # Información compacta con iconos
        y_pos = stats_y + 25
        
        # Puntuación
        self.screen.blit(visual_assets.icons['sun'], (stats_x + 10, y_pos))
        score_text = font.render(f'{self.score:,}', True, COLORES_INCA['DORADO'])
        self.screen.blit(score_text, (stats_x + 35, y_pos + 2))
        y_pos += 30
        
        # Nivel
        self.screen.blit(visual_assets.icons['chasqui'], (stats_x + 10, y_pos))
        level_text = font.render(f'Nivel {self.level}', True, COLORES_INCA['TEXTO'])
        self.screen.blit(level_text, (stats_x + 35, y_pos + 2))
        y_pos += 30
        
        # Líneas
        self.screen.blit(visual_assets.icons['quipu'], (stats_x + 10, y_pos))
        lines_text = font.render(f'Líneas: {self.lines_cleared_total}', True, COLORES_INCA['TEXTO'])
        self.screen.blit(lines_text, (stats_x + 35, y_pos + 2))
        y_pos += 35
        
        # Barra de sabiduría compacta
        self.draw_wisdom_bar(stats_x + 10, y_pos, stats_panel_width - 20)
        
        # Panel de consejos (parte inferior, centrado)
        advice_panel_width = min(600, WINDOW_WIDTH - 40)
        advice_x = (WINDOW_WIDTH - advice_panel_width) // 2
        advice_y = WINDOW_HEIGHT - 120
        
        # Renderizar consejo de Yachay en posición fija
        advice_font = pygame.font.Font(None, 18)
        self.yachay.render_advice_compact(self.screen, advice_font, (advice_x, advice_y), advice_panel_width)
    
    def draw_wisdom_bar(self, x: int, y: int, width: int):
        """Dibuja barra de progreso de sabiduría compacta"""
        bar_height = 12
        wisdom_ratio = min(1.0, self.yachay.wisdom_level / 10)
        
        # Texto de sabiduría encima de la barra
        wisdom_text = pygame.font.Font(None, 16).render(
            f'Sabiduría: {int(self.yachay.wisdom_level)}/10', 
            True, COLORES_INCA['DORADO']
        )
        self.screen.blit(wisdom_text, (x, y - 18))
        
        # Fondo de la barra
        bar_bg = pygame.Rect(x, y, width, bar_height)
        pygame.draw.rect(self.screen, (60, 50, 40), bar_bg)
        pygame.draw.rect(self.screen, COLORES_INCA['DORADO'], bar_bg, 1)
        
        # Relleno de progreso
        if wisdom_ratio > 0:
            fill_width = int((width - 2) * wisdom_ratio)
            fill_rect = pygame.Rect(x + 1, y + 1, fill_width, bar_height - 2)
            pygame.draw.rect(self.screen, COLORES_INCA['DORADO'], fill_rect)
    
    def draw(self):
        """Dibuja todos los elementos del juego"""
        if self.showing_stats:
            return
            
        self.draw_board()
        self.draw_enhanced_ui()
        
        # Dibujar partículas
        particle_system.draw(self.screen)
        
        if self.game_over and not self.showing_stats:
            self.show_final_stats()
        
        pygame.display.flip()

    def reset_game(self):
        """Reinicia el juego con estadísticas mejoradas"""
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.score = 0
        self.level = 1
        self.lines_cleared_total = 0
        self.lines_for_next_level = LINES_PER_LEVEL
        self.fall_speed = INITIAL_FALL_SPEED
        self.game_over = False
        self.showing_stats = False
        self.game_start_time = time.time()
        self.decision_start_time = time.time()
        self.total_moves = 0
        self.perfect_drops = 0
        self.yachay = Yachay()
        self.spawn_piece()
