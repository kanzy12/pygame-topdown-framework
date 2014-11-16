import ConfigParser
import pygame
import pygame.locals
import json

from objects import *

#code inspired from tutorial at http://qq.readthedocs.org/en/latest/tiles.html

class Level(object):
    def load_file(self, filename):
        self.map = []
        self.players = []
        self.key = {}
        parser = ConfigParser.ConfigParser()
        parser.read(filename + ".map")
        self.tileset = parser.get("level", "tileset")
        self.map = parser.get("level", "map").split("\n")
        
        json_data=open(filename + ".json")

        data = json.load(json_data)
        json_data.close()

        switches = []
        for switch in data["switches"]:
            new_switch = Switch(switch["position"][0], switch["position"][1], switch["targets"])
            switches.append(new_switch)

        self.width = len(self.map[0])
        self.height = len(self.map)

        for i in xrange(self.width):
            for j in xrange(self.height):
                if (self.map[j][i] == "P"):
                    self.players.append([i,j])
                    
                if (self.map[j][i] == "G"):
                    self.goal = i, j
       
        for section in parser.sections():
            if len(section) == 1:
                desc = dict(parser.items(section))
                self.key[section] = desc
                        
        self.tile_height = 50;
        self.tile_width = 50;
        
        image = pygame.image.load(self.tileset).convert()
        image_width, image_height = image.get_size()
        self.tile_table = []
        for tile_y in range(0, image_height/self.tile_height):
            line = []
            self.tile_table.append(line)
            for tile_x in range(0, image_width/self.tile_width):
                rect = (tile_x * self.tile_width, tile_y * self.tile_height, self.tile_width, self.tile_height)
                line.append(image.subsurface(rect))
        
        return self.players, int(self.key["t"]["time"]), switches
        
    def get_tile(self, x, y):
        char = self.map[y][x]
        return self.key[char]
        
    def get_bool(self, x, y, tile_type):
        value = self.get_tile(x, y).get(tile_type)
        return value
        
    def is_wall(self, x, y):
        return self.get_bool(x, y, "wall")
        
    def is_blocking(self, x, y):
        if x < 0 or x > self.width or y < 0 or y > self.height:
            #out of bounds
            return True
        
        return self.get_bool(x, y, "block")
        
    def render(self):
        image = pygame.Surface((self.width * self.tile_width, self.height * self.tile_height))
        
        for map_y, line in enumerate(self.map):
            for map_x, c in enumerate(line):
                if self.is_wall(map_x, map_y):
                    tile = 0, 1
                elif self.get_bool(map_x, map_y, "goal"):
                    tile = 0, 2
                elif self.get_bool(map_x, map_y, "switch"):
                    tile = 0, 3
                else:
                    #it's ground
                    tile = 0, 0
                
                tile_image = self.tile_table[tile[0]] [tile[1]]
                image.blit(tile_image, (map_x * self.tile_width, map_y * self.tile_height))
        return image
        
if __name__ == "__main__":
    screen = pygame.display.set_mode((200, 200))
    level = Level()
    level.load_file("level.map")
    
    background = level.render()
    screen.blit(background,(0,0))
    pygame.display.flip()
    
    while True:   
        pygame.display.flip()
        
    
