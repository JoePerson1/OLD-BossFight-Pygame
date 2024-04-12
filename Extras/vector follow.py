import pygame

velocity         = 1

def FollowMe(pops, fpos):
    target_vector       = pygame.math.Vector2(*pops)
    follower_vector     = pygame.math.Vector2(*fpos)
    
    print('CharacterVector, FollowerVector')
    print(target_vector, follower_vector)

    distance = follower_vector.distance_to(target_vector)
    direction_vector    = (target_vector - follower_vector) / distance
    print('Direction Vector:')
    print(direction_vector)
    new_follower_vector = follower_vector + direction_vector * velocity
    
    print('FollowerVector2(x), FollowerVector2(y)')
    print(new_follower_vector.x, new_follower_vector.y)
    
    print('------------------------')
    
    return (new_follower_vector.x, new_follower_vector.y)

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

follower = (100, 100)
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player   = pygame.mouse.get_pos()
    follower = FollowMe(player, follower)

    window.fill(0)
    pygame.draw.circle(window, (0, 0, 255), player, 10)
    pygame.draw.circle(window, (255, 0, 0), (round(follower[0]), round(follower[1])), 30)
    pygame.display.flip()

pygame.quit()
exit()