import numpy as np
import pygame
from pygame import gfxdraw

# Initial conditions
rinp = input("Enter integer coordinates of r1 in x, y coordinates seperated by space, assuming com as origin :").split(" ")
r01 = np.array([int(rinp[0]), int(rinp[1])])

Rinp= input("Enter the radii for the two planets: ").split(" ")
R1,R2 = int(Rinp[0]),int(Rinp[1])

massin = input("Enter mass of both the objects seperated by space :").split(" ")
m1, m2 = int(massin[0]), int(massin[1])

vinp = input("Enter velocitiy vector of r1 in x, y coordinates seperated by space, assuming com as origin :").split(" ")
v01 = np.array([float(vinp[0]), float(vinp[1])])

r02 = -m1 / m2 * r01
v02 = -m1 / m2 * v01

Trail=input("Do you want a decaying trail or a constant trail or no trail to be shown (DecTrail/Trail/No) :")

GravConst=2000000

def acceleration(r1, r2, m1, m2):
    rel_pos = r2 - r1
    dist = np.linalg.norm(rel_pos)
    acc1 = GravConst * m2 * rel_pos / dist**3
    acc2 = -GravConst * m1 * rel_pos / dist**3
    return acc1, acc2

def velocity_verlet_step(r1, v1, r2, v2, m1, m2, dt):
    a1, a2 = acceleration(r1, r2, m1, m2)
    r1_new = r1 + v1 * dt + 0.5 * a1 * dt**2
    r2_new = r2 + v2 * dt + 0.5 * a2 * dt**2
    a1_new, a2_new = acceleration(r1_new, r2_new, m1, m2)
    v1_new = v1 + 0.5 * (a1 + a1_new) * dt
    v2_new = v2 + 0.5 * (a2 + a2_new) * dt
    return r1_new, v1_new, r2_new, v2_new

def search_min_safe_velocity(r01, m1, m2, G, dt, max_time, collision_distance):
    direction = np.array([-r01[1], r01[0]], dtype=np.float64)
    direction /= np.linalg.norm(direction)
    r02 = -m1 / m2 * r01

    def simulate(v_mag):
        v01 = v_mag * direction
        v02 = -m1 / m2 * v01
        r1, r2 = np.copy(r01), np.copy(r02)
        v1, v2 = np.copy(v01), np.copy(v02)

        steps = int(max_time / dt)
        for _ in range(steps):
            r1, v1, r2, v2 = velocity_verlet_step(r1, v1, r2, v2, m1, m2, dt)
            if np.linalg.norm(r1 - r2) < collision_distance:
                return False 
        return True 

    v_low = 0.0
    r = np.linalg.norm(r01 - r02)
    v_high = np.sqrt((G * (m1 + m2) / r) * 2)
    tolerance = 1e-3
    safe_v = None

    while v_high - v_low > tolerance:
        v_mid = (v_low + v_high) / 2
        if simulate(v_mid):
            safe_v = v_mid
            v_high = v_mid
        else:
            v_low = v_mid

    return safe_v

collision_distance = 10 * (R1 + R2)
v_safe = search_min_safe_velocity(r01, m1, m2, GravConst, dt=1/60, max_time=20, collision_distance=collision_distance)
print(f"Minimum velocity magnitude to avoid collision: {v_safe:.3f}")

direction = np.array([-r01[1], r01[0]])
direction = direction / np.linalg.norm(direction)
v_01 = v_safe * direction
v_02 = -m1 / m2 * v_01
print("The threshold velocity to prevent collision is the vector :",v_01)

v_esc = np.sqrt((2*GravConst*(m1+m2)/(np.linalg.norm(r01 - r02))))
v_esc1 = v_esc * direction
v_esc2 = -m1 / m2 * v_esc1
print("The escape velocity for m1 for this system is the vector :",v_esc1)

pygame.init()
WIDTH, HEIGHT = 1920, 1080
CENTER = np.array([WIDTH // 2, HEIGHT // 2])
screen = pygame.display.set_mode((WIDTH, HEIGHT), 528)
clock = pygame.time.Clock()

FPS=165
dt = 1 / FPS

r1 = r01
r2 = r02
v1 = v01
v2 = v02
r1s = [r1]
r2s = [r2]

running = True
paused = False   # <---- NEW pause flag
collided = False

while running:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:   # <---- SPACE toggles pause
                paused = not paused

    if not paused:  # <---- Skip updates if paused
        if not collided and np.linalg.norm(r1 - r2) < 10 * (R1+R2):
            collided = True

        if not collided:
            r1, v1, r2, v2 = velocity_verlet_step(r1, v1, r2, v2, m1, m2, dt)
            mu = (m1 * m2) / (m1 + m2)
            rel_vel = v1 - v2
            rel_pos = r1 - r2
            kinetic = 0.5 * mu * np.dot(rel_vel, rel_vel)
            potential = -GravConst * m1 * m2 / np.linalg.norm(rel_pos)
            energy=kinetic+potential
            print(f"Relative Energy: {energy:.2f}")

            MAX_TRAIL = 300 
            r1s.append(r1)
            r2s.append(r2)
            if len(r1s) > MAX_TRAIL:
                r1s.pop(0)
                r2s.pop(0)

    # Draw trails
    for i in range(len(r1s)):
        if Trail=="DecTrail":
            fade = int(255 * np.exp(-0.01 * (len(r1s) - i - 1)))
            fade = max(1, fade) 
            pygame.gfxdraw.filled_circle(screen, int((r1s[i] + CENTER)[0]), int((r1s[i] + CENTER)[1]), int(8*R1), (fade, 0, 0))
            pygame.gfxdraw.filled_circle(screen, int((r2s[i] + CENTER)[0]), int((r2s[i] + CENTER)[1]), int(8*R2), (0, fade, 0))
        elif Trail=="Trail":
            pygame.gfxdraw.filled_circle(screen, int((r1s[i] + CENTER)[0]), int((r1s[i] + CENTER)[1]), int(8*R1), (150, 0, 0)) 
            pygame.gfxdraw.filled_circle(screen, int((r2s[i] + CENTER)[0]), int((r2s[i] + CENTER)[1]), int(8*R2), (0, 150, 0)) 

    # Draw planets
    pygame.gfxdraw.filled_circle(screen , int((r1s[-1] + CENTER)[0]), int((r1s[-1] + CENTER)[1]), int(10 * R1), (255, 0, 255))
    pygame.gfxdraw.filled_circle(screen, int((r2s[-1] + CENTER)[0]), int((r2s[-1] + CENTER)[1]), int(10 * R2), (0, 0, 255))

    pygame.display.flip()
    # clock.tick(FPS)

pygame.quit()
