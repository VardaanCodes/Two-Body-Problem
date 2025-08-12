# standard packages
import pygame as pg
import sys
import os
# custom packages
import gui
# import numerical as num

script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
pg.init()


# keeping track of state of app
link = 'home-screen/'
link_prev = 'home-screen/'


font = pg.font.Font('freesansbold.ttf', 32)
font_small = pg.font.Font('freesansbold.ttf', 20)
screen_width, screen_height = 1200, 750
app = {'name': '2-Body Gravity Simulator',
       'logo': pg.image.load(os.path.join(script_dir, 'data/logo.png'))}


dp = pg.display.set_mode(size=(screen_width, screen_height))
pg.display.set_caption(app['name'])
pg.display.set_icon(app['logo'])


# home_screen
def hs_graphics_func(dp):
    dp.blit(pg.font.Font(None, 70).render(
        "Two-Body Gravity Simulation", True, (255, 255, 255)), (240, 50))
    dp.blit(pg.font.Font(None, 40).render(
        "enter the initial conditions for both masses 1 and 2", True, (255, 255, 255)), (240, 130))


def hs_info():
    global link, link_prev
    link_prev = link
    link = 'home-screen/info-win/'


def hs_simulate():
    global link, link_prev
    txt = states[link].getText()

    link_prev = link
    link = 'home-screen/simulation-win/'


hs_nodes = [gui.Button(dp, 'home-screen/', hs_info, 100, 35, 1080, 20, 'INFO'),
            gui.EntryField(dp, 'home-screen/', 'm1', 333, 35, 50, 190, 'm1'),
            gui.EntryField(dp, 'home-screen/', 'x1', 333, 35, 50, 255, 'x1'),
            gui.EntryField(dp, 'home-screen/', 'y1', 333, 35, 50, 320, 'y1'),
            gui.EntryField(dp, 'home-screen/', 'v1_x',
                           333, 35, 50, 385, 'v1_x'),
            gui.EntryField(dp, 'home-screen/', 'v1_y',
                           333, 35, 50, 450, 'v1_y'),
            gui.EntryField(dp, 'home-screen/', 'radius_1',
                           333, 35, 50, 515, 'radius_1'),
            gui.EntryField(dp, 'home-screen/', 'm2', 333, 35, 433, 190, 'm2'),
            gui.EntryField(dp, 'home-screen/', 'x2', 333, 35, 433, 255, 'x2'),
            gui.EntryField(dp, 'home-screen/', 'y2', 333, 35, 433, 320, 'y2'),
            gui.EntryField(dp, 'home-screen/', 'v2_x',
                           333, 35, 433, 385, 'v2_x'),
            gui.EntryField(dp, 'home-screen/', 'v2_y',
                           333, 35, 433, 450, 'v2_y'),
            gui.EntryField(dp, 'home-screen/', 'radius_2',
                           333, 35, 433, 515, 'radius_2'),
            gui.Button(dp, 'home-screen/', hs_simulate, 333, 35, 241.5, 580, 'SIMULATE!')]

hs_supp_gui_events = [pg.KEYDOWN, pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN]


# simulation-win
def sw_graphics_func(dp):
    txt = 'Live Data'
    txt_obj = font_small.render(txt, True, (255, 255, 255))
    txt_rect = txt_obj.get_rect()
    txt_rect.center = (screen_width//2, screen_height//2)
    dp.blit(txt_obj, txt_rect)


sw_nodes = []

sw_supp_gui_events = [pg.KEYDOWN, pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN]


# info-win
def iw_graphics_func(dp):
    txt = '''
                                      ==========================
                                        Two-Body Gravity Simulator
                                      ==========================

OVERVIEW
--------
This application simulates the orbital interaction between two point masses under
Newtonian gravity in Center of Mass frame. The simulation uses the velocity-Verlet
method for accuracy, and is visualized using Pygame.

INPUT INSTRUCTIONS
------------------
You will be prompted for several parameters in the console before the simulation starts:-
Masses m1, m2, Positions x1, y1, x2, y2, Velocities vx1, vx2, vy1, vy2 and Radii of two bodies
Also for trail visibilty, input:    1)DecTrail: trail fades over time
                                    2)Trail: persistent trail
                                    3)No: no trail shown

SIMULATION WINDOW
-----------------
--- Data Box: Shows live data (m1, m2, v1, v2, x1, x2) with corresponding planet images
--- Simulation Window: Displays planet images, velocity vectors, and full trails with
                     transparency as per algorithm
--- Control Box: Separate Pause/Resume, Reset buttons, Modify parameters instantaneously
--- Modify Live Parameters Functionality:
        Allows the user to pause the simulation to update the masses, velocities, and
        positions of the bodies in real time. Once changes are applied, the simulation
        resumes with the new parameters, enabling dynamic adjustment without restarting.
'''
    txt_obj = font_small.render(txt, True, (255, 255, 255))
    txt_rect = txt_obj.get_rect()
    txt_rect.center = (screen_width//2, screen_height//2)
    dp.blit(txt_obj, txt_rect)


def iw_back():
    global link, link_prev
    link_prev = link
    link = 'home-screen/'


iw_nodes = [gui.Button(dp, 'home-screen/info-win/',
                       iw_back, 100, 35, 1080, 20, 'BACK')]

iw_supp_gui_events = [pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN]


# control-box-win
def cbw_graphics_func():
    pass


cbw_nodes = []

cbw_supp_gui_events = [pg.KEYDOWN, pg.MOUSEMOTION, pg.MOUSEBUTTONDOWN]


# capsuled data

home_screen = {'link': 'home-screen/', 'caption': '2-Body Gravity Simulator', 'icon': pg.image.load(os.path.join(script_dir, 'data/logo.png')),
               'bg_img': pg.image.load(os.path.join(script_dir, "data/home-screen-bg.png")), 'graphics_func': hs_graphics_func,
               'nodes': hs_nodes, 'supp_gui_events': hs_supp_gui_events}

simulation_win = {'link': 'home-screen/simulation-win/', 'caption': '2-Body Gravity Simulator', 'icon': pg.image.load(os.path.join(script_dir, 'data/logo.png')),
                  'bg_img': pg.image.load(os.path.join(script_dir, "data/simulation-win-bg.png")), 'graphics_func': sw_graphics_func,
                  'nodes': sw_nodes, 'supp_gui_events': sw_supp_gui_events}

controlBox_win = {'link': 'home-screen/simulation-win/control-box-win/', 'caption': 'Control Box: modify parameters instantaneously',
                  'icon': pg.image.load(os.path.join(script_dir, 'data/control-box-icon.png')),
                  'bg_img': pg.image.load(os.path.join(script_dir, "data/control-box-win-bg.png")), 'graphics_func': cbw_graphics_func,
                  'nodes': cbw_nodes, 'supp_gui_events': cbw_supp_gui_events}

info_win = {'link': 'home-screen/info-win/', 'caption': 'info & instructions', 'icon': pg.image.load(os.path.join(script_dir, 'data/info-icon.png')),
            'bg_img': pg.image.load(os.path.join(script_dir, "data/info-win-bg.jpg")), 'graphics_func': iw_graphics_func,
            'nodes': iw_nodes, 'supp_gui_events': iw_supp_gui_events}

scenes = [home_screen, simulation_win, controlBox_win, info_win]


states = {}
for scene in scenes:
    states[scene['link']] = gui.Scene(scene['link'], dp, scene['caption'], scene['icon'], scene['bg_img'],
                                      scene['nodes'], scene['supp_gui_events'], scene['graphics_func'])


clock = pg.time.Clock()
while True:
    if link != link_prev:
        states[link_prev].reset()
        link_prev = link
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        else:
            states[link].routine([event])
    pg.event.clear()

    pg.display.update()
