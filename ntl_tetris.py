# Tetris Library for NTLight
#
# "Nintendo Rotation System" for Tetris (Game Boy) [Left-handed]
#
#
"""
Written as an exercise in self torture as there are examples out there
that complete this in 50 lines of code.  No, not really, written from
basics to allow for 
- Nintendo rotation system
- Ease to export to LED pixels
- Exercise to make 'easy' to read Tetris implementation.
  
Right x
Down y
"""

import pygame
import random
import threading

class Tetris( threading.Thread ):
  # Tetris
   
  def __init__(self, timerevent, input_queue, signal_queue, width=10, height=20):    
    self.input_queue  = input_queue
    self.signal_queue = signal_queue
    self.timerevent = timerevent
        
    #Set up game dimensions
    self.width = width
    self.height = height
    
    self.input_speed = 200
    self.drop_speed = 600
    
    self.surface = pygame.Surface( (width, height) )
    
    self.lines_cleared = 0
      
    #Define tetromino colours
    self.colours = [
      (0,0,0),
      (0,255,255), #(1)-I-Cyan
      (255,255,0), #(2)-O-Yellow
      (0,0,255),   #(3)-J-Blue
      (255,165,0), #(4)-L-Orange
      (0,255,0),   #(5)-S-Green
      (255,0,0),   #(6)-Z-Red
      (170,0,255)  #(7)-T-Purple
    ]
    
    #Define tetromino shapes
    self.tetrominoes = [
      [ 
        # Dummy(0)
        # Just so the tetrominoes can be indexed from 1-7
      ],
      [
        # 'I' (1)
        # .... .x.. .... .x..
        # .... .x.. .... .x..
        # xxxx .x.. xxxx .x..
        # .... .x.. .... .x..
        [
          [0,1,2,3],  #I-X-R0
          [2,2,2,2]   #I-Y-R0
        ],
        [
          [1,1,1,1],  #I-X-R1
          [0,1,2,3]   #I-Y-R1
        ],
        [
          [0,1,2,3],  #I-X-R2
          [2,2,2,2]   #I-Y-R2
        ],
        [
          [1,1,1,1],  #I-X-R3
          [0,1,2,3]   #I-Y-R3
        ]
      ],
      [
        # 'O' (2)
        # .... .... .... ....
        # .xx. .xx. .xx. .xx.
        # .xx. .xx. .xx. .xx.
        # .... .... .... ....
        [
          [1,2,1,2],  #O-X-R0
          [1,1,2,2]   #O-Y-R0
        ],
        [
          [1,2,1,2],  #O-X-R1
          [1,1,2,2]   #O-Y-R1
        ],
        [
          [1,2,1,2],  #O-X-R2
          [1,1,2,2]   #O-Y-R2
        ],
        [
          [1,2,1,2],  #O-X-R3
          [1,1,2,2]   #O-Y-R3
        ]
      ],
      [
        # 'J' (3)
        # ... .x. x.. .xx
        # xxx .x. xxx .x.
        # ..x xx. ... .x.
        [
          [0,1,2,2],  #J-X-R0
          [1,1,1,2]   #J-Y-R0
        ],
        [
          [1,1,0,1],  #J-X-R1
          [0,1,2,2]   #J-Y-R1
        ],
        [
          [0,0,1,2],  #J-X-R2
          [0,1,1,1]   #J-Y-R2
        ],
        [
          [1,2,1,1],  #J-X-R3
          [0,0,1,2]   #J-Y-R3
        ]
      ],
      [
        # 'L' (4)
        # ... xx. ..x .x.
        # xxx .x. xxx .x.
        # x.. .x. ... .xx
        [
          [0,1,2,0],  #L-X-R0
          [1,1,1,2]   #L-Y-R0
        ],
        [
          [0,1,1,1],  #L-X-R1
          [0,0,1,2]   #L-Y-R1
        ],
        [
          [2,0,1,2],  #L-X-R2
          [0,1,1,1]   #L-Y-R2
        ],
        [
          [1,1,1,2],  #L-X-R3
          [0,1,2,2]   #L-Y-R3
        ]
      ],
      [
        # 'S' (5)
        # ... x.. ... x..
        # .xx xx. .xx xx.
        # xx. .x. xx. .x.
        [
          [1,2,0,1],  #S-X-R0
          [1,1,2,2]   #S-Y-R0
        ],
        [
          [0,0,1,1],  #S-X-R1
          [0,1,1,2]   #S-Y-R1
        ],
        [
          [1,2,0,1],  #S-X-R2
          [1,1,2,2]   #S-Y-R2
        ],
        [
          [0,0,1,1],  #S-X-R3
          [0,1,1,2]   #S-Y-R3
        ]
      ],
      [
        # 'Z' (6)
        # ... .x. ... .x.
        # xx. xx. xx. xx.
        # .xx x.. .xx x..
        [
          [0,1,1,2],  #Z-X-R0
          [1,1,2,2]   #Z-Y-R0
        ],
        [
          [1,0,1,0],  #Z-X-R1
          [0,1,1,2]   #Z-Y-R1
        ],
        [
          [0,1,1,2],  #Z-X-R2
          [1,1,2,2]   #Z-Y-R2
        ],
        [
          [1,0,1,0],  #Z-X-R3
          [0,1,1,2]   #Z-Y-R3
        ]
      ],
      [
        # 'T' (7)
        # ... .x. .x. .x.
        # xxx xx. xxx .xx
        # .x. .x. ... .x.
        [
          [0,1,2,1],  #T-X-R0
          [1,1,1,2]   #T-Y-R0
        ],
        [
          [1,0,1,1],  #T-X-R1
          [0,1,1,2]   #T-Y-R1
        ],
        [
          [1,0,1,2],  #T-X-R2
          [0,1,1,1]   #T-Y-R2
        ],
        [
          [1,1,2,1],  #T-X-R3
          [0,1,1,2]   #T-Y-R3
        ]
      ]
    ]
    
    self.sounds = {}
    
    #Background Music Sounds
    self.sounds["bgm-a"]    = pygame.mixer.Sound("./ogg/bgm-a.ogg")
    self.sounds["bgm-b"]    = pygame.mixer.Sound("./ogg/bgm-b.ogg")
    self.sounds["bgm-c"]    = pygame.mixer.Sound("./ogg/bgm-c.ogg")
    for sound in self.sounds:
      self.sounds[sound].set_volume(0.5)

    #Game Sounds
    self.sounds["4line"]    = pygame.mixer.Sound("./ogg/4line.ogg")
    self.sounds["lineclear"]= pygame.mixer.Sound("./ogg/lineclear.ogg")
    self.sounds["lock"]     = pygame.mixer.Sound("./ogg/lock.ogg")
    self.sounds["move"]     = pygame.mixer.Sound("./ogg/move.ogg")
    self.sounds["newlevel"] = pygame.mixer.Sound("./ogg/newlevel.ogg")
    self.sounds["rotate"]   = pygame.mixer.Sound("./ogg/rotate.ogg")
    self.sounds["gameover"] = pygame.mixer.Sound("./ogg/gameover.ogg")
    self.sounds["hiscore"]  = pygame.mixer.Sound("./ogg/hiscore.ogg")
    
    #Initialize the play grid
    self.play_grid = []
    self.empty_block = [0]
    self.empty_row = self.width * self.empty_block
    for x in range(self.height):
      self.play_grid.append(list(self.empty_row))
    
    self.piece       = 1
    self.rot_current = 0
    self.rot_target  = 0
    self.pos_current = [4,-5] #Start in a hidden location
    self.pos_target  = [0,0]
    
    self.level = -1
    self.score = 0
    self.tetris_last = True
    threading.Thread.__init__( self )
    
  def game_over(self):
    print "Game Over"
    print "Score", self.score
    print "Level", self.level
    print "Lines", self.lines_cleared
    self.level = -1
    pygame.time.set_timer(self.timerevent, 0)
    
    self.sounds["gameover"].play()
    self.sounds["bgm-a"].stop()

  def is_dead(self):
    if self.level < 0:
      return True

  def new_game(self):
    for x in range(self.height):
      self.delete_row(self.height-1)
    #Restart Levels
    self.level = 1
    #Reset Speed
    pygame.time.set_timer(self.timerevent, self.drop_speed/self.level)
    #Reset Score
    self.score = 0
    self.lines_cleared = 0
    
    self.sounds["bgm-a"].stop()
    self.sounds["bgm-a"].play(-1)
    self.get_newpiece()
    
  def move_left(self):
    self.pos_target[0] = self.pos_current[0] - 1
    self.pos_target[1] = self.pos_current[1]
    if self.check_collision() is False:
      self.sounds["move"].play()
      self.move_piece()
      
  def move_right(self):
    self.pos_target[0] = self.pos_current[0] + 1
    self.pos_target[1] = self.pos_current[1]
    if self.check_collision() is False:
      self.sounds["move"].play()
      self.move_piece()
      
  def move_down(self):
    if self.level > 0:
      self.rot_target = self.rot_current
      self.pos_target[0] = self.pos_current[0]
      self.pos_target[1] = self.pos_current[1] + 1
      if self.check_collision() is False:
        #self.sounds["move"].play()
        self.move_piece()
      else:
        self.sounds["lock"].play()
        self.lock_piece()
        self.get_newpiece()

  def rotate_right(self):
    self.rot_target = (self.rot_current + 1) % 4
    if self.check_collision() is False:
      self.sounds["rotate"].play()
      self.move_piece()
      
  def rotate_left(self):    
    self.rot_target = (self.rot_current - 1) % 4
    if self.check_collision() is False:
      self.sounds["rotate"].play()
      self.move_piece()
      
  def get_newpiece(self):
    self.piece = random.randint(1,7)
    self.pos_target[0] = 4
    self.pos_target[1] = 0
    self.rot_target  = 0
    if self.check_collision() is False:
      self.move_piece()
    else:
      self.game_over()
  
  def move_piece(self):
    self.rot_current = self.rot_target
    self.pos_current[0] = self.pos_target[0]
    self.pos_current[1] = self.pos_target[1]

  def lock_piece(self):
    for i in xrange(4):
      x=self.pos_current[0] + self.tetrominoes[self.piece][self.rot_current][0][i] #x
      y=self.pos_current[1] + self.tetrominoes[self.piece][self.rot_current][1][i] #y
      self.play_grid[y][x] = self.piece
    self.check_lineclear()
    #print "Lock piece"
    
  def check_collision(self):
    #Checks if the target location/rotation is valid
    y = self.tetrominoes[self.piece][self.rot_target][1]
    x = self.tetrominoes[self.piece][self.rot_target][0]
    
    #Check left border
    if(self.pos_target[0] + min(x) < 0):
      #print "Left Border Hit"
      return True
    #Check right border
    if(self.pos_target[0] + max(x) >= self.width):
      #print "Right Border Hit"
      return True
    #Check bottom border
    if(self.pos_target[1] + max(y) >= self.height):
      #print "Bottom Border Hit"
      return True
    #Check individual blocks
    for i in xrange(4):
      x=self.pos_target[0] + self.tetrominoes[self.piece][self.rot_target][0][i] #x
      y=self.pos_target[1] + self.tetrominoes[self.piece][self.rot_target][1][i] #y
      if self.play_grid[y][x] != 0:      
        return True
    #If all OK
    return False
  def debug_print(self):
    pass
    #print "Current", self.pos_current, self.rot_current  
    #print "Target", self.pos_target, self.rot_target 
    
  def check_lineclear(self):
    y_set = set(self.tetrominoes[self.piece][self.rot_current][1])
    num_cleared = 0
    for y in y_set:
      row = y + self.pos_current[1]
      row_cleared = True
      for block in self.play_grid[row]:
        if block is 0:
          row_cleared = False
      if row_cleared:
        num_cleared = num_cleared + 1
        self.delete_row(row)
    if num_cleared == 4:
      #Tetris!
      self.sounds["4line"].play()
      if self.tetris_last == True:
        self.score = self.score + 1200
      else:
        self.score = self.score + 800
      self.tetris_last = True
    elif num_cleared > 0:
      self.sounds["lineclear"].play() #change
      self.score = self.score + num_cleared * 100
    if num_cleared > 0:
      self.lines_cleared = self.lines_cleared + num_cleared
      self.level = (self.lines_cleared / 10) + 1
      pygame.time.set_timer(self.timerevent, self.drop_speed/self.level)
      print "Lines", self.lines_cleared, "Level", self.level
      print "Score", self.score

  def delete_row(self, row):
    self.play_grid.pop(row)
    self.play_grid.insert(0, list(self.empty_row))
  
  def get_surface(self):
    surface = pygame.Surface( (self.width, self.height) )
    for i in xrange(4):
      x=self.pos_current[0] + self.tetrominoes[self.piece][self.rot_current][0][i] #x
      y=self.pos_current[1] + self.tetrominoes[self.piece][self.rot_current][1][i] #y
      surface.set_at( (x, y), self.colours[self.piece] )
      
    for x in range(self.width):
      for y in range(self.height):
        if self.play_grid[y][x] != 0:
          surface.set_at( (x, y), self.colours[self.play_grid[y][x]] )
    return surface

  def get_score(self):
    return self.score

  def do_nothing(self):
    pass
    
  def run(self):
    while True:
      #Try read a input from the queue
      input = self.input_queue.get( block=True )
      {"left"  : self.move_left,
       "right" : self.move_right,
       "down"  : self.move_down,
       "rot_r" : self.rotate_right,
       "rot_l" : self.rotate_left,
       "new_g" : self.new_game
       }.get(input, self.do_nothing)()
      self.input_queue.task_done()
      #self.signal_queue.put("done")
      #self.signal_queue.join()
