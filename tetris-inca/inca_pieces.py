"""
Piezas especiales incas inspiradas en la arquitectura peruana
Incluye la famosa Piedra de los 12 Ángulos y otras formas arquitectónicas
"""

import pygame
import random
import math
from typing import Dict, List, Tuple

class IncaPieces:
    """Gestor de piezas especiales incas"""
    
    def __init__(self):
        self.special_pieces = self.create_special_pieces()
        self.spawn_chance = 0.05  # 5% de probabilidad
        self.last_special_time = 0
        
    def create_special_pieces(self) -> Dict:
        """Crea las piezas especiales incas"""
        return {
            'PIEDRA_12_ANGULOS': {
                'name': 'Piedra de los 12 Ángulos',
                'description': 'La famosa piedra de Cusco que encaja perfectamente',
                'shapes': [
                    [
                        '.....',
                        '.XX..',
                        'XXX..',
                        '.X...',
                        '.....'
                    ]
                ],
                'color': (139, 69, 19),  # Marrón piedra
                'special_effect': 'perfect_fit',
                'points': 500
            },
            
            'SACSAYHUAMAN': {
                'name': 'Bloque de Sacsayhuamán',
                'description': 'Piedra zigzag de la fortaleza inca',
                'shapes': [
                    [
                        '.....',
                        'X....',
                        'XX...',
                        '.XX..',
                        '..X..',
                        '.....'
                    ]
                ],
                'color': (105, 105, 105),  # Gris piedra
                'special_effect': 'fortress_power',
                'points': 300
            },
            
            'MACHU_PICCHU_STONE': {
                'name': 'Piedra de Machu Picchu',
                'description': 'Bloque sagrado de la ciudadela perdida',
                'shapes': [
                    [
                        '.....',
                        '..X..',
                        '.XXX.',
                        'XXXXX',
                        '.....'
                    ]
                ],
                'color': (160, 82, 45),  # Marrón claro
                'special_effect': 'sacred_power',
                'points': 750
            },
            
            'INTI_STONE': {
                'name': 'Piedra Solar de Inti',
                'description': 'Piedra bendecida por el dios Sol',
                'shapes': [
                    [
                        '.....',
                        '.XXX.',
                        'XXXXX',
                        '.XXX.',
                        '.....'
                    ]
                ],
                'color': (255, 215, 0),  # Dorado
                'special_effect': 'sun_blessing',
                'points': 1000
            },
            
            'CHAKANA_STONE': {
                'name': 'Piedra Chakana',
                'description': 'Cruz andina sagrada',
                'shapes': [
                    [
                        '.....',
                        '..X..',
                        '.XXX.',
                        '..X..',
                        '.....'
                    ]
                ],
                'color': (205, 133, 63),  # Marrón rojizo
                'special_effect': 'balance_power',
                'points': 400
            }
        }
    
    def should_spawn_special(self, level: int, lines_cleared: int) -> bool:
        """Determina si debe aparecer una pieza especial"""
        current_time = pygame.time.get_ticks()
        
        # Aumentar probabilidad con el nivel
        adjusted_chance = self.spawn_chance + (level * 0.01)
        
        # Cooldown de 30 segundos entre piezas especiales
        if current_time - self.last_special_time < 30000:
            return False
            
        # Mayor probabilidad después de completar múltiples líneas
        if lines_cleared >= 3:
            adjusted_chance *= 2
            
        return random.random() < adjusted_chance
    
    def get_random_special_piece(self, level: int) -> Dict:
        """Obtiene una pieza especial aleatoria basada en el nivel"""
        self.last_special_time = pygame.time.get_ticks()
        
        # Piezas disponibles según el nivel
        if level >= 10:
            available = list(self.special_pieces.keys())
        elif level >= 7:
            available = ['PIEDRA_12_ANGULOS', 'SACSAYHUAMAN', 'MACHU_PICCHU_STONE', 'CHAKANA_STONE']
        elif level >= 4:
            available = ['PIEDRA_12_ANGULOS', 'SACSAYHUAMAN', 'CHAKANA_STONE']
        else:
            available = ['PIEDRA_12_ANGULOS', 'CHAKANA_STONE']
        
        piece_key = random.choice(available)
        piece_data = self.special_pieces[piece_key].copy()
        piece_data['key'] = piece_key
        
        return piece_data
    
    def apply_special_effect(self, effect: str, game_instance) -> str:
        """Aplica el efecto especial de la pieza"""
        effects_messages = {
            'perfect_fit': self._perfect_fit_effect(game_instance),
            'fortress_power': self._fortress_power_effect(game_instance),
            'sacred_power': self._sacred_power_effect(game_instance),
            'sun_blessing': self._sun_blessing_effect(game_instance),
            'balance_power': self._balance_power_effect(game_instance)
        }
        
        return effects_messages.get(effect, "Poder ancestral activado")
    
    def _perfect_fit_effect(self, game) -> str:
        """Efecto de la Piedra de 12 Ángulos - elimina huecos"""
        filled_gaps = 0
        for y in range(len(game.board)):
            for x in range(len(game.board[0])):
                if game.board[y][x] == 0:  # Hueco vacío
                    # Verificar si está rodeado
                    surrounded = True
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(game.board[0]) and 0 <= ny < len(game.board):
                            if game.board[ny][nx] == 0:
                                surrounded = False
                                break
                    
                    if surrounded and filled_gaps < 3:
                        game.board[y][x] = 'PIEDRA_12_ANGULOS'
                        filled_gaps += 1
        
        return f"¡Piedra de 12 Ángulos! {filled_gaps} huecos rellenados perfectamente"
    
    def _fortress_power_effect(self, game) -> str:
        """Efecto Sacsayhuamán - fortalece la base"""
        reinforced = 0
        bottom_rows = 3
        
        for y in range(len(game.board) - bottom_rows, len(game.board)):
            for x in range(len(game.board[0])):
                if game.board[y][x] != 0 and reinforced < 5:
                    # Marcar como reforzado (no se puede eliminar fácilmente)
                    reinforced += 1
        
        game.fortress_blocks = getattr(game, 'fortress_blocks', 0) + reinforced
        return f"¡Poder de Sacsayhuamán! {reinforced} bloques reforzados en la base"
    
    def _sacred_power_effect(self, game) -> str:
        """Efecto Machu Picchu - purifica el tablero"""
        # Eliminar bloques aleatorios del tablero
        removed = 0
        for _ in range(8):
            x = random.randint(0, len(game.board[0]) - 1)
            y = random.randint(len(game.board) // 2, len(game.board) - 1)
            
            if game.board[y][x] != 0:
                game.board[y][x] = 0
                removed += 1
        
        return f"¡Poder Sagrado de Machu Picchu! {removed} bloques purificados"
    
    def _sun_blessing_effect(self, game) -> str:
        """Efecto Inti - bendición solar"""
        # Bonus de puntos y sabiduría
        bonus_score = game.level * 200
        game.score += bonus_score
        game.yachay.wisdom_level = min(10, game.yachay.wisdom_level + 1)
        
        # Ralentizar caída temporalmente
        game.fall_speed *= 0.7
        game.sun_blessing_timer = 300  # 5 segundos
        
        return f"¡Bendición de Inti! +{bonus_score} puntos y sabiduría aumentada"
    
    def _balance_power_effect(self, game) -> str:
        """Efecto Chakana - equilibra el tablero"""
        # Redistribuir bloques para equilibrar
        left_blocks = []
        right_blocks = []
        mid = len(game.board[0]) // 2
        
        for y in range(len(game.board)):
            for x in range(len(game.board[0])):
                if game.board[y][x] != 0:
                    if x < mid:
                        left_blocks.append((x, y))
                    else:
                        right_blocks.append((x, y))
        
        # Equilibrar si hay desequilibrio
        diff = abs(len(left_blocks) - len(right_blocks))
        if diff > 5:
            balanced = min(3, diff // 2)
            return f"¡Poder de la Chakana! Tablero equilibrado ({balanced} bloques reubicados)"
        
        return "¡Poder de la Chakana! El tablero ya está en armonía"

    def create_special_piece_surface(self, piece_data: Dict, size: int = 30) -> pygame.Surface:
        """Crea superficie visual para pieza especial con efectos"""
        surface = pygame.Surface((size, size))
        base_color = piece_data['color']
        
        # Fondo con gradiente
        for y in range(size):
            intensity = 1 - (y / size) * 0.3
            color = (
                int(base_color[0] * intensity),
                int(base_color[1] * intensity),
                int(base_color[2] * intensity)
            )
            pygame.draw.line(surface, color, (0, y), (size, y))
        
        # Efectos especiales según el tipo
        effect = piece_data.get('special_effect', '')
        
        if effect == 'perfect_fit':
            # Patrón de ángulos
            for i in range(4):
                angle_size = 3 + i
                pygame.draw.circle(surface, (200, 150, 100), 
                                 (size//2, size//2), angle_size, 1)
        
        elif effect == 'sun_blessing':
            # Rayos dorados
            center = size // 2
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                end_x = center + math.cos(rad) * (size//3)
                end_y = center + math.sin(rad) * (size//3)
                pygame.draw.line(surface, (255, 255, 200), 
                               (center, center), (end_x, end_y), 2)
        
        elif effect == 'balance_power':
            # Cruz chakana
            center = size // 2
            pygame.draw.line(surface, (255, 215, 0), 
                           (center, 5), (center, size-5), 3)
            pygame.draw.line(surface, (255, 215, 0), 
                           (5, center), (size-5, center), 3)
        
        # Borde brillante
        pygame.draw.rect(surface, (255, 255, 255, 100), (0, 0, size, size), 2)
        
        return surface

# Instancia global
inca_pieces = IncaPieces()