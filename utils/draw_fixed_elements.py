import pygame

from .constants import track_color, background_color, center_color

def draw_fixed_elements(screen, track ,iteration, episode_number):

    screen.fill(background_color)

    font = pygame.font.SysFont('Garamond', 30)
    text = 'Episode {} Iteration {}'.format(episode_number,iteration)
    screen.blit(font.render(text,False, (255,255,255)),(20,20))

    pygame.draw.polygon(screen, color = track_color, points = track.exterior_list)

    pygame.draw.lines(screen, color = center_color, closed = False,points = track.center_list)