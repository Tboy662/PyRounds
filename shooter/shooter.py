import pygame
import sys
import math
import random
import Soundsys as sound
# ------------------
# Configuration & Scaling
# ------------------
device = "Windows"
if device == "Mac":
    extra_path = "/Users/tomerbar/Python_III/"
    res = 1450, 800
    scale = 0.7
else:
    res = 2560, 720
    scale = 1
    extra_path = ""

WIDTH, HEIGHT = res

def s(val):
    """Helper function to scale pixel values."""
    return int(val * scale)

# ------------------
# Initialization
# ------------------
pygame.init()
sound.initsounds(60)
# Using SCALED handles the window stretching, but manual scaling ensures high-res assets look sharp
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("PyRounds")

CLOCK = pygame.time.Clock()
FPS = 60
health1 = 100
health2 = 100
damage1 = 10
damage2 = 10

# Scale Font Sizes
title_font = pygame.font.SysFont("arial", s(22), bold=True)
desc_font = pygame.font.SysFont("arial", s(16))

card_picking_turn = 1
basehealth1 = 100
basehealth2 = 100
basehealth1,basehealth2=100,100
# ------------------
# Colors
# ------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
hb1color = [0, 255, 0]
hb2color = [0, 255, 0]
randcolor = (random.randint(50, 200), random.randint(50, 255), random.randint(50, 255))
second_life = 0
move_speed = s(5)
move_speed2= s(5)
# ------------------
# Card Loading
# ------------------
def loadcards(filename):
    global cards
    cards = []
    with open(filename, 'r') as file:
        for line in file:
            card_data = line.strip().split('_')
            # Load and scale card image
            img = pygame.image.load(extra_path + card_data[1]).convert_alpha()
            img = pygame.transform.scale(img, (s(160), s(120)))
            
            card = {
                'name': card_data[0],
                'card_image': img,
                'image_path': extra_path + card_data[1],
                'shoot_type_req': card_data[6],
                'r': card_data[3],
                'g': card_data[4],
                'b': card_data[5],
                'color': (int(card_data[3]), int(card_data[4]), int(card_data[5])),
                'description': card_data[2],
                'attack_mod': float(card_data[7]) if card_data[7] else None,
                'hp_mod': int(card_data[8]) if card_data[8] else None,
                'speed_mod': int(card_data[9]) if len(card_data) > 9 else None,
                'second_life': int(card_data[10]) if len(card_data) > 10 else None,
            }
            cards.append(card)

# ------------------
# Player & Gun Assets (Scaled)
# ------------------
img_folder = "shooter/images"

player_img_orig = pygame.image.load(extra_path + "/shooter/images/player.jpeg").convert_alpha()

gun_img_orig = pygame.image.load(extra_path + "/shooter/images/glock.png").convert_alpha()

# Apply Scaling to Images
player_img_orig = pygame.transform.scale(player_img_orig, (s(50), s(80)))
gun_img_orig = pygame.transform.scale(gun_img_orig, (s(30), s(30)))

player_width, player_height = player_img_orig.get_size()
player_rect = pygame.Rect(s(100), s(100), player_width, player_height)
gun2_img_orig=gun_img_orig
player_vel_y = 0
facing_right = True
player_img = player_img_orig
gun_img = gun_img_orig

# Scaled Offsets
gun_offset_x = s(50)
gun_offset_y = s(15)
bullet_offset_x = s(51)
bullet_offset_y = s(25)

# Player 2
if device !="Mac":
    player2_rect = pygame.Rect(WIDTH - 360, 100, player_width, player_height)
else:
    player2_rect = pygame.Rect(WIDTH - 100, 100, player_width, player_height)
player2_vel_y = 0
player2_facing_right = False
player2_img = player_img_orig
gun2_img = gun_img_orig
gun2_offset_x = s(50)
gun2_offset_y = s(15)
bullet2_offset_x = s(51)
bullet2_offset_y = s(25)
player2_angle = 0
round_count = 0
p1color=0,255,0
showslife1=False
showslife2=False

second_life_2=0
#------------------
#gun rand --139--
#------------------
def randgun():
    global gun_img,gun2_img,gun_img_orig,gun2_img_orig
    pick=random.randint(0,1100)
    if pick<1:
        gun_img_orig=pygame.image.load(extra_path + "/shooter/images/pineapple.png").convert_alpha()
        gun_img_orig = pygame.transform.scale(gun_img_orig, (s(32), s(32)))
    elif pick<10:
        gun_img_orig=pygame.image.load(extra_path + "/shooter/images/mp7.png").convert_alpha()
        gun_img_orig = pygame.transform.scale(gun_img_orig, (s(32), s(32)))
    elif pick<50:
        gun_img_orig=pygame.image.load(extra_path + "/shooter/images/p90.png").convert_alpha()
        gun_img_orig = pygame.transform.scale(gun_img_orig, (s(32), s(32)))
    elif pick<200:
        gun_img_orig=pygame.image.load(extra_path + "/shooter/images/m4a1.png").convert_alpha()
        gun_img_orig = pygame.transform.scale(gun_img_orig, (s(32), s(32)))
    elif pick<500:
        gun_img_orig=pygame.image.load(extra_path + "/shooter/images/colt.png").convert_alpha()
        gun_img_orig = pygame.transform.scale(gun_img_orig, (s(32), s(32)))
    elif pick<1100:
        gun_img_orig=pygame.image.load(extra_path + "/shooter/images/glock.png").convert_alpha()
        gun_img_orig = pygame.transform.scale(gun_img_orig, (s(32), s(32)))
    
    pick=random.randint(0,1100)
    if pick<1:
        gun2_img_orig=pygame.image.load(extra_path + "/shooter/images/pineapple.png").convert_alpha()
        gun2_img_orig = pygame.transform.scale(gun2_img_orig, (s(32), s(32)))
    elif pick<10:
        gun2_img_orig=pygame.image.load(extra_path + "/shooter/images/mp7.png").convert_alpha()
        gun2_img_orig = pygame.transform.scale(gun2_img_orig, (s(32), s(32)))
    elif pick<50:
        gun2_img_orig=pygame.image.load(extra_path + "/shooter/images/p90.png").convert_alpha()
        gun2_img_orig = pygame.transform.scale(gun2_img_orig, (s(32), s(32)))
    elif pick<200:
        gun2_img_orig=pygame.image.load(extra_path + "/shooter/images/m4a1.png").convert_alpha()
        gun2_img_orig = pygame.transform.scale(gun2_img_orig, (s(32), s(32)))
    elif pick<500:
        gun2_img_orig=pygame.image.load(extra_path + "/shooter/images/colt.png").convert_alpha()
        gun2_img_orig = pygame.transform.scale(gun2_img_orig, (s(32), s(32)))
    elif pick<1100:
        gun2_img_orig=pygame.image.load(extra_path + "/shooter/images/glock.png").convert_alpha()
        gun2_img_orig = pygame.transform.scale(gun2_img_orig, (s(32), s(32)))
randgun()
# ------------------
# Platforms (Scaled Coordinates)
# ------------------
def random_platforms():
    featue_type = random.randint(0, 1)
    global plat
    plat = []
    if featue_type == 0:
        plat.append(pygame.Rect(s(121), s(949), s(200), s(20)))
        plat.append(pygame.Rect(s(1746), s(949), s(200), s(20)))
        plat.append(pygame.Rect(s(478), s(828), s(500), s(20)))
        plat.append(pygame.Rect(s(1071), s(828), s(500), s(20)))
        plat.append(pygame.Rect(s(598), s(713), s(200), s(20)))
        plat.append(pygame.Rect(s(907), s(580), s(200), s(20)))
    if featue_type == 1:
        plat.append(pygame.Rect(s(295), s(1024), s(1500), s(20)))
        plat.append(pygame.Rect(s(295), s(580), s(1500), s(20)))
        plat.append(pygame.Rect(s(295), s(800), s(300), s(20)))
        plat.append(pygame.Rect(s(1554), s(800), s(300), s(20)))
        plat.append(pygame.Rect(s(911), s(800), s(300), s(20)))
    
    # Static platforms
    plat.append(pygame.Rect(s(294), s(580), s(1500), s(20)))
    plat.append(pygame.Rect(s(288), s(486), s(500), s(20)))
    plat.append(pygame.Rect(s(1278), s(476), s(500), s(20)))
    plat.append(pygame.Rect(s(786), s(373), s(500), s(20)))
    plat.append(pygame.Rect(s(288), s(256), s(500), s(20)))
    plat.append(pygame.Rect(s(1283), s(248), s(500), s(20)))
    plat.append(pygame.Rect(s(1559), s(132), s(500), s(20)))
    plat.append(pygame.Rect(s(132), s(159), s(500), s(20)))
    plat.append(pygame.Rect(s(808), s(152), s(500), s(20)))

random_platforms()
def get_health_color(current, base, player):
    global basehealth1,basehealth2,health1,health2
    
    
    if current==0:
        current=1
    if base==0:
        base=1
    pct = max(0, min(1, current / base))
    # Transition from Green (0,255,0) to Red (255,0,0)
    r = int(255 * (1 - pct))
    g = int(255 * pct)
    if showslife1 and player==1:
        b=255
    elif showslife2 and player==2:
        b=255
    else:
        b=0
    return (r, g, b)
#------------------
# Cards Setup
# ------------------
loadcards(extra_path + "shooter/cards/cards.pylist")

# Scaled Card UI Positions
card_rects = [
    pygame.Rect(s(660), s(390), s(200), s(300)),
    pygame.Rect(s(940), s(390), s(200), s(300)),
    pygame.Rect(s(1220), s(390), s(200), s(300)),
    pygame.Rect(s(1500), s(390), s(200), s(300)),
]
image_rects = [
    pygame.Rect(s(680), s(510), s(160), s(120)),
    pygame.Rect(s(960), s(510), s(160), s(120)),
    pygame.Rect(s(1240), s(510), s(160), s(120)),
    pygame.Rect(s(1520), s(510), s(160), s(120)),
]

def randcard():
    return [random.randint(0, len(cards) - 1) for _ in range(4)]
randcardpick = [random.randint(0, len(cards) - 1) for _ in range(4)]
selected_cards = []  
Disp = False

# Projectiles
projectiles = []
PROJECTILE_SPEED = s(25)
PROJECTILE_SPEED_2 = s(25)
PROJECTILE_SIZE = (s(15), s(5))

# ------------------
# Gravity & Collision (Scaled)
# ------------------
def apply_gravity(rect, vel_y):
    vel_y += 0.8 * scale # Scale gravity strength
    rect.y += vel_y
    if rect.bottom >= HEIGHT:
        rect.bottom = HEIGHT
        vel_y = 0
    for platform in plat:
        if rect.colliderect(platform) and vel_y > 0:
            rect.bottom = platform.top
            vel_y = 0
    return rect, vel_y
# ------------------
# Randomize Player Pos
# ------------------
def randplayer():
    player_rect.x,player2_rect.x,player_rect.y,player2_rect.y=random.randint(0,1450),random.randint(0,1450),random.randint(0,800),random.randint(0,800)
# ------------------
# Main Game Loop
# ------------------
sound.addsound("/Users/tomerbar/Python_III/shooter/sounds/Neon Code.mp3","Neon Code","bg",True,True)
running = True
while running:
    sound.update_sounds()
    CLOCK.tick(FPS)
    SCREEN.fill(BLACK)

    

    # Health boxes (Scaled offsets and sizes)
    hbox1 = pygame.Rect(player_rect.x - s(25), player_rect.y - s(50), s(health1), s(10))
    hbox2 = pygame.Rect(player2_rect.x - s(25), player2_rect.y - s(50), s(health2), s(10))
    
    
    
    keys = pygame.key.get_pressed()

    # ---- EVENTS ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # PLAYER 1 SHOOT
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            # Bullet origin calculation with scaled offsets
            b_off = bullet_offset_x - s(30) if facing_right else bullet_offset_x
            gun_tip = pygame.Vector2(
                player_rect.right + b_off if facing_right else player_rect.left + bullet_offset_x,
                player_rect.y + bullet_offset_y
            )
            vec = mouse_pos - gun_tip
            if vec.length() != 0:
                direction = vec.normalize()
                angle = math.degrees(math.atan2(-direction.y, direction.x))
                projectiles.append({
                    "pos": gun_tip.copy(),
                    "dir": direction,
                    "angle": angle,
                    "clock": 0,
                    "owner": 1
                })

        # CARD SELECTION (Right Click)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for i, carddata in enumerate(selected_cards):
                if carddata['rect'].collidepoint(pygame.mouse.get_pos()):
                    if card_picking_turn == 1:
                        card_picking_turn = 2
                        if carddata['card']['attack_mod']>0:
                            damage1 *= carddata['card']['attack_mod']
                        if carddata['card']['hp_mod'] is not None:
                            if basehealth1-carddata['card']['hp_mod']<1:
                                pass
                            else:
                                basehealth1+=carddata['card']['hp_mod']
                                health1=basehealth1
                                print('290')
                        if carddata['card']['speed_mod'] is not None:
                            move_speed+=carddata['card']['speed_mod']
                            PROJECTILE_SPEED+=carddata['card']['speed_mod']
                        if carddata['card']['second_life']>0:
                            second_life+=carddata['card']['second_life']

                    elif card_picking_turn == 2:
                        card_picking_turn = 1
                        if carddata['card']['attack_mod']>0:
                            damage2 *= carddata['card']['attack_mod']
                        
                        if carddata['card']['hp_mod'] is not None:
                            if basehealth2-carddata['card']['hp_mod']<1:
                                pass
                            else:
                                basehealth2+=carddata['card']['hp_mod']
                                health2=basehealth2
                        if carddata['card']['speed_mod'] is not None:
                            move_speed2+=carddata['card']['speed_mod']
                            PROJECTILE_SPEED_2+=carddata['card']['speed_mod']
                        if carddata['card']['second_life']>0:
                            second_life_2+=carddata['card']['second_life']
                        Disp = False
        
        # PLAYER 2 SHOOT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RALT:
                direction = pygame.Vector2(math.cos(math.radians(player2_angle)),
                                           -math.sin(math.radians(player2_angle)))
                projectiles.append({
                    "pos": pygame.Vector2(player2_rect.center),
                    "dir": direction,
                    "angle": player2_angle,
                    "clock": 0,
                    "owner": 2
                })
            if event.key == pygame.K_r:
                sound.addsound("/Users/tomerbar/Python_III/shooter/sounds/pistol-cock.mp3","pcock","short_sound",True,False)
                pass
            if event.key == pygame.K_t:
                sound.stop_sound("Neon Code")
                sound.stop_type("short_sound")
    # ---- PLAYER 1 MOVEMENT (Scaled Speeds) ----
    
    if keys[pygame.K_a]:
        player_rect.x -= move_speed
        gun_offset_x = s(-30)
        bullet_offset_x = s(-31)
        if facing_right:
            player_img = pygame.transform.flip(player_img_orig, True, False)
            gun_img = pygame.transform.flip(gun_img_orig, True, False)
            facing_right = False
    if keys[pygame.K_d]:
        player_rect.x += move_speed
        gun_offset_x = s(50)
        bullet_offset_x = s(51)
        if not facing_right:
            player_img = player_img_orig
            gun_img = gun_img_orig
            facing_right = True
    if keys[pygame.K_SPACE] and player_vel_y == 0:
        player_vel_y = s(-20)

    # ---- PLAYER 2 MOVEMENT ----
    if keys[pygame.K_LEFT]:
        player2_rect.x -= move_speed
        gun2_offset_x = s(-30)
        bullet2_offset_x = s(-31)
        if player2_facing_right:
            player2_img = pygame.transform.flip(player_img_orig, True, False)
            gun2_img = pygame.transform.flip(gun2_img_orig, True, False)
            player2_facing_right = False
    if keys[pygame.K_RIGHT]:
        player2_rect.x += move_speed
        gun2_offset_x = s(50)
        bullet2_offset_x = s(51)
        if not player2_facing_right:
            player2_img = player_img_orig
            gun2_img = gun2_img_orig
            player2_facing_right = True
    if keys[pygame.K_RSHIFT] and player2_vel_y == 0:
        player2_vel_y = s(-20)
    if keys[pygame.K_UP]:
        player2_angle += 3
    if keys[pygame.K_DOWN]:
        player2_angle -= 3

    # ---- APPLY GRAVITY ----
    player_rect, player_vel_y = apply_gravity(player_rect, player_vel_y)
    player2_rect, player2_vel_y = apply_gravity(player2_rect, player2_vel_y)

    # ---- UPDATE PROJECTILES ----
    for proj in projectiles[:]:
        if proj["owner"]==1:
            proj["pos"] += proj["dir"] * PROJECTILE_SPEED
        else:
            proj["pos"] += proj["dir"] * PROJECTILE_SPEED_2
        proj["clock"] += 1
        bullet_rect = pygame.Rect(0, 0, *PROJECTILE_SIZE)
        bullet_rect.center = proj["pos"]

        # Bounce
        if bullet_rect.left <= 0 or bullet_rect.right >= WIDTH:
            proj["dir"].x *= -1
        if bullet_rect.top <= 0 or bullet_rect.bottom >= HEIGHT:
            proj["dir"].y *= -1
        for platform in plat:
            if bullet_rect.colliderect(platform):
                proj["dir"].y *= -1
                break

        # Player hit
        # Player 1 hit by Player 2
        if proj["owner"] == 2 and bullet_rect.colliderect(player_rect) and proj["clock"] > 1:
            health1 -= damage2
            print(damage1,'|398')
            if proj in projectiles: projectiles.remove(proj) # Safer removal
            if health1 <= 0:
                print(second_life)
                if second_life>0:
                    health1 = basehealth1
                    print(basehealth1)
                    showslife1 = True
                else:
                    
                    showslife1,showslife2=False,False
                    Disp = True
                    randplayer()
                    randgun()
                    projectiles.clear()
                    health1, health2 = basehealth1, basehealth2
                    randcardpick = [random.randint(0, len(cards) - 1) for _ in range(4)]
                if showslife1:
                    second_life-=1

        # Player 2 hit by Player 1
        if proj["owner"] == 1 and bullet_rect.colliderect(player2_rect) and proj["clock"] > 10:
            health2 -= damage1
            if proj in projectiles: projectiles.remove(proj) # Safer removal
            if health2 <= 0:
                if second_life_2>0:
                    health2 = basehealth2
                    second_life_2 -=1
                    showslife2 = True
                else:
                    showslife1,showslife2=False,False
                    Disp = True
                    randplayer()
                    randgun()
                    projectiles.clear()
                    health1, health2 = basehealth1, basehealth2
                    randcardpick = [random.randint(0, len(cards) - 1) for _ in range(4)]

    # ---- DRAW ----
    # Aim Line
    aim_length = s(200)
    aim_end = (
        player2_rect.centerx + math.cos(math.radians(player2_angle)) * aim_length,
        player2_rect.centery - math.sin(math.radians(player2_angle)) * aim_length
    )
    pygame.draw.line(SCREEN, RED, player2_rect.center, aim_end, s(3))

    pygame.draw.line(SCREEN, WHITE, (0, HEIGHT), (WIDTH, HEIGHT), s(2))
    pygame.draw.rect(SCREEN, get_health_color(health1,basehealth1,1), hbox1)
    pygame.draw.rect(SCREEN, get_health_color(health2,basehealth2,2), hbox2)
    
    for platform in plat:
        pygame.draw.rect(SCREEN, randcolor, platform)
    
    SCREEN.blit(player_img, player_rect.topleft)
    SCREEN.blit(player2_img, player2_rect.topleft)

    # Cards Rendering
    selected_cards = []
    for i, card_rect in enumerate(card_rects):
        if i >= len(cards) or not Disp:
            break
        card = cards[randcardpick[i]]
        carddata = {'card': card, 'rect': card_rect, 'image_rect': image_rects[i]}
        selected_cards.append(carddata)
        
        pygame.draw.rect(SCREEN, card["color"], card_rect, border_radius=s(10))
        pygame.draw.rect(SCREEN, WHITE, card_rect, s(2), border_radius=s(10))
        
        # Scale card image display
        img = pygame.transform.scale(card["card_image"], image_rects[i].size)
        SCREEN.blit(img, image_rects[i])
        if card["color"][1]+card["color"][2]+card["color"][0]>400:
            cardcol=BLACK
        else:
            cardcol=WHITE
        title_surf = title_font.render(card["name"], True, cardcol)
        SCREEN.blit(title_surf, (card_rect.x + s(10), card_rect.y + s(10)))

        desc_surf = desc_font.render(card["description"], True, cardcol)
        SCREEN.blit(desc_surf, (card_rect.x + s(10), card_rect.bottom - s(35)))

    # Guns
    SCREEN.blit(gun_img, (player_rect.x + gun_offset_x, player_rect.y + gun_offset_y))
    SCREEN.blit(gun2_img, (player2_rect.x + gun2_offset_x, player2_rect.y + gun2_offset_y))

    for proj in projectiles:
        surf = pygame.Surface(PROJECTILE_SIZE, pygame.SRCALPHA)
        surf.fill(RED)
        rotated = pygame.transform.rotate(surf, proj["angle"])
        SCREEN.blit(rotated, rotated.get_rect(center=proj["pos"]))

    pygame.display.flip()
    
pygame.quit()

sys.exit()
