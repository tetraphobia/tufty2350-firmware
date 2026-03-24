from badgeware import run

# Constants
BADGE_VIEW = 0
SOCIALS_VIEW = 1
ARTIST_VIEW = 2

# Background Swirlies
CX = screen.width / 2
CY = screen.height / 2

ARMS = 6
SPEED = 0.2
CURVE = 0.1


# Views
current_view = 0
views = {
    io.BUTTON_A: BADGE_VIEW,
    io.BUTTON_B: SOCIALS_VIEW,
    io.BUTTON_C: ARTIST_VIEW,
}

def draw_background(hue=0):
    pass

def draw_badge_view():
    draw_background()

    screen.text("Badge view", 10, 50)

def draw_socials_view():
    draw_background()

    screen.text("Socials view", 10, 50)

def draw_artist_view():
    draw_background()

    screen.text("Artist view", 10, 50)

def update():
    global current_view

    if (len(io.pressed) > 0):
        current_view = views[io.pressed[-1]]

    if current_view == BADGE_VIEW:
        draw_badge_view()
    elif current_view == SOCIALS_VIEW:
        draw_socials_view()
    elif current_view == ARTIST_VIEW:
        draw_artist_view()
    else:
        draw_badge_view()


if __name__ == "__main__":
    run(update)
