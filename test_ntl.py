import ntl_iface
import time
import pygame

NTL_SIZE = (24,30)
DEBUG_SIZE = (24*20,30*20)
FONT_SIZE = 10

pygame.init()
ntl = ntl_iface.NTL()

screen = pygame.display.set_mode( DEBUG_SIZE )
bg = pygame.Surface( NTL_SIZE )

font = pygame.font.match_font('arial')
text_font = pygame.font.Font(font, FONT_SIZE)
m_bot = text_font.render("     I blame Kean Maizels", True, (255,0,0)) 
m_top = text_font.render("     www.kean.com.au", True, (0,255,0)) 

m_top_rot = pygame.transform.rotate(m_top, 270)
m_bot_rot = pygame.transform.rotate(m_bot, 270)

"""
if m_top.get_rect()[2] > m_bot.get_rect()[2]:
  width = m_top.get_rect()[2]
else:
  width = m_bot.get_rect()[2]

left = 0
for x in range(width):
  bg.fill((0,0,0))  
  bg.blit(m_top, (left,0))
  bg.blit(m_bot, (left,15))
  pygame.transform.scale(bg, DEBUG_SIZE, screen)
  pygame.display.update()
  ntl.draw_surface(bg)
  left = left - 1
  time.sleep(0.1)

left = 0
for x in range(width):
  bg.fill((0,0,0))  
  bg.blit(m_top_rot, (0,left))
  bg.blit(m_bot_rot, (12,left))
  pygame.transform.scale(bg, DEBUG_SIZE, screen)
  pygame.display.update()
  ntl.draw_surface(bg)
  left = left - 1
  time.sleep(0.1)


img = pygame.image.load("test_img/chick.jpg")
ntl.draw_surface(img)
time.sleep(10)

img = pygame.image.load("test_img/kitty.jpg")
ntl.draw_surface(img)
time.sleep(10)

img = pygame.image.load("test_img/paw.jpg")
ntl.draw_surface(img)
time.sleep(10)
"""


font = pygame.font.match_font('courier new')
text_font = pygame.font.Font(font, 24)
m_top = text_font.render("   www.robodino.org   ", True, (0,0,255)) 

m_top_rot = pygame.transform.rotate(m_top, 270)
left = 0

width = m_top.get_rect()[2]

for x in range(width):
  bg.fill((0,0,0))  
  bg.blit(m_top_rot, (0,left))
  pygame.transform.scale(bg, DEBUG_SIZE, screen)
  pygame.display.update()
  ntl.draw_surface(bg)
  left = left - 1
  time.sleep(0.1)
  
