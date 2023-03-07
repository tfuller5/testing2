import pygame
import random
import time



class chatbox:
    def __init__(self):
        self.activated = False
        self.message = []
        self.actual = ""
        self.upto = ""
        self.cursor = -1
        self.updated()

    def updated(self):
        self.actual = font.render("What are you thinking right now?: "+"".join(self.message), True, Blue)
        self.upto = font.render("What are you thinking right now?: "+"".join(self.message[:self.cursor + 1]), True, Blue)

    def is_active(self):
        return self.activated

    def activate(self):
        self.activated = True

    def deactivate(self):
        self.activated = False

    def reset(self):
        self.cursor = -1
        self.message = []

    def send_key(self, event):
        if event.key == pygame.K_RETURN:
            final_message = "".join(self.message)
            self.deactivate()
            self.reset()
            self.updated()
            return final_message

        elif event.key == pygame.K_LEFT:
            if self.cursor >= 0:
                self.cursor = self.cursor - 1
            self.updated()

        elif event.key == pygame.K_RIGHT:
            if self.cursor < len(self.message) - 1:
                self.cursor = self.cursor + 1
            self.updated()

        elif event.key == pygame.K_BACKSPACE:
            if self.message != [] and self.cursor != -1:
                self.message.pop(self.cursor)
                self.cursor -= 1
                self.updated()
        elif event.unicode != "":
            self.cursor = self.cursor + 1
            self.message.insert(self.cursor, event.unicode)
            self.updated()

pygame.init()
screen_size = (1200, 700)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
cloud_img = pygame.image.load("cloud1.png")
cloud_size = cloud_img.get_size()
cloud_img = pygame.transform.scale(cloud_img, [xy//1.2 for xy in cloud_size])
cloud_size = cloud_img.get_size()
fps = 30
CLOUD_EVERY_N_SECONDS = 1




# Define colors
bg = (150, 200, 200)
RED = (255, 100, 100)
DARK_RED = (139, 0, 0)
Blue = (0, 0, 255)

# Define fonts
font = pygame.font.Font(None, 30)

chat = chatbox()


# Create the button surface
button = pygame.Surface((300, 50))
button.fill(RED)
button_rect = button.get_rect()
button_rect.center = (screen_size[0]//2, 50)

# Create the button text
button_text = font.render("XXX Stop Thinking XXX", True, DARK_RED)
button_text_rect = button_text.get_rect()
button_text_rect.center = button_rect.center
thoughts = []

# Set up the fade time
fade_time = 5  # 5 seconds

class game:
    fade_text_rect = None
    fade_start_time = None
    fade_text = None
#cloud_img = pygame.transform.scale(cloud_img, [x//5 for x in cloud_img.get_size()])

class cloud:
    def __init__(self, possible_ys, message = None):
        self.x = -cloud_size[0]
        self.y = random.choice(list(possible_ys))
        self.vx = 1.5 + random.randint(-5, 5)/10
        self.vy = random.randint(-10, 10)/100
        self.held = False
        if message is None:
            self.message = message
        else:
            self.message = self.message_lines(message)

    def message_lines(self, thought):
        lines = []
        cut_off = 20
        y = 0
        while len(thought) > 0:
            y = y + 20
            if " " not in thought[cut_off:]:
                gap = len(thought)
            else:
                gap = thought[cut_off:].index(" ") + cut_off
            before = thought[:gap]
            thought = thought[gap:]
            lines.append((y, font.render(before, True, (64, 64, 64))))

        return lines


    def move(self):
        if self.held:
            return
        self.x += self.vx
        self.y += self.vy

        if self.x > screen_size[0]:
            clouds.clouds.remove(self)

    def at(self):
        return (self.x, self.y)

    def clicked(self, pos):
        if pygame.Rect(self.x, self.y, cloud_size[0], cloud_size[1]).collidepoint(pos[0], pos[1]):
            return True
        else:
            return False


class clouds:
    clouds = []

    @staticmethod
    def new_cloud(thought = None):
        possible_ys = set(range(10, screen_size[1] - cloud_size[1]))
        for c in clouds.clouds_on_screen():
            possible_ys = possible_ys.difference(set(range(int(c.y) - cloud_size[1] - 10, int(c.y) + cloud_size[1] + 10)))
        if possible_ys != set():
            clouds.clouds.append(cloud(possible_ys, thought))
            return True
        return False

    @staticmethod
    def clouds_on_screen():
        return [c for c in clouds.clouds if c.x < 30]

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for c in clouds.clouds:
                c.held = False

            if button_rect.collidepoint(event.pos):
                # Create the fading text
                game.fade_start_time = time.time()
                game.fade_text = font.render("Sorry, That's impossible!!!", True, DARK_RED)
                game.fade_text_rect = game.fade_text.get_rect()
                game.fade_text_rect.center = (
                    button_rect.centerx + random.randint(-200, 100),
                    button_rect.centery + random.randint(50, 100))

        if event.type == pygame.KEYDOWN:
            done = chat.send_key(event)
            if done is not None:
                thoughts.append(done)



    if pygame.mouse.get_pressed()[0]:
        for c in clouds.clouds[::-1]:
            c.held = False
            pos = pygame.mouse.get_pos()
            if c.clicked(pos):
                colour = screen.get_at((pos[0], pos[1]))
                if colour[:3] != bg:
                    c.held = True
                    break

    return True


def draw_everything():
    screen.fill(bg)
    for c in clouds.clouds:
        screen.blit(cloud_img, c.at())

        if c.message != None:
            for yplus, line in c.message:
                r = line.get_rect()
                r.center = (c.x + cloud_size[0] //2 , c.y + 30 + yplus)
                screen.blit(line, r)


        # Draw the button
    screen.blit(button, button_rect)
    screen.blit(button_text, button_text_rect)

    screen.blit(chat.actual, (20, screen_size[1] - 30))

    arrow_x = 20 + chat.upto.get_size()[0]
    arrow_y = screen_size[1] - 40
    arrow_width = 20
    arrow_height = 30
    arrow_points = [(arrow_x - arrow_width // 2, arrow_y - arrow_height // 2),
                    (arrow_x + arrow_width // 2, arrow_y - arrow_height // 2),
                    (arrow_x, arrow_y + arrow_height // 2)]
    pygame.draw.polygon(screen, (0, 0, 255), arrow_points)

    # Draw the fading text
    if game.fade_start_time is not None:
        if time.time() - game.fade_start_time < fade_time:
            alpha = int((1 - (time.time() - game.fade_start_time) / fade_time) * 255)
            game.fade_text.set_alpha(alpha)
            screen.blit(game.fade_text, game.fade_text_rect)
        else:
            game.fade_start_time = None
        

    pygame.display.flip()

def frame_actions():
    if pygame.time.get_ticks() % (fps * CLOUD_EVERY_N_SECONDS) == 0:
        if len(thoughts) > 0:

            if clouds.new_cloud(thoughts[-1]):
                thoughts.pop()
        else:
            clouds.new_cloud()

    for c in clouds.clouds:
        c.move()

while handle_events():
    frame_actions()
    draw_everything()
    clock.tick(fps)