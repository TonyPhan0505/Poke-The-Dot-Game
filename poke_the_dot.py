import pygame
import random
import math

# Create the window and its size and title

def main():

	pygame.init() # Required to render fonts
	screen = pygame.display.set_mode((500,400))
	pygame.display.set_caption("Poke The Dots")

	game = Game(screen)
	game.play()
	pygame.quit()


class Game:

	def __init__(self, screen):

		self.screen = screen
		self.bg_color = pygame.Color('black')
		self.game_clock = pygame.time.Clock()
		self.FPS = 30
		self.close_clicked = False
		self.mouse_clicked = False
		self.width = 500
		self.height = 400
		self.big_radius = 40
		self.small_radius = 30
		self.score = 0
		self.big_dot_pos = [random.randint(self.big_radius, self.width-self.big_radius), random.randint(self.big_radius, self.height-self.big_radius)]
		self.small_dot_pos = [random.randint(self.small_radius, self.width-self.small_radius), random.randint(self.small_radius, self.height - self.small_radius)]

		big_dot_color = pygame.Color('blue')
		big_dot_velocity = [8,4]
		self.big_dot = Dot(big_dot_color, self.big_radius, self.big_dot_pos, big_dot_velocity, self.screen)

		small_dot_color = pygame.Color('red')
		small_dot_velocity = [4,8]
		self.small_dot = Dot(small_dot_color, self.small_radius, self.small_dot_pos, small_dot_velocity, self.screen)
	
	def dots_collide(self):

		if math.sqrt((self.small_dot_pos[0]-self.big_dot_pos[0])**2 + (self.small_dot_pos[1]-self.big_dot_pos[1])**2) <= (self.small_radius + self.big_radius):
			return True
		return False


	def play(self):

		while not self.close_clicked:

			self.handle_events()
			self.draw()
			self.update()
			self.game_clock.tick(self.FPS)

	def handle_events(self):

		for event in pygame.event.get(): # all the mouse and keyboard input events of the users	
			if event.type == pygame.QUIT:	
				self.close_clicked = True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse_clicked = True

	def draw(self):

		self.screen.fill(self.bg_color)
		self.big_dot.draw()
		self.small_dot.draw()
		self.show_score()
		self.show_game_over_message()
		pygame.display.flip()

	def update(self):

		if not self.dots_collide():
			self.small_dot.move()
			self.big_dot.move()

		if self.mouse_clicked:
			if self.dots_collide():
				self.score = 0
			self.small_dot_pos[0] = random.randint(self.small_radius, self.width-self.small_radius)
			self.small_dot_pos[1] = random.randint(self.small_radius, self.height - self.small_radius)
			self.big_dot_pos[0] = random.randint(self.big_radius, self.width-self.big_radius)
			self.big_dot_pos[1] = random.randint(self.big_radius, self.height-self.big_radius)
			self.mouse_clicked = False

	def show_game_over_message(self):
		text_string = "GAME OVER"
		text_color = pygame.Color("PURPLE")
		text_font = pygame.font.SysFont("Times New Roman", 24, bold = True, italic = False)
		text_image = text_font.render(text_string, True, text_color)
		text_pos = (10, self.height - 30)
		if self.dots_collide():
			self.screen.blit(text_image, text_pos)
	
	def show_score(self):

		if self.big_dot.collide_with_edges() or self.small_dot.collide_with_edges() and not self.dots_collide():
			self.score += 1
		
		score_string = f"Score: {self.score}"
		text_color = pygame.Color("GREEN")
		text_font = pygame.font.SysFont("Times New Roman", 24, bold = False, italic = False)
		text_image = text_font.render(score_string, True, text_color)
		text_pos = (10, 10)
		self.screen.blit(text_image, text_pos)
class Dot:

	def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, screen):

		self.color = dot_color
		self.radius = dot_radius
		self.center = dot_center
		self.velocity = dot_velocity
		self.screen = screen
		self.width = 500
		self.height = 400

	def collide_with_edges(self):

		if self.collide_with_bottom_edge() or self.collide_with_left_edge() or self.collide_with_right_edge() or self.collide_with_top_edge():
			return True

	def collide_with_left_edge(self):

		if self.center[0] < self.radius:
			return True
		return False
	
	def collide_with_right_edge(self):

		if self.center[0] + self.radius > self.width:
			return True
		return False

	def collide_with_top_edge(self):

		if self.center[1] < self.radius:
			return True
		return False

	def collide_with_bottom_edge(self):

		if self.center[1] + self.radius > self.height:
			return True
		return False

	def move(self):

		if self.collide_with_left_edge():
			self.velocity[0] = -self.velocity[0]

		if self.collide_with_top_edge():
			self.velocity[1] = -self.velocity[1]

		if self.collide_with_right_edge():
			self.velocity[0] = - self.velocity[0]

		if self.collide_with_bottom_edge():

			self.velocity[1] = -self.velocity[1]

		for index in range(0,2):
			self.center[index] += self.velocity[index]

	def draw(self):

		pygame.draw.circle(self.screen, self.color, self.center, self.radius)

main()