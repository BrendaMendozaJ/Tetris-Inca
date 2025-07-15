import time
import random
from collections import deque
import pygame

class Yachay:
    def __init__(self):
        self.decision_times = deque(maxlen=10)
        self.rotation_patterns = {0: 0, 90: 0, 180: 0, 270: 0}
        self.errors = 0
        self.consecutive_errors = 0
        self.successful_placements = 0
        self.last_action_time = time.time()
        self.skill_level = 0
        self.wisdom_level = 0
        self.current_advice = ""
        self.board_balance_warnings = 0
        self.last_balance_check = 0
        
        self.historical_facts = [
            "Los incas construían sus templos sin usar mortero entre las piedras.",
            "Machu Picchu fue construido siguiendo los patrones del movimiento solar.",
            "Las terrazas agrícolas incas aún funcionan después de 500 años.",
            "Los incas usaban un sistema de nudos llamado quipu para contar.",
            "La piedra de los 12 ángulos en Cusco es una obra maestra de precisión.",
            "Los chasquis podían llevar mensajes a través de los Andes en días.",
            "Sacsayhuamán fue construido con bloques de piedra de hasta 125 toneladas.",
            "Los incas crearon más de 39,000 km de caminos en terreno montañoso.",
            "El Qhapaq Ñan conectaba todo el imperio Inca.",
            "Los incas cultivaban en terrazas a más de 3,000 metros de altura."
        ]

        self.frases_sabiduria = {
            'inicio': [
                "Bienvenido al camino del Tetris Inca, donde cada pieza es sagrada.",
                "Como los antiguos maestros, construirás tu legado piedra a piedra.",
                "Que Inti ilumine tus decisiones en este desafío."
            ],
            'error': [
                "La paciencia es el camino del sabio. Como los chasquis, aprende del camino.",
                "Cada error es una piedra que nos enseña a construir mejor.",
                "Los Apus nos recuerdan que la perseverancia es la base del éxito."
            ],
            'exito': [
                "¡Excelente! Una terraza digna de Machu Picchu.",
                "Construyes con la precisión de los maestros de Sacsayhuamán.",
                "¡Pachacútec estaría orgulloso de tu destreza!"
            ],
            'mejora': [
                "Tu habilidad crece como el maíz en el valle sagrado.",
                "Las piedras encuentran su lugar, como en los muros incas.",
                "Tu sabiduría en el juego florece como la cantuta."
            ],
            'consejo': [
                "Observa el patrón como los antiguos astrónomos de Machu Picchu.",
                "Planifica tus movimientos como los arquitectos de Ollantaytambo.",
                "Como el cóndor, mira el panorama completo antes de decidir."
            ],
            'desequilibrio': [
                "Como las terrazas de Moray, busca el equilibrio en tu construcción.",
                "Las piedras deben distribuirse como las estrellas en el cielo andino.",
                "Un muro inclinado pronto caerá. Nivela tu construcción."
            ],
            'motivacion': [
                "Los grandes maestros incas también comenzaron aprendiendo.",
                "La persistencia es el camino del sabio constructor.",
                "Cada error nos acerca más a la perfección de Sacsayhuamán."
            ]
        }
        
        self.stats = {
            'total_score': 0,
            'lines_cleared': 0,
            'avg_decision_time': 0,
            'total_errors': 0,
            'perfect_placements': 0,
            'play_time': 0
        }
        
        self.init_music()
        
        self.current_advice = random.choice(self.frases_sabiduria['inicio']) + "\n– Yachay, el Amauta"

    def track_decision(self, start_time, end_time):
        """Registra el tiempo de decisión del jugador"""
        decision_time = end_time - start_time
        self.decision_times.append(decision_time)
        return self.analyze_decision_speed()

    def track_rotation(self, rotation_angle):
        """Registra patrones de rotación"""
        self.rotation_patterns[rotation_angle] += 1

    def track_error(self):
        """Registra un error y genera consejo motivacional"""
        self.errors += 1
        self.consecutive_errors += 1
        self.update_skill_level()
        
        if self.consecutive_errors >= 3:
            self.consecutive_errors = 0
            motivation = random.choice(self.frases_sabiduria['motivacion'])
            guidance = random.choice(self.frases_sabiduria['consejo'])
            return f"🏔️ Palabras del Amauta:\n{motivation}\n\n💡 Consejo Ancestral:\n{guidance}\n– Yachay, el Amauta"
        
        return random.choice(self.frases_sabiduria['error']) + "\n– Yachay, el Amauta"

    def track_success(self, lines_cleared):
        """Registra un éxito y genera celebración con datos históricos"""
        self.consecutive_errors = 0
        self.successful_placements += 1
        self.stats['lines_cleared'] += lines_cleared
        
        if lines_cleared > 0:
            self.wisdom_level = min(10, self.wisdom_level + 0.5)
            historical_fact = random.choice(self.historical_facts)
            celebration = random.choice(self.frases_sabiduria['exito'])
            return f"{celebration}\n\n📜 Sabiduría Ancestral:\n{historical_fact}\n– Yachay, el Amauta"
        return None

    def analyze_decision_speed(self):
        """Analiza la velocidad de decisión del jugador"""
        if len(self.decision_times) < 5:
            return None
            
        avg_time = sum(self.decision_times) / len(self.decision_times)
        if avg_time > 2.0: 
            return random.choice(self.frases_sabiduria['consejo'])
        return None

    def analyze_board_balance(self, board):
        """Analiza el equilibrio del tablero y detecta acumulación lateral"""
        left_blocks = 0
        right_blocks = 0
        mid = len(board[0]) // 2
        
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x]:
                    if x < mid:
                        left_blocks += 1
                    else:
                        right_blocks += 1
        
        total_blocks = left_blocks + right_blocks
        if total_blocks > 10: 
            imbalance_ratio = abs(left_blocks - right_blocks) / total_blocks
            
            if imbalance_ratio > 0.6: 
                self.board_balance_warnings += 1
                if self.board_balance_warnings >= 2:
                    self.board_balance_warnings = 0
                    side = "izquierdo" if left_blocks > right_blocks else "derecho"
                    return f"Detectas demasiados bloques en el lado {side}.\n{random.choice(self.frases_sabiduria['desequilibrio'])}\n– Yachay, el Amauta"
        return None

    def update_skill_level(self):
        """Actualiza el nivel de habilidad del jugador"""
        success_rate = self.successful_placements / (self.successful_placements + self.errors) if (self.successful_placements + self.errors) > 0 else 0
        self.skill_level = min(10, success_rate * 10)

    def get_suggested_speed(self):
        """Sugiere velocidad de caída basada en habilidad"""
        base_speed = 0.5
        return max(0.1, base_speed - (self.skill_level * 0.04))

    def render_advice(self, screen, font, position):
        """Renderiza el consejo y nivel de sabiduría mejorado"""
        wisdom_text = f"🌟 Nivel de Sabiduría: {int(self.wisdom_level)}/10"
        wisdom_surface = font.render(wisdom_text, True, (255, 215, 0))
        screen.blit(wisdom_surface, (position[0], position[1] - 50))
        
        if self.current_advice:
            lines = self.current_advice.split('\n')
            max_width = max([font.size(line)[0] for line in lines]) + 20
            advice_height = len(lines) * 25 + 20
            
            advice_bg = pygame.Surface((max_width, advice_height))
            advice_bg.set_alpha(180)
            advice_bg.fill((40, 61, 59)) 
            screen.blit(advice_bg, (position[0] - 10, position[1] - 10))
            
            y_offset = 0
            for line in lines:
                if line.strip(): 
                    color = (255, 215, 0) if "– Yachay" in line else (255, 198, 89)
                    text = font.render(line, True, color)
                    screen.blit(text, (position[0], position[1] + y_offset))
                y_offset += 25
    
    def render_advice_compact(self, screen, font, position, max_width):
        """Renderiza consejos de forma compacta sin superposiciones"""
        if not self.current_advice:
            return
            
        lines = self.current_advice.split('\n')
        filtered_lines = [line.strip() for line in lines if line.strip()]
        
        line_height = 20
        panel_height = len(filtered_lines) * line_height + 20
        panel_width = min(max_width, 580)
        
        advice_bg = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        advice_bg.fill((40, 61, 59, 200))
        pygame.draw.rect(advice_bg, (255, 215, 0), (0, 0, panel_width, panel_height), 2)
        
        if hasattr(pygame, 'transform'):
            try:
                from visual_assets import visual_assets
                small_chakana = pygame.transform.scale(visual_assets.patterns['chakana'], (12, 12))
                advice_bg.blit(small_chakana, (8, 8))
            except:
                pass
        
        screen.blit(advice_bg, position)
        
        y_offset = 10
        for line in filtered_lines:
            if len(line) > 70: 
                line = line[:67] + "..."
            
            color = (255, 215, 0) if "– Yachay" in line else (255, 198, 89)
            text_surface = font.render(line, True, color)
            
            text_x = position[0] + (panel_width - text_surface.get_width()) // 2
            screen.blit(text_surface, (text_x, position[1] + y_offset))
            y_offset += line_height

    def update_stats(self, current_time):
        """Actualiza las estadísticas del juego"""
        self.stats['play_time'] = current_time - self.last_action_time
        if len(self.decision_times) > 0:
            self.stats['avg_decision_time'] = sum(self.decision_times) / len(self.decision_times)
        self.stats['total_errors'] = self.errors

    def init_music(self):
        """Inicializa la música de fondo andina 8-bit"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            music_files = ['assets/sounds/inca_theme.mp3', 'assets/sounds/andean_8bit.wav', 'assets/inca_theme.mp3']
            for music_file in music_files:
                try:
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(-1)  # Loop infinito
                    print(f"Música cargada: {music_file}")
                    break
                except:
                    continue
        except Exception as e:
            print(f"No se pudo inicializar la música: {e}")
    
    def check_board_balance(self, board):
        """Método público para verificar equilibrio del tablero"""
        current_time = time.time()
        if current_time - self.last_balance_check > 5: 
            self.last_balance_check = current_time
            return self.analyze_board_balance(board)
        return None
    
    def get_final_stats(self):
        """Retorna estadísticas mejoradas para la pantalla final"""
        return {
            'Tiempo Total': f"{self.stats['play_time']:.1f}s",
            'Líneas Completadas': self.stats['lines_cleared'],
            'Nivel de Sabiduría': f"{int(self.wisdom_level)}/10",
            'Tiempo Promedio de Decisión': f"{self.stats['avg_decision_time']:.2f}s",
            'Errores Totales': self.stats['total_errors'],
            'Nivel de Habilidad': f"{int(self.skill_level)}/10",
            'Colocaciones Exitosas': self.successful_placements
        }
