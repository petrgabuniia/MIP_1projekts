import pygame
import sys
import math
import colorsys
import tkinter as tk
from tkinter import filedialog
from game import Game

# Initialize pygame
pygame.init()
tk_root = tk.Tk()
tk_root.withdraw()

# Constants
WIDTH, HEIGHT = 800, 600
FONT_NAME = "Arial"
FONT_SIZE = 24
COLOR_WHEEL_DIAMETER = 200
COMPUTER_MOVE_DELAY = 1000  # ms

# Colors
BG_COLOR = [0, 0, 0]
TEXT_COLOR = [255, 255, 255]

# Game state
class GameState:
    MODE = "mode"
    NAMES = "names"
    INIT = "inicializācija"
    GAME = "spēle"
    END = "spēles_beigas"
    SETTINGS = "settings"
def get_current_color():
    return BG_COLOR if settings["color_target"] == "bg" else TEXT_COLOR

def set_current_color(color):
    if settings["color_target"] == "bg":
        BG_COLOR[0], BG_COLOR[1], BG_COLOR[2] = color
        settings["bg_image"] = None
    else:
        TEXT_COLOR[0], TEXT_COLOR[1], TEXT_COLOR[2] = color
# Settings
settings = {
    "no_ads": False,
    "bg_image": None,
    "color_target": "bg",
    "brightness": 1.0,
    "saturation": 1.0,
    "selected_color": None,
    "hover_preview_color": None
}

# Game variables
game_vars = {
    "phase": GameState.MODE,
    "game_mode": None,
    "game_instance": None,
    "error_message": "",
    "mode_input": "",
    "name1": "",
    "name2": "",
    "sequence_length_input": "",
    "move_input": "",
    "last_used_length": None,
    "active_name": 1,
    "last_computer_move_time": None,
    "mouse_pressed": False
}

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spēle: Skaitļu izņemšana")
clock = pygame.time.Clock()
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Rectangles for buttons and input boxes
rects = {
    "mode_input_box": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 40),
    "exit_button": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 100, 100, 40),
    "settings_button": pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 150, 130, 40),
    "no_ads_button": pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 150, 130, 40),
    "input_name1": pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 40),
    "input_name2": pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 40),
    "input_length": pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 40),
    "input_move": pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 40),
    "replay_button": pygame.Rect(WIDTH // 2 - 160, HEIGHT // 2 + 100, 130, 40),
    "menu_button": pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 100, 130, 40),
    "color_wheel": pygame.Rect(WIDTH - 220, 80, COLOR_WHEEL_DIAMETER, COLOR_WHEEL_DIAMETER),
    "brightness_slider": pygame.Rect(WIDTH - 220 + COLOR_WHEEL_DIAMETER + 20, 80, 20, COLOR_WHEEL_DIAMETER),
    "saturation_slider": pygame.Rect(WIDTH - 220 - 30, 80, 20, COLOR_WHEEL_DIAMETER),
    "load_bg_button": pygame.Rect(50, 300, 200, 40),
    "toggle_color_button": pygame.Rect(270, 300, 200, 40),
    "back_button": pygame.Rect(WIDTH - 150, HEIGHT - 60, 130, 40)
}

def draw_text(text, x, y, color=None):
    if color is None:
        color = TEXT_COLOR  # Use the updated TEXT_COLOR by default
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def create_color_wheel(diameter, value=1.0, saturation=1.0):
    surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
    radius = diameter // 2
    for x in range(diameter):
        for y in range(diameter):
            dx = x - radius
            dy = y - radius
            distance = math.sqrt(dx * dx + dy * dy)
            if distance <= radius:
                angle = math.degrees(math.atan2(dy, dx)) % 360
                dist_saturation = distance / radius
                r, g, b = colorsys.hsv_to_rgb(
                    angle / 360, 
                    min(1.0, dist_saturation * saturation), 
                    value * (dist_saturation if dist_saturation > 0.2 else 0.0)
                )
                surface.set_at((x, y), (int(r * 255), int(g * 255), int(b * 255)))
    return surface

def smart_ai_choice(sequence):
    for priority in [3, 2, 1]:
        if priority in sequence:
            return sequence.index(priority)
    return 0

def handle_mode_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if rects["exit_button"].collidepoint(event.pos):
            pygame.quit()
            sys.exit()
        elif rects["settings_button"].collidepoint(event.pos):
            game_vars["phase"] = GameState.SETTINGS
            game_vars["error_message"] = ""
        elif rects["no_ads_button"].collidepoint(event.pos):
            settings["no_ads"] = True
            game_vars["error_message"] = "Funkcija 'Bez reklām' iegādāta!"
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if game_vars["mode_input"] in ["1", "2"]:
                game_vars["game_mode"] = "pc" if game_vars["mode_input"] == "1" else "pvp"
                game_vars["phase"] = GameState.NAMES
                game_vars["error_message"] = ""
            else:
                game_vars["error_message"] = "Lūdzu, ievadi 1 vai 2!"
            game_vars["mode_input"] = ""
        elif event.key == pygame.K_BACKSPACE:
            game_vars["mode_input"] = game_vars["mode_input"][:-1]
        elif event.unicode in ["1", "2"]:
            game_vars["mode_input"] += event.unicode

def handle_names_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if rects["input_name1"].collidepoint(event.pos):
            game_vars["active_name"] = 1
        elif rects["input_name2"].collidepoint(event.pos):
            game_vars["active_name"] = 2
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if game_vars["name1"].strip() and game_vars["name2"].strip():
                game_vars["phase"] = GameState.INIT
                game_vars["error_message"] = ""
            else:
                game_vars["error_message"] = "Lūdzu, ievadi abus vārdus!"
        elif event.key == pygame.K_BACKSPACE:
            if game_vars["active_name"] == 1:
                game_vars["name1"] = game_vars["name1"][:-1]
            else:
                game_vars["name2"] = game_vars["name2"][:-1]
        else:
            if game_vars["active_name"] == 1:
                game_vars["name1"] += event.unicode
            else:
                game_vars["name2"] += event.unicode

def handle_init_events(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            try:
                length = int(game_vars["sequence_length_input"])
                if 15 <= length <= 25:
                    game_vars["last_used_length"] = length
                    game_vars["game_instance"] = Game(length, human_starts=True)
                    game_vars["phase"] = GameState.GAME
                    game_vars["error_message"] = ""
                else:
                    game_vars["error_message"] = "Ievadi skaitli no 15 līdz 25!"
            except ValueError:
                game_vars["error_message"] = "Nepareiza ievade!"
            game_vars["sequence_length_input"] = ""
        elif event.key == pygame.K_BACKSPACE:
            game_vars["sequence_length_input"] = game_vars["sequence_length_input"][:-1]
        elif event.unicode.isdigit():
            game_vars["sequence_length_input"] += event.unicode

def handle_computer_move():
    current_time = pygame.time.get_ticks()
    if game_vars["last_computer_move_time"] is None:
        game_vars["last_computer_move_time"] = current_time
    elif current_time - game_vars["last_computer_move_time"] > COMPUTER_MOVE_DELAY:
        if game_vars["game_instance"].sequence:
            index = smart_ai_choice(game_vars["game_instance"].sequence)
            game_vars["game_instance"].make_move(index, is_human=False)
            game_vars["game_instance"].is_comp_turn = False
        game_vars["last_computer_move_time"] = None

def handle_game_events(event):
    if game_vars["game_mode"] == "pc":
        if not game_vars["game_instance"].is_comp_turn:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_vars["move_input"] in ["1", "2", "3"]:
                        chosen_number = int(game_vars["move_input"])
                        if chosen_number in game_vars["game_instance"].sequence:
                            index = game_vars["game_instance"].sequence.index(chosen_number)
                            game_vars["game_instance"].make_move(index, is_human=True)
                            game_vars["game_instance"].is_comp_turn = True
                            game_vars["last_computer_move_time"] = pygame.time.get_ticks()
                            game_vars["move_input"] = ""
                            game_vars["error_message"] = ""
                        else:
                            game_vars["error_message"] = f"Skaitlis {chosen_number} nav secībā!"
                            game_vars["move_input"] = ""
                    else:
                        game_vars["error_message"] = "Ievadi tikai 1, 2 vai 3!"
                        game_vars["move_input"] = ""
                elif event.key == pygame.K_BACKSPACE:
                    game_vars["move_input"] = game_vars["move_input"][:-1]
                elif event.unicode in ["1", "2", "3"]:
                    game_vars["move_input"] += event.unicode
    elif game_vars["game_mode"] == "pvp":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_vars["move_input"] in ["1", "2", "3"]:
                    chosen_number = int(game_vars["move_input"])
                    if chosen_number in game_vars["game_instance"].sequence:
                        index = game_vars["game_instance"].sequence.index(chosen_number)
                        game_vars["game_instance"].make_move(index, is_human=not game_vars["game_instance"].is_comp_turn)
                        game_vars["game_instance"].is_comp_turn = not game_vars["game_instance"].is_comp_turn
                        game_vars["move_input"] = ""
                        game_vars["error_message"] = ""
                    else:
                        game_vars["error_message"] = f"Skaitlis {chosen_number} nav secībā!"
                        game_vars["move_input"] = ""
                else:
                    game_vars["error_message"] = "Ievadi tikai 1, 2 vai 3!"
                    game_vars["move_input"] = ""
            elif event.key == pygame.K_BACKSPACE:
                game_vars["move_input"] = game_vars["move_input"][:-1]
            elif event.unicode in ["1", "2", "3"]:
                game_vars["move_input"] += event.unicode

def handle_end_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if rects["replay_button"].collidepoint(event.pos):
            game_vars["game_instance"] = Game(game_vars["last_used_length"], human_starts=True)
            game_vars["phase"] = GameState.GAME
            game_vars["error_message"] = ""
        elif rects["menu_button"].collidepoint(event.pos):
            game_vars["phase"] = GameState.MODE
            game_vars["game_mode"] = None
            game_vars["error_message"] = ""
    
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        game_vars["phase"] = GameState.MODE
        game_vars["game_mode"] = None
        game_vars["error_message"] = ""

def handle_settings_events(event):
    global BG_COLOR, TEXT_COLOR
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        game_vars["mouse_pressed"] = True
        if rects["load_bg_button"].collidepoint(event.pos):
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
            if file_path:
                try:
                    img = pygame.image.load(file_path)
                    settings["bg_image"] = pygame.transform.scale(img, (WIDTH, HEIGHT))
                    settings["selected_color"] = None
                except Exception:
                    game_vars["error_message"] = "Nevar ielādēt attēlu!"
        
        elif rects["toggle_color_button"].collidepoint(event.pos):
            settings["color_target"] = "text" if settings["color_target"] == "bg" else "bg"
        
        elif rects["back_button"].collidepoint(event.pos):
            game_vars["phase"] = GameState.MODE
        
        elif rects["color_wheel"].collidepoint(event.pos):
            mx, my = event.pos
            rel_x = mx - rects["color_wheel"].x
            rel_y = my - rects["color_wheel"].y
            radius = COLOR_WHEEL_DIAMETER // 2
            dx = rel_x - radius
            dy = rel_y - radius
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= radius:
                try:
                    settings["hover_preview_color"] = create_color_wheel(
                        COLOR_WHEEL_DIAMETER, 
                        settings["brightness"], 
                        settings["saturation"]
                    ).get_at((rel_x, rel_y))[:3]
                except IndexError:
                    settings["hover_preview_color"] = None
    
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if game_vars["mouse_pressed"] and settings["hover_preview_color"]:
            settings["selected_color"] = settings["hover_preview_color"]
            if settings["color_target"] == "bg":
                BG_COLOR = settings["selected_color"]
                settings["bg_image"] = None
            else:
                TEXT_COLOR = settings["selected_color"]
        game_vars["mouse_pressed"] = False
    
    elif event.type == pygame.MOUSEMOTION and game_vars["mouse_pressed"]:
        mx, my = pygame.mouse.get_pos()
        
        if rects["saturation_slider"].collidepoint((mx, my)):
            relative_y = my - rects["saturation_slider"].top
            settings["saturation"] = 1 - (relative_y / rects["saturation_slider"].height)
            settings["saturation"] = max(0, min(1, settings["saturation"]))
        
        elif rects["brightness_slider"].collidepoint((mx, my)):
            relative_y = my - rects["brightness_slider"].top
            settings["brightness"] = 1 - (relative_y / rects["brightness_slider"].height)
            settings["brightness"] = max(0, min(1, settings["brightness"]))
        
        elif rects["color_wheel"].collidepoint((mx, my)):
            rel_x = mx - rects["color_wheel"].x
            rel_y = my - rects["color_wheel"].y
            radius = COLOR_WHEEL_DIAMETER // 2
            dx = rel_x - radius
            dy = rel_y - radius
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= radius:
                try:
                    settings["hover_preview_color"] = create_color_wheel(
                        COLOR_WHEEL_DIAMETER, 
                        settings["brightness"], 
                        settings["saturation"]
                    ).get_at((rel_x, rel_y))[:3]
                except IndexError:
                    settings["hover_preview_color"] = None
            else:
                settings["hover_preview_color"] = None

def draw_mode_screen():
    draw_text("Izvēlies spēles režīmu:", WIDTH // 2 - 140, HEIGHT // 2 - 100)
    draw_text("1 - pret datoru, 2 - pret spēlētāju", WIDTH // 2 - 160, HEIGHT // 2 - 70)
    
    pygame.draw.rect(screen, TEXT_COLOR, rects["mode_input_box"], 2)
    draw_text(game_vars["mode_input"], rects["mode_input_box"].x + 10, rects["mode_input_box"].y + 10)
    
    pygame.draw.rect(screen, (200, 0, 0), rects["exit_button"])
    draw_text("Iziet", rects["exit_button"].x + 15, rects["exit_button"].y + 10)
    
    pygame.draw.rect(screen, (0, 200, 200), rects["settings_button"])
    draw_text("Iestatījumi", rects["settings_button"].x + 5, rects["settings_button"].y + 10)
    
    pygame.draw.rect(screen, (200, 200, 0), rects["no_ads_button"])
    draw_text("Bez reklām", rects["no_ads_button"].x + 5, rects["no_ads_button"].y + 10)
    
    if not settings["no_ads"]:
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(0, 0, WIDTH, 50))
        draw_text("Reklāmas baneris", 10, 10)
    
    if game_vars["error_message"]:
        draw_text(game_vars["error_message"], WIDTH // 2 - 150, HEIGHT // 2 + 200, (255, 0, 0))

def draw_names_screen():
    if game_vars["game_mode"] == "pc":
        draw_text("Ievadi savu vārdu:", WIDTH // 2 - 150, HEIGHT // 2 - 80)
        draw_text("Ievadi bota vārdu:", WIDTH // 2 - 150, HEIGHT // 2 + 10)
    else:
        draw_text("Ievadi Spēlētājs 1 vārdu:", WIDTH // 2 - 150, HEIGHT // 2 - 80)
        draw_text("Ievadi Spēlētājs 2 vārdu:", WIDTH // 2 - 150, HEIGHT // 2 + 10)
    
    pygame.draw.rect(screen, (255, 255, 255), rects["input_name1"], 2)
    pygame.draw.rect(screen, (255, 255, 255), rects["input_name2"], 2)
    draw_text(game_vars["name1"], rects["input_name1"].x + 10, rects["input_name1"].y + 10)
    draw_text(game_vars["name2"], rects["input_name2"].x + 10, rects["input_name2"].y + 10)
    
    draw_text("Nospied Enter, lai turpinātu", WIDTH // 2 - 150, HEIGHT // 2 + 60)
    
    if game_vars["error_message"]:
        draw_text(game_vars["error_message"], WIDTH // 2 - 150, HEIGHT // 2 + 100, (255, 0, 0))

def draw_init_screen():
    draw_text("Ievadi secības garumu (15-25):", WIDTH // 2 - 180, HEIGHT // 2 - 80)
    pygame.draw.rect(screen, (255, 255, 255), rects["input_length"], 2)
    draw_text(game_vars["sequence_length_input"], rects["input_length"].x + 10, rects["input_length"].y + 10)
    
    if game_vars["error_message"]:
        draw_text(game_vars["error_message"], WIDTH // 2 - 150, HEIGHT // 2 + 60, (255, 0, 0))

def draw_game_screen():
    draw_text("Atlikusā secība: " + " ".join(map(str, game_vars["game_instance"].sequence)), 20, 20)
    
    if game_vars["game_mode"] == "pc":
        draw_text(f"{game_vars['name1']}: {game_vars['game_instance'].human_score}", 20, 60)
        draw_text(f"{game_vars['name2']} (Bota): {game_vars['game_instance'].comp_score}", 20, 100)
        
        if game_vars["game_instance"].is_comp_turn:
            current_time = pygame.time.get_ticks()
            if game_vars["last_computer_move_time"] is not None:
                time_left = max(0, COMPUTER_MOVE_DELAY - (current_time - game_vars["last_computer_move_time"]))
                draw_text(f"Datora gājiens pēc: {time_left//1000}.{time_left%1000//100}...", 20, HEIGHT - 100)
            else:
                draw_text("Datora kārta...", 20, HEIGHT - 100)
        else:
            draw_text("Tava kārta! Ievadi 1, 2 vai 3:", 20, HEIGHT - 140)
            pygame.draw.rect(screen, (255, 255, 255), rects["input_move"], 2)
            draw_text(game_vars["move_input"], rects["input_move"].x + 10, rects["input_move"].y + 10)
    else:
        draw_text(f"{game_vars['name1']}: {game_vars['game_instance'].human_score}", 20, 60)
        draw_text(f"{game_vars['name2']}: {game_vars['game_instance'].comp_score}", 20, 100)
        
        if not game_vars["game_instance"].is_comp_turn:
            draw_text("Spēlētājs 1, ievadi savu gājienu (1, 2 vai 3):", 20, HEIGHT - 140)
        else:
            draw_text("Spēlētājs 2, ievadi savu gājienu (1, 2 vai 3):", 20, HEIGHT - 140)
        
        pygame.draw.rect(screen, (255, 255, 255), rects["input_move"], 2)
        draw_text(game_vars["move_input"], rects["input_move"].x + 10, rects["input_move"].y + 10)
    
    if game_vars["error_message"]:
        draw_text(game_vars["error_message"], 20, HEIGHT - 50, (255, 0, 0))

def draw_end_screen():
    if game_vars["game_mode"] == "pvp":
        if game_vars["game_instance"].human_score > game_vars["game_instance"].comp_score:
            result = f"{game_vars['name1']} uzvar!"
        elif game_vars["game_instance"].comp_score > game_vars["game_instance"].human_score:
            result = f"{game_vars['name2']} uzvar!"
        else:
            result = "Neizšķirts!"
    else:
        result = game_vars["game_instance"].get_winner()
    
    draw_text("Spēle beigusies!", WIDTH // 2 - 100, HEIGHT // 2 - 60)
    draw_text(result, WIDTH // 2 - 100, HEIGHT // 2 - 20)
    
    pygame.draw.rect(screen, (0, 200, 0), rects["replay_button"])
    draw_text("Spēlēt atkal", rects["replay_button"].x + 5, rects["replay_button"].y + 10)
    
    pygame.draw.rect(screen, (0, 0, 200), rects["menu_button"])
    draw_text("Galvenā izvēlne", rects["menu_button"].x + 5, rects["menu_button"].y + 10)

def draw_settings_screen():
    color_wheel = create_color_wheel(COLOR_WHEEL_DIAMETER, settings["brightness"], settings["saturation"])
    
    draw_text("Iestatījumi", WIDTH // 2 - 60, 20)
    draw_text("Izvēlies krāsu (klikšķini uz ratīta):", WIDTH - 230, 40)
    screen.blit(color_wheel, rects["color_wheel"])
    
    # Draw sliders
    pygame.draw.rect(screen, (100, 100, 100), rects["saturation_slider"])
    pygame.draw.rect(screen, (100, 100, 100), rects["brightness_slider"])
    
    # Position of the circle on the sliders
    saturation_pos = rects["saturation_slider"].top + (1 - settings["saturation"]) * rects["saturation_slider"].height
    brightness_pos = rects["brightness_slider"].top + (1 - settings["brightness"]) * rects["brightness_slider"].height
    
    pygame.draw.circle(screen, (255, 255, 255), (rects["saturation_slider"].centerx, saturation_pos), 10)
    pygame.draw.circle(screen, (255, 255, 255), (rects["brightness_slider"].centerx, brightness_pos), 10)
    
    draw_text(f"Saturation: {settings['saturation']:.2f}", rects["saturation_slider"].left - 120, rects["saturation_slider"].top)
    draw_text(f"Brightness: {settings['brightness']:.2f}", rects["brightness_slider"].right + 10, rects["brightness_slider"].top)
    
    draw_text("Pašreiz: " + ("Fons" if settings["color_target"] == "bg" else "Teksts"), 
              rects["color_wheel"].x, rects["color_wheel"].y - 30)
    
    # Preview color
    if settings["hover_preview_color"]:
        pygame.draw.rect(screen, settings["hover_preview_color"], pygame.Rect(WIDTH - 120, 80, 60, 30))
        draw_text("Priekšskatījums", WIDTH - 125, 120)
    
    pygame.draw.rect(screen, (200, 200, 200), rects["toggle_color_button"])
    draw_text("Mainīt mērķi", rects["toggle_color_button"].x + 10, rects["toggle_color_button"].y + 10, (0, 0, 0))
    
    pygame.draw.rect(screen, (150, 150, 150), rects["load_bg_button"])
    draw_text("Ielādēt fona attēlu", rects["load_bg_button"].x + 5, rects["load_bg_button"].y + 10, (0, 0, 0))
    
    pygame.draw.rect(screen, (150, 150, 150), rects["back_button"])
    draw_text("Atpakaļ", rects["back_button"].x + 10, rects["back_button"].y + 10, (0, 0, 0))
    
    if game_vars["error_message"]:
        draw_text(game_vars["error_message"], WIDTH // 2 - 150, HEIGHT - 80, (255, 0, 0))

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if game_vars["phase"] == GameState.MODE:
            handle_mode_events(event)
        elif game_vars["phase"] == GameState.NAMES:
            handle_names_events(event)
        elif game_vars["phase"] == GameState.INIT:
            handle_init_events(event)
        elif game_vars["phase"] == GameState.GAME:
            handle_game_events(event)
        elif game_vars["phase"] == GameState.END:
            handle_end_events(event)
        elif game_vars["phase"] == GameState.SETTINGS:
            handle_settings_events(event)
    
    # Computer move handling
    if (game_vars["phase"] == GameState.GAME and 
        game_vars["game_instance"] and 
        game_vars["game_mode"] == "pc" and 
        game_vars["game_instance"].is_comp_turn):
        handle_computer_move()
    
    # Game over handling
    if game_vars["phase"] == GameState.GAME and game_vars["game_instance"] and game_vars["game_instance"].is_game_over():
        game_vars["phase"] = GameState.END
    
    # Clear screen
    if settings["bg_image"]:
        screen.blit(settings["bg_image"], (0, 0))
    else:
        screen.fill(BG_COLOR)
    
    # Draw screen based on game phase
    if game_vars["phase"] == GameState.MODE:
        draw_mode_screen()
    elif game_vars["phase"] == GameState.NAMES:
        draw_names_screen()
    elif game_vars["phase"] == GameState.INIT:
        draw_init_screen()
    elif game_vars["phase"] == GameState.GAME:
        draw_game_screen()
    elif game_vars["phase"] == GameState.END:
        draw_end_screen()
    elif game_vars["phase"] == GameState.SETTINGS:
        draw_settings_screen()
    
    pygame.display.flip()
    clock.tick(60)