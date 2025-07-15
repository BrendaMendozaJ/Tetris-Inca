import pygame
import sys
import math
from game import TetrisInca, WINDOW_WIDTH, WINDOW_HEIGHT, COLORES_INCA
from visual_assets import visual_assets, animation_manager, particle_system

def create_stone_text(text: str, size: int, color: tuple) -> pygame.Surface:
    """Crea texto con efecto de piedra tallada"""
    font = pygame.font.Font(None, size)
    
    # Texto base
    text_surface = font.render(text, True, color)
    
    # Crear superficie con borde para efecto de relieve
    bordered_surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4), pygame.SRCALPHA)
    
    # Sombra (efecto de profundidad)
    shadow_color = (max(0, color[0] - 60), max(0, color[1] - 60), max(0, color[2] - 60))
    shadow_text = font.render(text, True, shadow_color)
    bordered_surface.blit(shadow_text, (2, 2))
    
    # Texto principal
    bordered_surface.blit(text_surface, (0, 0))
    
    return bordered_surface

def draw_mountain_background(screen: pygame.Surface):
    """Dibuja fondo de montañas andinas estilizado con efectos mejorados"""
    time = pygame.time.get_ticks()
    
    # Gradiente de cielo con variación temporal sutil
    for y in range(WINDOW_HEIGHT // 2):
        sky_intensity = 1 - (y / (WINDOW_HEIGHT // 2))
        # Variación sutil del color del cielo
        time_variation = 10 * math.sin(time * 0.0005)
        sky_color = (
            int(135 * sky_intensity + 76 * (1 - sky_intensity) + time_variation),
            int(206 * sky_intensity + 63 * (1 - sky_intensity) + time_variation * 0.5),
            int(235 * sky_intensity + 47 * (1 - sky_intensity))
        )
        pygame.draw.line(screen, sky_color, (0, y), (WINDOW_WIDTH, y))
    
    # Montañas con múltiples capas para profundidad
    # Montañas de fondo (más claras)
    back_mountains = [
        (0, WINDOW_HEIGHT // 2 + 20),
        (200, WINDOW_HEIGHT // 3 + 30),
        (400, WINDOW_HEIGHT // 2 - 20),
        (WINDOW_WIDTH, WINDOW_HEIGHT // 3 + 40),
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        (0, WINDOW_HEIGHT)
    ]
    pygame.draw.polygon(screen, (80, 70, 60), back_mountains)
    
    # Montañas principales
    mountain_points = [
        (0, WINDOW_HEIGHT // 2),
        (150, WINDOW_HEIGHT // 3),
        (300, WINDOW_HEIGHT // 2 - 50),
        (450, WINDOW_HEIGHT // 4),
        (600, WINDOW_HEIGHT // 2 - 30),
        (WINDOW_WIDTH, WINDOW_HEIGHT // 3),
        (WINDOW_WIDTH, WINDOW_HEIGHT),
        (0, WINDOW_HEIGHT)
    ]
    pygame.draw.polygon(screen, (60, 50, 40), mountain_points)
    
    # Terrazas animadas con brillo sutil
    for i in range(3):
        y_level = WINDOW_HEIGHT // 2 + i * 40
        brightness = int(20 * math.sin(time * 0.002 + i))
        terrace_color = (101 + brightness, 67 + brightness//2, 33)
        pygame.draw.line(screen, terrace_color, (0, y_level), (WINDOW_WIDTH, y_level), 2)
    
    # Nubes flotantes ocasionales
    if time % 8000 < 4000:  # Aparecen cada 8 segundos por 4 segundos
        cloud_x = (time % 4000) // 10
        draw_stylized_cloud(screen, cloud_x, 100)
        draw_stylized_cloud(screen, cloud_x - 200, 150)

def draw_stylized_cloud(screen: pygame.Surface, x: int, y: int):
    """Dibuja nubes estilizadas andinas"""
    cloud_color = (220, 220, 230, 100)
    cloud_surface = pygame.Surface((80, 30), pygame.SRCALPHA)
    
    # Círculos superpuestos para formar nube
    pygame.draw.circle(cloud_surface, cloud_color, (20, 20), 15)
    pygame.draw.circle(cloud_surface, cloud_color, (35, 15), 18)
    pygame.draw.circle(cloud_surface, cloud_color, (50, 20), 12)
    pygame.draw.circle(cloud_surface, cloud_color, (60, 18), 10)
    
    screen.blit(cloud_surface, (x % (WINDOW_WIDTH + 100), y))

def draw_animated_sun(screen: pygame.Surface, x: int, y: int):
    """Dibuja sol Inti animado con efectos mejorados"""
    time = pygame.time.get_ticks()
    
    # Pulsación suave
    pulse = 1 + 0.1 * math.sin(time * 0.003)
    base_radius = int(25 * pulse)
    
    # Halo exterior con gradiente
    for i in range(5):
        halo_radius = base_radius + 10 + i * 3
        halo_alpha = 30 - i * 5
        halo_surface = pygame.Surface((halo_radius * 2, halo_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(halo_surface, (255, 215, 0, halo_alpha), (halo_radius, halo_radius), halo_radius)
        screen.blit(halo_surface, (x - halo_radius, y - halo_radius))
    
    # Sol principal con gradiente
    sun_color = (255, 215, 0)
    pygame.draw.circle(screen, sun_color, (x, y), base_radius)
    
    # Rayos principales animados
    for angle in range(0, 360, 30):
        animated_angle = angle + time * 0.05
        rad = math.radians(animated_angle)
        
        start_x = x + math.cos(rad) * (base_radius + 5)
        start_y = y + math.sin(rad) * (base_radius + 5)
        end_x = x + math.cos(rad) * (base_radius + 15)
        end_y = y + math.sin(rad) * (base_radius + 15)
        
        pygame.draw.line(screen, sun_color, (start_x, start_y), (end_x, end_y), 3)
    
    # Rayos secundarios más pequeños
    for angle in range(15, 360, 30):
        animated_angle = angle - time * 0.03
        rad = math.radians(animated_angle)
        
        start_x = x + math.cos(rad) * (base_radius + 3)
        start_y = y + math.sin(rad) * (base_radius + 3)
        end_x = x + math.cos(rad) * (base_radius + 8)
        end_y = y + math.sin(rad) * (base_radius + 8)
        
        pygame.draw.line(screen, (255, 235, 100), (start_x, start_y), (end_x, end_y), 1)
    
    # Cara del sol Inti
    eye_offset = 8
    pygame.draw.circle(screen, (200, 150, 0), (x - eye_offset, y - 5), 3)
    pygame.draw.circle(screen, (200, 150, 0), (x + eye_offset, y - 5), 3)
    
    # Sonrisa
    smile_points = [(x - 8, y + 5), (x, y + 10), (x + 8, y + 5)]
    pygame.draw.lines(screen, (200, 150, 0), False, smile_points, 2)
    
    # Brillo interior
    inner_color = (255, 255, 200, 120)
    inner_surface = pygame.Surface((base_radius * 2, base_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(inner_surface, inner_color, (base_radius, base_radius), base_radius - 5)
    screen.blit(inner_surface, (x - base_radius, y - base_radius))

def show_title_screen(screen):
    """Muestra la pantalla de título con mejor organización visual"""
    clock = pygame.time.Clock()
    
    # Esperar input con animaciones
    waiting = True
    while waiting:
        # Actualizar animaciones
        animation_manager.update()
        particle_system.update()
        
        # Fondo artístico
        draw_mountain_background(screen)
        
        # Sol animado
        draw_animated_sun(screen, WINDOW_WIDTH - 100, 80)
        
        # Panel central para contenido
        panel_width, panel_height = 600, 400
        panel_x = (WINDOW_WIDTH - panel_width) // 2
        panel_y = (WINDOW_HEIGHT - panel_height) // 2 - 20
        
        # Fondo del panel principal
        panel_bg = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_bg.fill((40, 61, 59, 200))
        pygame.draw.rect(panel_bg, COLORES_INCA['DORADO'], (0, 0, panel_width, panel_height), 3)
        
        # Patrones decorativos en esquinas del panel
        corners = [(10, 10), (panel_width-30, 10), (10, panel_height-30), (panel_width-30, panel_height-30)]
        for corner_x, corner_y in corners:
            panel_bg.blit(visual_assets.patterns['chakana'], (corner_x, corner_y))
        
        screen.blit(panel_bg, (panel_x, panel_y))
        
        # Título con efecto de piedra
        titulo_surface = create_stone_text("TETRIS INCA", 64, COLORES_INCA['DORADO'])
        titulo_y = panel_y + 30 + animation_manager.get_floating_offset(3, 0.001)
        titulo_x = panel_x + (panel_width - titulo_surface.get_width()) // 2
        screen.blit(titulo_surface, (titulo_x, titulo_y))
        
        # Subtítulo
        subtitulo_surface = create_stone_text("El Puzzle de Machu Picchu", 32, COLORES_INCA['TEXTO'])
        subtitulo_x = panel_x + (panel_width - subtitulo_surface.get_width()) // 2
        screen.blit(subtitulo_surface, (subtitulo_x, titulo_y + 70))
        
        # Sección de controles organizada
        font_titulo_seccion = pygame.font.Font(None, 28)
        font_controles = pygame.font.Font(None, 22)
        
        controles_y = titulo_y + 130
        
        # Título de controles
        controles_titulo = font_titulo_seccion.render("CONTROLES:", True, COLORES_INCA['DORADO'])
        controles_titulo_x = panel_x + (panel_width - controles_titulo.get_width()) // 2
        screen.blit(controles_titulo, (controles_titulo_x, controles_y))
        
        # Lista de controles en dos columnas
        controles_izq = [
            "LEFT/RIGHT : Mover pieza",
            "UP : Rotar pieza",
            "DOWN : Bajar rápido"
        ]
        
        controles_der = [
            "ESPACIO : Caída instantánea",
            "ESC : Salir del juego",
            ""
        ]
        
        controles_y += 35
        col_izq_x = panel_x + 80
        col_der_x = panel_x + 320
        
        for i, (izq, der) in enumerate(zip(controles_izq, controles_der)):
            y_pos = controles_y + i * 25
            
            # Columna izquierda
            if izq:
                texto_izq = font_controles.render(izq, True, COLORES_INCA['TEXTO'])
                screen.blit(texto_izq, (col_izq_x, y_pos))
            
            # Columna derecha
            if der:
                texto_der = font_controles.render(der, True, COLORES_INCA['TEXTO'])
                screen.blit(texto_der, (col_der_x, y_pos))
        
        # Botón "Presiona ENTER" con pulsación
        enter_y = panel_y + panel_height - 60
        enter_alpha = animation_manager.get_pulsing_alpha(0.005)
        enter_color = (*COLORES_INCA['DORADO'], min(255, enter_alpha))
        
        enter_bg = pygame.Surface((300, 35), pygame.SRCALPHA)
        enter_bg.fill(enter_color)
        enter_bg_x = panel_x + (panel_width - 300) // 2
        screen.blit(enter_bg, (enter_bg_x, enter_y))
        
        enter_text = font_titulo_seccion.render("Presiona ENTER para comenzar", True, COLORES_INCA['DORADO'])
        enter_text_x = panel_x + (panel_width - enter_text.get_width()) // 2
        screen.blit(enter_text, (enter_text_x, enter_y + 8))
        
        # Efectos de partículas mejorados
        current_time = pygame.time.get_ticks()
        
        # Chispas del sol
        if current_time % 60 == 0:
            particle_system.add_sparkle(WINDOW_WIDTH - 100, 80)
        
        # Partículas flotantes doradas ocasionales
        if current_time % 180 == 0:
            import random
            for _ in range(3):
                px = random.randint(50, WINDOW_WIDTH - 50)
                py = random.randint(50, WINDOW_HEIGHT // 2)
                particle_system.add_floating_particle(px, py)
        
        particle_system.draw(screen)
        
        # Efecto de brillo en el título
        if current_time % 120 < 60:
            glow_surface = pygame.Surface((panel_width, 100), pygame.SRCALPHA)
            glow_alpha = int(30 * math.sin(current_time * 0.01))
            glow_surface.fill((255, 215, 0, abs(glow_alpha)))
            screen.blit(glow_surface, (panel_x, titulo_y - 10))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    # Inicialización de Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Configuración de la ventana con icono
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("🏛️ TETRIS INCA: El Puzzle de Machu Picchu ☀️")
    
    # Crear icono simple para la ventana
    icon_surface = pygame.Surface((32, 32))
    icon_surface.fill((255, 215, 0))
    pygame.draw.circle(icon_surface, (200, 150, 0), (16, 16), 12)
    pygame.display.set_icon(icon_surface)
    
    # Importar time para las funcionalidades mejoradas
    import time
    
    # Mostrar pantalla de título
    show_title_screen(screen)
    
    # Game loop principal
    while True:
        # Crear nueva instancia del juego
        game = TetrisInca(screen)
        clock = pygame.time.Clock()
        
        # Loop del juego
        while True:
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    if game.game_over:
                        if event.key == pygame.K_SPACE:
                            # Reiniciar juego
                            game.reset_game()
                            continue
                    else:
                        # Registrar tiempo de decisión para Yachay
                        game.decision_start_time = time.time()
                        
                        if event.key == pygame.K_LEFT:
                            game.move_piece(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            game.move_piece(1, 0)
                        elif event.key == pygame.K_DOWN:
                            game.move_piece(0, 1)
                        elif event.key == pygame.K_UP:
                            game.rotate_piece()
                            # Registrar patrón de rotación
                            game.yachay.track_rotation(game.current_rotation * 90)
                        elif event.key == pygame.K_SPACE:
                            # Caída rápida con efectos visuales espectaculares
                            drops = 0
                            while game.move_piece(0, 1):
                                drops += 1
                            
                            # Efectos de impacto mejorados
                            if drops > 0:
                                impact_x = game.board_x + game.current_x * 30 + 15
                                impact_y = game.board_y + game.current_y * 30 + 15
                                
                                # Partículas de impacto
                                for _ in range(12):
                                    particle_system.add_impact_particle(impact_x, impact_y)
                                
                                # Ondas de choque
                                for wave_size in [20, 35, 50]:
                                    wave_surface = pygame.Surface((wave_size * 2, wave_size * 2), pygame.SRCALPHA)
                                    pygame.draw.circle(wave_surface, (255, 140, 0, 80), (wave_size, wave_size), wave_size, 3)
                                    screen.blit(wave_surface, (impact_x - wave_size, impact_y - wave_size))
                                
                                game.perfect_drops += 1
                                pygame.display.flip()
                                pygame.time.wait(100)
            
            # Actualizar estado del juego
            game.update()
            
            # Actualizar sistemas visuales
            animation_manager.update()
            particle_system.update()
            
            # Dibujar
            game.draw()
            
            # Control de FPS
            clock.tick(60)
            
            # Manejo especial para pantalla de estadísticas
            if game.game_over and game.showing_stats:
                stats_events = pygame.event.get()
                for event in stats_events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_SPACE:
                            # Volver al menú principal
                            show_title_screen(screen)
                            break
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    main()


