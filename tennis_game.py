import pygame
import sys
import random
import time

# تهيئة pygame
pygame.init()

# ثوابت اللعبة
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
WHITE = (255, 0, 0)
BLACK = (0, 255, 0)
BALL_SPEED = 4
PADDLE_SPEED = 10
FPS = 60

# إنشاء النافذة
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة التنس")
clock = pygame.time.Clock()

# المضارب والكرة
player_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# سرعة الكرة
ball_speed_x = BALL_SPEED * random.choice((1, -1))
ball_speed_y = BALL_SPEED * random.choice((1, -1))

# نقاط اللاعبين
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 74)

def reset_ball():
    """إعادة الكرة إلى وسط الملعب وتحديد اتجاه عشوائي"""
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = BALL_SPEED * random.choice((1, -1))
    ball_speed_y = BALL_SPEED * random.choice((1, -1))

def opponent_ai():
    """حركة الخصم الآلي البسيطة"""
    if opponent_paddle.top < ball.y:
        opponent_paddle.top += min(PADDLE_SPEED, ball.y - opponent_paddle.top)
    if opponent_paddle.bottom > ball.y:
        opponent_paddle.bottom -= min(PADDLE_SPEED, opponent_paddle.bottom - ball.y)
    
    # التأكد من أن المضرب لا يخرج من الشاشة
    if opponent_paddle.top < 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom > HEIGHT:
        opponent_paddle.bottom = HEIGHT

def ball_movement():
    """حركة الكرة والتصادمات"""
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    
    # تحريك الكرة
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # التصادم مع الحدود العلوية والسفلية
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    # التسجيل
    if ball.left <= 0:
        opponent_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()
    
    # التصادم مع المضارب
    if ball.colliderect(player_paddle) and ball_speed_x < 0:
        ball_speed_x *= -1
    if ball.colliderect(opponent_paddle) and ball_speed_x > 0:
        ball_speed_x *= -1

def draw_objects():
    """رسم كل العناصر على الشاشة"""
    # تنظيف الشاشة
    screen.fill(BLACK)
    
    # رسم المضارب والكرة
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # رسم الخط المنتصف
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # عرض النقاط
    player_text = font.render(str(player_score), True, WHITE)
    opponent_text = font.render(str(opponent_score), True, WHITE)
    screen.blit(player_text, (WIDTH//4, 20))
    screen.blit(opponent_text, (3*WIDTH//4, 20))

def show_splash_image():
    """عرض صورة البداية لمدة 2 ثانية"""
    try:
        # محاولة تحميل الصورة
        # يجب أن يكون الملف "splash.png" موجودًا في نفس المجلد مع البرنامج
        splash_image = pygame.image.load("splash.jpg")
        
        # ضبط حجم الصورة لتناسب الشاشة
        splash_image = pygame.transform.scale(splash_image, (WIDTH, HEIGHT))
        
        # عرض الصورة
        screen.blit(splash_image, (0, 0))
        pygame.display.flip()
        
        # انتظار لمدة 2 ثانية
        start_time = time.time()
        while time.time() - start_time < 2:
            # معالجة الأحداث فقط لإغلاق اللعبة إذا ضغط المستخدم على زر الإغلاق
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(FPS)
            
    except pygame.error:
        # في حالة عدم وجود الصورة، سيتم عرض شاشة بداية بسيطة
        screen.fill(BLACK)
        title_text = font.render("لعبة التنس", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - title_text.get_height()//2))
        pygame.display.flip()
        
        # انتظار لمدة 2 ثانية
        start_time = time.time()
        while time.time() - start_time < 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(FPS)

# عرض صورة البداية
show_splash_image()

# الحلقة الرئيسية للعبة
while True:
    # معالجة الأحداث
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # تحكم اللاعب
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += PADDLE_SPEED
    
    # تشغيل الخصم الآلي
    opponent_ai()
    
    # حركة الكرة
    ball_movement()
    
    # الرسم
    draw_objects()
    
    # تحديث الشاشة
    pygame.display.flip()
    clock.tick(FPS)
