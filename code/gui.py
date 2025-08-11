import pygame as pg

pg.init()

clock = pg.time.Clock()
font = pg.font.Font('freesansbold.ttf', 32)


'''
class Interactive():
    
    def __init__(self):
        pass
'''
    
    
class Button():
    
    def __init__(self, display_obj, link, func, width, height, top_left_x, top_left_y, 
                 text, text_font=font, text_color=(0,0,0), color=(230,230,230), highlight_color=(150,150,150), click_color=(255,255,0)):
       
        self.dp = display_obj
        self.link = link
        self.func = func
        
        self.h, self.w = height, width
        self.x, self.y = top_left_x, top_left_y
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.txt, self.txt_col, self.txt_font = text, text_color, text_font
        self.txt_obj = self.txt_font.render(self.txt, True, self.txt_col)
        self.txt_rect = self.txt_obj.get_rect()
        self.txt_rect.center = self.rect.center
        self.col, self.high_col, self.click_col = color, highlight_color, click_color
        
        self.mouse_hover = False
        self.active = False
    
    def draw(self):
        if not self.active:
            if not self.mouse_hover:
                color = self.col
            else:
                color = self.high_col
        else:
            color = self.click_col
        
        pg.draw.rect(self.dp, color, self.rect)
        self.dp.blit(self.txt_obj, self.txt_rect)
    
    def checkMouseHover(self, mousePos: tuple|list) -> bool:
        return self.rect.collidepoint(mousePos)
    
    def checkMouseClick(self, mousePos: tuple|list, mouseClick: bool) -> bool:
        if mouseClick:
            return self.checkMouseHover(mousePos)
        else:
            return False
    
    def reset(self):
        self.mouse_hover = False
        self.active = False

    def routine(self, gui_events):
        for event in gui_events:
            if event.type == pg.MOUSEMOTION:
                if self.checkMouseHover(event.pos):
                    self.mouse_hover = True
                else:
                    self.mouse_hover = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.checkMouseClick(event.pos, True):
                    self.active = True                      # feels useless!
                    self.draw()
                    pg.time.delay(50)
                    self.func()
                    self.reset()
            
                
class EntryField():
    
    def __init__(self, display_object, link, name, width, height, top_left_x, top_left_y, text,
                 text_font=font, text_color=(0,0,0), place_holder_color=(180,180,180), color=(230,230,230),
                 highlight_color=(200,200,200), entried_color=(220,220,0), cursor_color=(0,0,0)):
        
        self.dp = display_object
        self.link = link
        self.name = name
        
        self.h, self.w = height, width
        self.x, self.y = top_left_x, top_left_y
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.txt, self.txt_placeHolder, self.txt_col, self.placeHolder_col, self.txt_font = '', text, text_color, place_holder_color, text_font
        self.txt_obj = self.txt_font.render(self.txt, True, self.txt_col)
        self.txt_rect = self.txt_obj.get_rect(topleft=(self.x + 5, self.y + (self.h - self.txt_font.get_height()) // 2))
        #self.txt_rect = self.txt_obj.get_rect()
        self.cursor = pg.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))
        self.col, self.high_col, self.entr_col, self.cur_col = color, highlight_color, entried_color, cursor_color
        
        self.mouse_hover = False
        self.active = False
        self.filled = False
        self.last_blink_time = 0
        self.blink_interval = 500
        self.cursor_visible = False
        
    def draw(self):
        if not self.active:
            if not self.mouse_hover:
                if not self.filled:
                    color = self.col
                else:
                    color = self.entr_col
            else:
                color = self.high_col      
        else:
            color = self.high_col
        
        if not self.txt and not self.active:
            display_txt = self.txt_placeHolder
            display_col = self.placeHolder_col
        else:
            display_txt = self.txt
            display_col = self.txt_col
        
        pg.draw.rect(self.dp, color, self.rect)
        
        self.txt_obj = self.txt_font.render(display_txt, True, display_col)
        self.txt_rect = self.txt_obj.get_rect(topleft=(self.x + 5, self.y + (self.h - self.txt_font.get_height()) // 2))
        self.cursor = pg.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))
        self.dp.blit(self.txt_obj, self.txt_rect)
        
        if self.active and self.cursor_visible:
            pg.draw.rect(self.dp, self.cur_col, self.cursor)
    
    def checkMouseHover(self, mousePos: tuple|list) -> bool:
        return self.rect.collidepoint(mousePos)
        
    def checkMouseClick(self, mousePos: tuple|list, mouseClick: bool) -> bool:
        if mouseClick:
            return self.checkMouseHover(mousePos)
        else:
            return False
    
    def getText(self):
        return self.txt

    def reset(self):
        self.txt = ''
        self.mouse_hover = False
        self.active = False
        self.filled = False
    
    def routine(self, gui_events):
        for event in gui_events:
            if event.type == pg.MOUSEMOTION:
                if self.checkMouseHover(event.pos):
                    self.mouse_hover = True
                else:
                    self.mouse_hover = False
            
            elif self.active and event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    if not self.txt:
                        self.cursor = pg.Rect((self.x + 5, self.y + (self.h - self.txt_font.get_height()) // 2), (3, self.txt_font.get_height()))
                    self.txt = self.txt[:-1] 
                elif event.key == pg.K_RETURN:
                    self.active = False
                    if self.txt: self.filled = True
                else:
                    self.txt += event.unicode
            
            elif event.type == pg.MOUSEBUTTONDOWN:
                if not self.active and event.button == 1 and self.checkMouseClick(event.pos, True):
                    self.active = True
                    self.cursor_visible = True
                    self.last_blink_time = pg.time.get_ticks()
                elif self.active and not(event.button == 1 and self.checkMouseClick(event.pos, True)):
                    self.active = False
                    if self.txt: self.filled = True
        
        if self.active:
            current_time = pg.time.get_ticks()
            if current_time - self.last_blink_time >= self.blink_interval:
                self.cursor_visible = not self.cursor_visible
                self.last_blink_time = current_time


class Scene():
    
    def __init__(self, link, display_object, caption, icon, bg_image, nodes: list[Button|EntryField], supported_gui_events, graphics_func):
        self.link = link
        
        self.dp = display_object
        #self.w, self.h = width, height
        self.caption = caption
        self.icon = icon
        self.bg_img = bg_image
        self.graphics_func = graphics_func
        
        self.nodes = nodes
        self.supp_gui_events = supported_gui_events
    
    def draw(self):
        pg.display.set_caption(self.caption)
        pg.display.set_icon(self.icon)
        self.dp.blit(self.bg_img, (0, 0))
        self.graphics_func(self.dp)
        
        for node in self.nodes: node.draw()
    
    def routine(self, gui_events):
        events = []
        for event in gui_events:
            if event.type in self.supp_gui_events: events.append(event)
                
        for node in self.nodes: node.routine(events)
        self.draw()                                         # could behave unexpectedly problematically
    
    def reset(self):
        for node in self.nodes: node.reset()
    
    def getText(self):
        txt = {}
        for node in self.nodes:
            if type(node) == EntryField:
                txt[node.name] = node.getText()
    
