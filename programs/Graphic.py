import psutil, pygame

def Graphs(screen, cpu_percent):
    l_cpu_percent = cpu_percent  
    num_cpu = len(l_cpu_percent)
    alt = 220
    larg = (360 - (num_cpu+1)*10)/num_cpu
    d = 120
    for i in l_cpu_percent:
          pygame.draw.rect(screen, pygame.Color('black'), (d, 200, larg, alt))
          pygame.draw.rect(screen, pygame.Color('white'), 	(d, 200, larg, (1-i/100)*alt))
          d = d + larg + 10
    cont += 1