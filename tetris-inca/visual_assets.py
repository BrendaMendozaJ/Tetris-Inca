"""
Sistema de assets visuales para Tetris Inca
Maneja texturas, patrones y efectos visuales con temática andina
"""

import pygame
import math
import os
from typing import Dict, Tuple, Optional

class VisualAssets:
    """Gestor centralizado de assets visuales"""
    
    def __init__(self):
        self.textures = {}
        self.patterns = {}
        self.icons = {}
        self.animations = {}
        self.init_assets()
    
    def init_assets(self):
        """Inicializa todos los assets visuales"""
        self.create_stone_textures()
        self.create_inca_patterns()
        self.create_ui_icons()
        self.create_background_gradients()
    
    def create_stone_textures(self):
        """Crea texturas de piedra para las piezas"""
        # Textura base de piedra
        stone_base = pygame.Surface((30, 30))
        
        # Colores de piedra andina
        stone_colors = {
            'light': (120, 100, 80),
            'medium': (90, 75, 60),
            'dark': (60, 50, 40),
            'highlight': (140, 120, 100)
        }
        
        # Crear patrón de piedra con ruido
        for y in range(30):
            for x in range(30):
                # Crear variación de color basada en posición
                noise = (x * 7 + y * 11) % 40 - 20
                base_color = stone_colors['medium']
                
                # Aplicar variación
                r = max(0, min(255, base_color[0] + noise))
                g = max(0, min(255, base_color[1] + noise))
                b = max(0, min(255, base_color[2] + noise))
                
                stone_base.set_at((x, y), (r, g, b))
        
        self.textures['stone_base'] = stone_base
    
    def create_inca_patterns(self):
        """Crea patrones decorativos incas mejorados"""
        # Patrón chakana (cruz andina) mejorado
        chakana = pygame.Surface((20, 20), pygame.SRCALPHA)
        gold = (255, 215, 0)
        dark_gold = (200, 170, 0)
        
        # Dibujar chakana con más detalle
        pygame.draw.line(chakana, gold, (10, 2), (10, 18), 3)
        pygame.draw.line(chakana, gold, (2, 10), (18, 10), 3)
        pygame.draw.rect(chakana, gold, (7, 7, 6, 6))
        pygame.draw.rect(chakana, dark_gold, (8, 8, 4, 4))
        
        # Pequeños detalles en las puntas
        for x, y in [(10, 2), (10, 18), (2, 10), (18, 10)]:
            pygame.draw.circle(chakana, gold, (x, y), 2)
        
        self.patterns['chakana'] = chakana
        
        # Patrón de terrazas mejorado
        terrace = pygame.Surface((30, 10), pygame.SRCALPHA)
        earth_color = (101, 67, 33)
        light_earth = (121, 87, 53)
        
        for i in range(3):
            y = i * 3
            pygame.draw.line(terrace, earth_color, (0, y), (30, y), 2)
            pygame.draw.line(terrace, light_earth, (0, y + 1), (30, y + 1), 1)
        
        self.patterns['terrace'] = terrace
        
        # Nuevo patrón: Escalones incas
        steps = pygame.Surface((25, 25), pygame.SRCALPHA)
        step_color = (139, 69, 19)
        
        for i in range(4):
            step_y = 5 + i * 5
            step_width = 20 - i * 3
            pygame.draw.rect(steps, step_color, (2 + i, step_y, step_width, 3))
        
        self.patterns['steps'] = steps
    
    def create_ui_icons(self):
        """Crea iconos mejorados para la interfaz"""
        # Icono del sol (Inti) mejorado
        sun_icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        gold = (255, 215, 0)
        dark_gold = (200, 170, 0)
        
        # Centro del sol con gradiente
        pygame.draw.circle(sun_icon, gold, (12, 12), 8)
        pygame.draw.circle(sun_icon, dark_gold, (12, 12), 6)
        
        # Rayos del sol
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            start_x = 12 + math.cos(rad) * 10
            start_y = 12 + math.sin(rad) * 10
            end_x = 12 + math.cos(rad) * 14
            end_y = 12 + math.sin(rad) * 14
            pygame.draw.line(sun_icon, gold, (start_x, start_y), (end_x, end_y), 2)
        
        # Cara del sol
        pygame.draw.circle(sun_icon, dark_gold, (9, 9), 1)  # Ojo izquierdo
        pygame.draw.circle(sun_icon, dark_gold, (15, 9), 1)  # Ojo derecho
        pygame.draw.arc(sun_icon, dark_gold, (9, 12, 6, 4), 0, math.pi, 1)  # Sonrisa
        
        self.icons['sun'] = sun_icon
        
        # Icono quipu mejorado (para líneas)
        quipu_icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        brown = (139, 69, 19)
        light_brown = (159, 89, 39)
        
        # Cuerda principal horizontal
        pygame.draw.line(quipu_icon, brown, (2, 4), (22, 4), 3)
        
        # Líneas colgantes del quipu
        for i in range(4):
            x = 4 + i * 5
            pygame.draw.line(quipu_icon, brown, (x, 4), (x, 20), 2)
            # Nudos con diferentes tamaños
            pygame.draw.circle(quipu_icon, light_brown, (x, 8 + i), 2)
            pygame.draw.circle(quipu_icon, brown, (x, 8 + i), 1)
            pygame.draw.circle(quipu_icon, light_brown, (x, 16 - i), 2)
            pygame.draw.circle(quipu_icon, brown, (x, 16 - i), 1)
        
        self.icons['quipu'] = quipu_icon
        
        # Icono chasqui mejorado (para nivel)
        chasqui_icon = pygame.Surface((24, 24), pygame.SRCALPHA)
        green = (34, 139, 34)
        dark_green = (24, 99, 24)
        
        # Figura estilizada de chasqui corriendo
        pygame.draw.circle(chasqui_icon, green, (12, 8), 4)  # Cabeza
        pygame.draw.circle(chasqui_icon, dark_green, (12, 8), 2)  # Cara
        pygame.draw.line(chasqui_icon, green, (12, 12), (12, 18), 3)  # Cuerpo
        pygame.draw.line(chasqui_icon, green, (8, 14), (16, 14), 2)  # Brazos
        
        # Piernas en movimiento
        pygame.draw.line(chasqui_icon, green, (12, 18), (8, 22), 2)  # Pierna izq
        pygame.draw.line(chasqui_icon, green, (12, 18), (16, 20), 2)  # Pierna der
        
        # Plumas en la cabeza
        pygame.draw.line(chasqui_icon, (255, 215, 0), (10, 4), (8, 2), 2)
        pygame.draw.line(chasqui_icon, (255, 215, 0), (14, 4), (16, 2), 2)
        
        self.icons['chasqui'] = chasqui_icon
    
    def create_background_gradients(self):
        """Crea gradientes para fondos"""
        # Gradiente de terrazas andinas
        gradient = pygame.Surface((800, 600))
        
        for y in range(600):
            # Transición de cielo a tierra
            sky_ratio = max(0, min(1, (300 - y) / 300))
            earth_ratio = 1 - sky_ratio
            
            sky_color = (135, 206, 235)  # Azul cielo
            earth_color = (76, 63, 47)   # Marrón tierra
            
            r = int(sky_color[0] * sky_ratio + earth_color[0] * earth_ratio)
            g = int(sky_color[1] * sky_ratio + earth_color[1] * earth_ratio)
            b = int(sky_color[2] * sky_ratio + earth_color[2] * earth_ratio)
            
            pygame.draw.line(gradient, (r, g, b), (0, y), (800, y))
        
        self.textures['background_gradient'] = gradient
    
    def get_textured_piece_surface(self, base_color: Tuple[int, int, int], size: int = 30) -> pygame.Surface:
        """Crea una superficie texturizada para una pieza"""
        surface = pygame.Surface((size, size))
        
        # Aplicar color base
        surface.fill(base_color)
        
        # Aplicar textura de piedra
        stone_texture = self.textures['stone_base'].copy()
        
        # Mezclar colores
        for y in range(size):
            for x in range(size):
                if x < stone_texture.get_width() and y < stone_texture.get_height():
                    stone_pixel = stone_texture.get_at((x, y))
                    base_pixel = surface.get_at((x, y))
                    
                    # Mezcla aditiva suave
                    mixed_r = min(255, int(base_pixel[0] * 0.7 + stone_pixel[0] * 0.3))
                    mixed_g = min(255, int(base_pixel[1] * 0.7 + stone_pixel[1] * 0.3))
                    mixed_b = min(255, int(base_pixel[2] * 0.7 + stone_pixel[2] * 0.3))
                    
                    surface.set_at((x, y), (mixed_r, mixed_g, mixed_b))
        
        # Agregar borde de piedra
        pygame.draw.rect(surface, (40, 30, 20), (0, 0, size, size), 1)
        
        # Agregar patrón decorativo según el tamaño
        if size >= 20:
            # Alternar entre chakana y escalones
            pattern_choice = (pygame.time.get_ticks() // 1000) % 2
            if pattern_choice == 0:
                pattern = pygame.transform.scale(self.patterns['chakana'], (8, 8))
            else:
                pattern = pygame.transform.scale(self.patterns.get('steps', self.patterns['chakana']), (8, 8))
            
            surface.blit(pattern, (size//2 - 4, size//2 - 4), special_flags=pygame.BLEND_ADD)
        
        return surface

class ParticleSystem:
    """Sistema de partículas mejorado para efectos visuales"""
    
    def __init__(self):
        self.particles = []
    
    def add_sparkle(self, x: int, y: int):
        """Añade chispa dorada"""
        import random
        for _ in range(5):
            particle = {
                'x': x + random.randint(-10, 10),
                'y': y + random.randint(-10, 10),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'life': 30,
                'max_life': 30,
                'color': (255, 215, 0),
                'type': 'sparkle',
                'size': random.randint(2, 4)
            }
            self.particles.append(particle)
    
    def add_floating_particle(self, x: int, y: int):
        """Añade partícula flotante dorada"""
        import random
        particle = {
            'x': x,
            'y': y,
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-1, -0.2),
            'life': 120,
            'max_life': 120,
            'color': (255, 215, 0),
            'type': 'floating',
            'size': random.randint(3, 6)
        }
        self.particles.append(particle)
    
    def add_impact_particle(self, x: int, y: int):
        """Añade partícula de impacto"""
        import random
        particle = {
            'x': x + random.randint(-15, 15),
            'y': y + random.randint(-15, 15),
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(-4, -1),
            'life': 25,
            'max_life': 25,
            'color': (255, 140, 0),
            'type': 'impact',
            'size': random.randint(3, 7)
        }
        self.particles.append(particle)
    
    def update(self):
        """Actualiza todas las partículas"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Gravedad para partículas de impacto
            if particle['type'] == 'impact':
                particle['vy'] += 0.2
            
            # Flotación suave para partículas flotantes
            elif particle['type'] == 'floating':
                particle['vx'] += math.sin(pygame.time.get_ticks() * 0.01) * 0.02
            
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen: pygame.Surface):
        """Dibuja todas las partículas con efectos mejorados"""
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (*particle['color'], alpha)
            size = particle['size']
            
            # Crear superficie temporal con alpha
            temp_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            
            if particle['type'] == 'sparkle':
                # Estrella pequeña
                center = size
                pygame.draw.circle(temp_surface, color, (center, center), size)
                # Rayos de estrella
                for angle in range(0, 360, 90):
                    rad = math.radians(angle)
                    end_x = center + math.cos(rad) * size
                    end_y = center + math.sin(rad) * size
                    pygame.draw.line(temp_surface, color, (center, center), (end_x, end_y), 1)
            
            elif particle['type'] == 'floating':
                # Círculo con brillo
                pygame.draw.circle(temp_surface, color, (size, size), size)
                inner_color = (*particle['color'], alpha // 2)
                pygame.draw.circle(temp_surface, inner_color, (size, size), size // 2)
            
            elif particle['type'] == 'impact':
                # Fragmento angular
                points = [(size, 0), (size * 2, size), (size, size * 2), (0, size)]
                pygame.draw.polygon(temp_surface, color, points)
            
            screen.blit(temp_surface, (int(particle['x'] - size), int(particle['y'] - size)))

class AnimationManager:
    """Gestor de animaciones suaves"""
    
    def __init__(self):
        self.animations = {}
        self.time = 0
    
    def update(self):
        """Actualiza el tiempo de animación"""
        self.time = pygame.time.get_ticks()
    
    def get_pulsing_alpha(self, speed: float = 0.003) -> int:
        """Retorna alpha pulsante para efectos"""
        return int(127 + 127 * math.sin(self.time * speed))
    
    def get_floating_offset(self, amplitude: float = 5, speed: float = 0.002) -> int:
        """Retorna offset flotante para animaciones"""
        return int(amplitude * math.sin(self.time * speed))
    
    def get_rotating_angle(self, speed: float = 0.001) -> float:
        """Retorna ángulo de rotación continua"""
        return (self.time * speed) % (2 * math.pi)

# Instancia global para fácil acceso
visual_assets = VisualAssets()
particle_system = ParticleSystem()
animation_manager = AnimationManager()