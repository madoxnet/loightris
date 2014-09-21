#!/bin/python

import pygame
import ntl_iface
import ntl_tetris
import ntl_iface
import Queue
import threading

#DDR "Joystick" definitions
DDR_LEFT     = 0
DDR_DOWN     = 1
DDR_UP       = 2
DDR_RIGHT    = 3
DDR_SQUARE   = 4
DDR_TRIANGLE = 5
DDR_X        = 6
DDR_O        = 7
DDR_SELECT   = 8
DDR_START    = 9

#Winning Condition
MAX_SCORE_DIFF = 1000

T1_ORIGIN = (13,9)
T2_ORIGIN = (1,9)

t1_input  = Queue.Queue()
t1_signal = Queue.Queue()

t2_input  = Queue.Queue()
t2_signal = Queue.Queue()

update_event = pygame.USEREVENT + 1
t1_event     = pygame.USEREVENT + 2
t2_event     = pygame.USEREVENT + 3
    
#Initialise pygame
pygame.init()

try:
  joy = pygame.joystick.Joystick(0)
  joy.init()
except:
  pass
  
try:
  ntl = ntl_iface.NTL()
except:
  pass

t1 = ntl_tetris.Tetris(t1_event, t1_input, t1_signal)
t2 = ntl_tetris.Tetris(t2_event, t2_input, t2_signal)
t1.setDaemon(True)
t2.setDaemon(True)
t1.start()
t2.start()


screen = pygame.display.set_mode((24*20, 30*20))
outputsurface = pygame.Surface( (24,30) )
tetris_borders = pygame.Surface( (24,30) )
win_surface = pygame.Surface( (10,20) )
lose_surface = pygame.Surface( (10,20) )
score_diff = 0

pts = [(0,8),
       (0,29),
       (11,29),
       (11,8),
       (12,8),
       (12,29),
       (23,29),
       (23,8)]
pygame.draw.lines(tetris_borders, (10,50,50), True, pts)
font = pygame.font.match_font('courier new')
text_font = pygame.font.Font(font, 11)
text = text_font.render("RnD", False, (255,0,0))
tetris_borders.blit(text,(2,-2))
text_font = pygame.font.Font(font, 14)
text = text_font.render("W", True, (0,0,255))
win_surface.fill((0,255,0))
win_surface.blit(text, (0,3))
text = text_font.render("L", True, (255,255,0))
lose_surface.fill((127,0,0))
lose_surface.blit(text, (0,3))

#Set the timer for input_events
pygame.time.set_timer(update_event, 100)

while True:
  event = pygame.event.wait()
  if event.type == pygame.QUIT:
    break
  elif event.type == pygame.KEYDOWN:
    if event.key == pygame.K_LEFT:
      t1_input.put("left")
      t1_input.join()
    elif event.key == pygame.K_RIGHT:
      t1_input.put("right")
      t1_input.join()
    elif event.key == pygame.K_UP:
      t1_input.put("rot_r")
      t1_input.join()
    elif event.key == pygame.K_DOWN:
      t1_input.put("down")
      t1_input.join()
    if event.key == pygame.K_a:
      t2_input.put("left")
      t2_input.join()
    elif event.key == pygame.K_d:
      t2_input.put("right")
      t2_input.join()
    elif event.key == pygame.K_w:
      t2_input.put("rot_r")
      t2_input.join()
    elif event.key == pygame.K_s:
      t2_input.put("down")
      t2_input.join()
    elif event.key == pygame.K_RETURN:
      if t1.is_dead() and t2.is_dead():
        t1_input.put("new_g")
        t1_input.join()
        t2_input.put("new_g")
        t2_input.join()
    else:
      pass
  # Check for a key push by the user
  elif event.type == pygame.JOYBUTTONDOWN:
    if event.button == DDR_SQUARE:
      t1_input.put("left")
      t1_input.join()
    elif event.button == DDR_O:
      t1_input.put("right")
      t1_input.join()
    elif event.button == DDR_UP :
      t1_input.put("rot_r")
      t1_input.join()
    elif event.button == DDR_RIGHT:
      t1_input.put("down")
      t1_input.join()
    if event.button == DDR_X:
      t2_input.put("left")
      t2_input.join()
    elif event.button == DDR_TRIANGLE:
      t2_input.put("right")
      t2_input.join()
    elif event.button == DDR_DOWN :
      t2_input.put("rot_r")
      t2_input.join()
    elif event.button == DDR_LEFT:
      t2_input.put("down")
      t2_input.join()
    elif event.button == DDR_START:
      if t1.is_dead() and t2.is_dead():
        t1_input.put("new_g")
        t1_input.join()
        t2_input.put("new_g")
        t2_input.join()
  elif event.type == t1_event:
    t1_input.put("down")
    t1_input.join()
  elif event.type == t2_event:
    t2_input.put("down")
    t2_input.join()
  elif event.type == update_event:
    outputsurface.fill((0,0,0))
    outputsurface.blit(tetris_borders,(0,0))
    if not t1.is_dead() and not t2.is_dead():
      score_diff = t1.get_score() - t2.get_score()
    #11 is the max
    score_bar = 11 * score_diff / MAX_SCORE_DIFF
    #Hack clear line
    pygame.draw.line(tetris_borders, (0,0,0), (0,7), (23,7)) 
    if (score_diff > 0):
      pygame.draw.line(tetris_borders, (255,255,0), (12,7), (12+score_bar,7)) 
    elif (score_diff < 0):
      pygame.draw.line(tetris_borders, (255,255,0), (11,7), (11+score_bar,7)) 
    else:
      pass
    if (abs(score_diff) >= MAX_SCORE_DIFF) or t1.is_dead() or t2.is_dead():
      if not t1.is_dead() and t2.is_dead():
        print "T2 Died first"
        score_diff = MAX_SCORE_DIFF
      elif t1.is_dead() and not t2.is_dead():
        print "T1 Died first"
        score_diff = -MAX_SCORE_DIFF
      
      if t1.is_dead() and t2.is_dead():
        #Game has already been ended before
        pass
      else:
        print "Won, score diff %d" % score_diff
        #Someone has won, end the games
        t1.game_over()
        t2.game_over()
      #Draw the winner and scorebar
      if (score_diff > 0):
        #Player 1 Won
        outputsurface.blit(win_surface, T1_ORIGIN)
        outputsurface.blit(lose_surface, T2_ORIGIN)
      elif (score_diff < 0):
        #Player 2 Won
        outputsurface.blit(lose_surface, T1_ORIGIN)
        outputsurface.blit(win_surface, T2_ORIGIN)      
      else:
        #Both suck
        outputsurface.blit(lose_surface, T1_ORIGIN)
        outputsurface.blit(lose_surface, T2_ORIGIN)
    else:
      #Draw game surfaces
      outputsurface.blit(t2.get_surface(), T2_ORIGIN)
      outputsurface.blit(t1.get_surface(), T1_ORIGIN)

    pygame.transform.scale(outputsurface, (20*24,20*30), screen)
    pygame.display.update()

    try:
      #outputsurface = pygame.transform.rotate(outputsurface, 180)
      ntl.draw_surface(outputsurface)
    except:
      pass


