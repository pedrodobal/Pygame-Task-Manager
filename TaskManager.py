import pygame, psutil, platform, datetime, socket, os, time, threading
from programs import SystemInfo, CpuInfo

# Colours
DARKWHITE = (227, 227, 227)
LIGHTGREY = (200, 200, 200)
MEDIUMGREY = (170, 170, 170)
DARKGREY = (56, 56, 56)
# End_Colours

# CONSTANTES
(width, height) = (500, 450)
SCREEN = pygame.display.set_mode((width, height))
TIME = pygame.time.Clock()
ICON = pygame.image.load("images/icon.png")
pygame.display.set_caption("Task Manager")
pygame.display.set_icon(ICON)
pygame.init()
FONT_CALIBRI = pygame.font.SysFont('Calibri', 15, True, False)
FONT_CALIBRI_Small = pygame.font.SysFont('Calibri', 9, True, False)
FONT_CALIBRI_Medium = pygame.font.SysFont('Calibri', 12, True, False)
af_map = {socket.AF_INET: 'IPv4', socket.AF_INET6: 'IPv6', psutil.AF_LINK: 'MAC'}
duplex_map = {psutil.NIC_DUPLEX_FULL: "full", psutil.NIC_DUPLEX_HALF: "half", psutil.NIC_DUPLEX_UNKNOWN: "?"}
EndProgram = False
TabProcessos = True
TabFiles = False
extend = False
Page = 0
cont = 30
ScrBt = 0
ScrBtExt = 0
pinfo = {}
PIDInfo = []
path = ["C:\\"]
listdir = os.listdir(path[0])
path_cont = 0


# FIM_CONSTANTES

def Extend(ScrBtExt):
    global TabExtendLoc, TabExtendRect, ScrlSizeExt
    ScrlSizeExt = 0
    TabExtendRect = pygame.Surface.get_rect(TabExtend[0])
    TabExtendLoc = (width - TabExtendRect[2] - 2, (height - TabExtendRect[3]) / 2)
    if extend:
        bg_size = (430, 348)
        pygame.draw.rect(SCREEN, MEDIUMGREY, (488, 12, 450, 426))
        pygame.draw.rect(SCREEN, pygame.Color("black"), (490, 24, 1, 402))
        pygame.draw.rect(SCREEN, pygame.Color("white"), (width / 2 + 25, 75, bg_size[0], bg_size[1]))
        pygame.draw.rect(SCREEN, DARKWHITE, (width / 2 + 26, 76, bg_size[0] - 3, bg_size[1] - 3), 2)
        if TabProcessos and width == 950:
            draw(TabFilesImg, width - 119, 46, MousePos)
            pygame.draw.rect(SCREEN, (189, 189, 189), (width / 2 + 25, 75, bg_size[0], bg_size[1]), 1)
            draw(TabProcessosImg, width / 2 + 25, 46, MousePos)

            Dist = 0
            if width == 950:
                templ = "%-9s  %-23s  %25s  %24s"
                SCREEN.blit(FONT_CALIBRI_Medium.render(templ % ('PID', 'Nome', 'Memoria', 'Usuário'), True, DARKGREY),
                            [width / 2 + 50, 80])
                for row in PIDInfo:
                    if 100 <= ((100 + ScrBtExt) + Dist) <= 400:
                        name = str(row['name'][0:21])
                        if row['username'] == 'None':
                            username = str("SYSTEM")
                        else:
                            username = str(row['username'][0:15])

                        SCREEN.blit(FONT_CALIBRI_Medium.render(str(row['pid']), True, DARKGREY),
                                    [width / 2 + 50, (100 + ScrBtExt) + Dist])
                        SCREEN.blit(FONT_CALIBRI_Medium.render(name, True, DARKGREY),
                                    [width / 2 + 95, (100 + ScrBtExt) + Dist])
                        try:
                            SCREEN.blit(FONT_CALIBRI_Medium.render(
                                str(BytesConversion(psutil.Process(row['pid']).memory_info().rss)), True, DARKGREY),
                                [width / 2 + 250, (100 + ScrBtExt) + Dist])
                        except psutil.NoSuchProcess:
                            pass
                        SCREEN.blit(FONT_CALIBRI_Medium.render(username, True, DARKGREY),
                                    [width / 2 + 350, (100 + ScrBtExt) + Dist])
                    ScrlSizeExt += 15
                    Dist += 15

        if TabFiles and width == 950:
            draw(TabProcessosImg, width / 2 + 25, 46, MousePos)
            pygame.draw.rect(SCREEN, (189, 189, 189), (width / 2 + 25, 75, bg_size[0], bg_size[1]), 1)
            draw(TabFilesImg, width - 119, 46, MousePos)
            icons_draw()

def icons_draw():
    
    global file_loc, folder_loc, ScrlSizeExt
    
    icon_desloc_x = width / 2 + 46
    icon_desloc_y = 91
    ScrlSizeExt = 0
    file_loc = []
    folder_loc = []
    ScrlSizeExt = 0
    for name in listdir:
        if os.path.isfile(path[path_cont]+name):
            if 91 <= (ScrBtExt + icon_desloc_y) <= 380:
                SCREEN.blit(file_icon, [icon_desloc_x, icon_desloc_y + ScrBtExt])
            file_loc.append((name,icon_desloc_x, icon_desloc_y + ScrBtExt))
            name_split = os.path.splitext(path[path_cont]+name)
            if len(name) > 15:
                if 91 <= (ScrBtExt + icon_desloc_y+45) <= 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name[:12], True, pygame.Color('black')), [icon_desloc_x, icon_desloc_y+45 + ScrBtExt])
                if 91 <= (ScrBtExt + icon_desloc_y+55) <= 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name[12:24], True, pygame.Color('black')), [icon_desloc_x, icon_desloc_y+55 + ScrBtExt])
            else:
                if 91 <= (ScrBtExt + icon_desloc_y+45) <= 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name, True, pygame.Color('black')), [icon_desloc_x, icon_desloc_y+45 + ScrBtExt])

                if 91 <= (ScrBtExt + icon_desloc_y+20) <= 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name_split[1][:5], True, pygame.Color('black')), [icon_desloc_x+7, icon_desloc_y+20 + ScrBtExt])
            icon_desloc_x += 65

        elif os.path.isdir(path[path_cont]+name):
            if 91 <= (ScrBtExt + icon_desloc_y) <= 380:
                SCREEN.blit(folder_icon, [icon_desloc_x, icon_desloc_y + ScrBtExt])
            folder_loc.append((name,icon_desloc_x, icon_desloc_y + ScrBtExt))
            if len(name) > 15:
                if 91 <= (ScrBtExt + icon_desloc_y + 20) < 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name[:12], True, pygame.Color('black')),
                                            [icon_desloc_x, icon_desloc_y+45 + ScrBtExt])
                if 91 <= (ScrBtExt + icon_desloc_y + 20) < 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name[12:24], True, pygame.Color('black')),
                                            [icon_desloc_x, icon_desloc_y+55 + ScrBtExt])
            else:
                if 91 <= (ScrBtExt + icon_desloc_y + 20) < 380:
                    SCREEN.blit(FONT_CALIBRI_Small.render(name, True, pygame.Color('black')),
                                        [icon_desloc_x, icon_desloc_y+45 + ScrBtExt])
            icon_desloc_x += 65
        if icon_desloc_x == width / 2 + 436:
            icon_desloc_x = width / 2 + 46
            icon_desloc_y += 75
            ScrlSizeExt += 15

def PcInfo(ScrBt):
    global ScrlSize
    ScrlSize = 0
    Alin = 0
    Dist = 0
    Dist1 = 0
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)

    for nic, addrs in psutil.net_if_addrs().items():
        NIC = str(nic)
        if nic in stats:
            st = stats[nic]
            if ((225 + ScrBt) + Dist) >= 210 and ((235 + ScrBt) + Dist) <= 410:
                SCREEN.blit((FONT_CALIBRI.render(
                    "Speed= {}Mb, Duplex= {}, Mtu= {}, Up= {}".format(st.speed, duplex_map[st.duplex], st.mtu,
                                                                      "yes" if st.isup else "no"), True, DARKGREY)),
                    [120, (225 + ScrBt) + Dist])
                ScrlSize += 15
        if nic in io_counters:
            io = io_counters[nic]
            # Incoming
            NetOutBytes = BytesConversion(io.bytes_sent)
            NetOutPackets = str(io.packets_sent)
            NetOutErrs = BytesConversion(io.errout)
            # Outgoing
            NetIncBytes = BytesConversion(io.bytes_recv)
            NetIncPackets = str(io.packets_recv)
            NetIncErrs = BytesConversion(io.errin)
            #
            if ((210 + ScrBt) + Dist) >= 200 and ((235 + ScrBt) + Dist) <= 410:
                SCREEN.blit((FONT_CALIBRI.render("{}:".format(NIC), True, DARKGREY)), [120, (210 + ScrBt) + Dist])
                ScrlSize += 15
            if ((240 + ScrBt) + Dist) >= 210 and ((250 + ScrBt) + Dist) <= 410:
                SCREEN.blit((FONT_CALIBRI.render(
                    "Incoming - Bytes: {}  Packets: {}  Erros: {}".format(NetIncBytes, NetIncPackets, NetIncErrs), True,
                    DARKGREY)), [120, (240 + ScrBt) + Dist])
                ScrlSize += 15
            if ((255 + ScrBt) + Dist) >= 210 and ((265 + ScrBt) + Dist) <= 410:
                SCREEN.blit((FONT_CALIBRI.render(
                    "Outgoing - Bytes: {}  Packets: {}  Erros: {}".format(NetOutBytes, NetOutPackets, NetOutErrs), True,
                    DARKGREY)), [120, (255 + ScrBt) + Dist])
                ScrlSize += 15
        Alin = ((255 + ScrBt) + Dist) + 15
        for addr in addrs:
            if 210 <= ((270 + ScrBt) + Dist + Dist1) <= 410:
                SCREEN.blit((FONT_CALIBRI.render("{}: {}".format(af_map.get(addr.family, addr.family), addr.address),
                                                 True, DARKGREY)), [120, Alin + Dist1])
                ScrlSize += 15
            if addr.broadcast:
                if 210 <= ((285 + ScrBt) + Dist1 + Dist) <= 410:
                    SCREEN.blit((FONT_CALIBRI.render("Broadcast {}:".format(addr.broadcast), True, DARKGREY)),
                                [120, (285 + ScrBt) + Dist + Dist1])
                    ScrlSize += 15
                    Dist1 += 15
            if addr.netmask:
                if 210 <= ((285 + ScrBt) + Dist1 + Dist) <= 410:
                    SCREEN.blit((FONT_CALIBRI.render("Netmask {}:".format(addr.netmask), True, DARKGREY)),
                                [120, (285 + ScrBt) + Dist + Dist1])
                    ScrlSize += 15
                    Dist1 += 15
            if addr.ptp:
                if 210 <= ((285 + ScrBt) + Dist1 + Dist) <= 410:
                    SCREEN.blit((FONT_CALIBRI.render("Broadcast {}:".format(addr.ptp), True, DARKGREY)),
                                [120, (285 + ScrBt) + Dist + Dist1])
                    ScrlSize += 15
                    Dist1 += 15

            Dist1 += 15
        Dist1 = 0
        Dist += 170
        ScrlSize += 170
    ScrlSize = ScrlSize - 285
    SCREEN.blit((FONT_CALIBRI.render("Informações do Sistema", True, DARKGREY)), [120, 30])
    SCREEN.blit((FONT_CALIBRI.render("______________________________________________", True, DARKGREY)), [120, 32])
    SCREEN.blit((FONT_CALIBRI.render("Sistema Operacional: ", True, DARKGREY)), [120, 60])
    SCREEN.blit(OS, [260, 60])
    SCREEN.blit((FONT_CALIBRI.render("Versão do OS: ", True, DARKGREY)), [120, 80])
    SCREEN.blit((FONT_CALIBRI.render(
        datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("Boot Time: %d-%m-%Y  %H:%M:%S"), True, DARKGREY)),
        [120, 140])
    SCREEN.blit(VERSION, [215, 80])
    SCREEN.blit((FONT_CALIBRI.render("Nome do Computador: {}".format(SystemInfo.name()), True, DARKGREY)), [120, 100])
    SCREEN.blit((FONT_CALIBRI.render("Arquitetura: {}".format(SystemInfo.arc()), True, DARKGREY)), [120, 120])
    SCREEN.blit((FONT_CALIBRI.render("Informações da Rede ", True, DARKGREY)), [120, 180])
    SCREEN.blit((FONT_CALIBRI.render("______________________________________________", True, DARKGREY)), [120, 182])


def ProcessorInfo(SCREEN, Cpu_Percent_Cores, Cpu_Percent):
    SCREEN.blit((FONT_CALIBRI.render("Informações do Processador ", True, DARKGREY)), [120, 30])
    SCREEN.blit((FONT_CALIBRI.render("______________________________________________", True, DARKGREY)), [120, 32])
    SCREEN.blit((FONT_CALIBRI.render("Processador: ", True, DARKGREY)), [120, 60])
    SCREEN.blit(BRAND, [213, 60])
    SCREEN.blit((FONT_CALIBRI.render("Arquitetura: ", True, DARKGREY)), [120, 80])
    SCREEN.blit(ARCH, [213, 80])
    SCREEN.blit((FONT_CALIBRI.render("Sistema: ", True, DARKGREY)), [120, 100])
    SCREEN.blit(BITS, [213, 100])
    SCREEN.blit((FONT_CALIBRI.render("Frequência: ", True, DARKGREY)), [120, 120])
    SCREEN.blit(FREQ_CURRENT, [213, 120])
    SCREEN.blit(FREQ_MAX, [300, 120])
    SCREEN.blit((FONT_CALIBRI.render("Logic (Cores): ", True, DARKGREY)), [120, 140])
    SCREEN.blit(CORES, [213, 140])
    SCREEN.blit((FONT_CALIBRI.render("Uso CPU:            {}%".format(str(Cpu_Percent)), True, DARKGREY)), [120, 160])
    GraphsCpu(SCREEN, Cpu_Percent_Cores)


def MemoryInfo():
    MEM = psutil.virtual_memory()
    SCREEN.blit((FONT_CALIBRI.render("Informações da Memória ", True, DARKGREY)), [120, 30])
    SCREEN.blit((FONT_CALIBRI.render("______________________________________________", True, DARKGREY)), [120, 32])
    SCREEN.blit((FONT_CALIBRI.render("Virtual Memory:", True, DARKGREY)), [120, 80])
    MemDetails(psutil.virtual_memory(), 120, 100)
    SCREEN.blit((FONT_CALIBRI.render("Swap Memory: ", True, DARKGREY)), [300, 80])
    MemDetails(psutil.swap_memory(), 300, 100)


def HdInfo(ScrBt):
    global ScrlSize
    ScrlSize = 0
    Alin = 0
    Dist = 0
    Dist1 = 0
    io_counters = psutil.disk_io_counters(perdisk=True)
    for disk in psutil.disk_io_counters(perdisk=True):
        if disk in io_counters:
            io = io_counters[disk]
            if ((60 + ScrBt) + Dist) >= 60 and ((60 + ScrBt) + Dist) <= 410:
                ScrlSize += 15
                SCREEN.blit((FONT_CALIBRI.render("{}:".format(disk), True, DARKGREY)), [120, (60 + ScrBt) + Dist])
            if (75 + Dist + ScrBt) >= 60 and (75 + Dist + ScrBt) <= 410:
                ScrlSize += 15
                SCREEN.blit((FONT_CALIBRI.render(
                    "Number of reads - Reads = {}   Writes = {}".format(io.read_count, io.write_count), True,
                    DARKGREY)), [120, 75 + Dist + ScrBt])
            if (90 + Dist + ScrBt) >= 60 and (90 + Dist + ScrBt) <= 410:
                ScrlSize += 15
                SCREEN.blit((FONT_CALIBRI.render(
                    "Number of bytes - Reads = {}   Writes = {}".format(BytesConversion(io.read_bytes),
                                                                        BytesConversion(io.write_bytes)), True,
                    DARKGREY)), [120, 90 + Dist + ScrBt])
            if (105 + Dist + ScrBt) >= 60 and (105 + Dist + ScrBt) <= 410:
                ScrlSize += 15
                SCREEN.blit((FONT_CALIBRI.render(
                    "Amount of time   - Reads = {}   Writes = {}".format(datetime.timedelta(seconds=io.read_time),
                                                                         datetime.timedelta(seconds=io.write_time)),
                    True, DARKGREY)), [120, 105 + Dist + ScrBt])
        Dist += 75
        ScrlSize += 75
    Alin = (105 + Dist + 15)
    templ = "%-8s  %8s  %8s  %8s  %5s%%  %9s   %s"
    if (Alin - 45 + ScrBt) >= 60 and (Alin - 45 + ScrBt) <= 410: SCREEN.blit(
        (FONT_CALIBRI.render(templ % ("Device", "Total", "Used", "Free", "Use ", "Type", "Mount"), True, DARKGREY)),
        [120, Alin - 45 + ScrBt])
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        if (Alin + 15 + Dist1 - 45 + ScrBt) >= 60 and (Alin + 15 + Dist1 - 45 + ScrBt) <= 410:
            ScrlSize += 15
            Graphs(SCREEN, 120, Alin + 15 + Dist1 - 45 + ScrBt, 15,
                   RED if usage.percent >= 75 else pygame.Color('green'),
                   int(usage.percent))
        if (Alin + 15 + Dist1 - 45 + ScrBt) >= 60 and (Alin + 15 + Dist1 - 45 + ScrBt) <= 410:
            ScrlSize += 15
            SCREEN.blit((FONT_CALIBRI.render(templ % (
                part.device, BytesConversion(usage.total), BytesConversion(usage.used), BytesConversion(usage.free),
                int(usage.percent), part.fstype, part.mountpoint), True, DARKGREY)),
                        [120, Alin + 15 + Dist1 - 45 + ScrBt])
        Dist1 += 30
        ScrlSize += 30
        ScrlSize = ScrlSize - 400
    SCREEN.blit((FONT_CALIBRI.render("Informações do Disco Rígido", True, DARKGREY)), [120, 30])
    SCREEN.blit((FONT_CALIBRI.render("______________________________________________", True, DARKGREY)), [120, 32])


def Overview():
    SCREEN.blit((FONT_CALIBRI.render("Overview", True, DARKGREY)), [120, 30])
    SCREEN.blit((FONT_CALIBRI.render("______________________________________________", True, DARKGREY)), [120, 32])


def BytesConversion(n):
    symbols = ('Kb', 'Mb', 'Gb', 'Tb', 'Pb', 'Eb', 'Zb', 'Yb')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f%s' % (value, s)
    return '%.2fB' % (n)


def MemDetails(mem, x, y):
    Dist = 0
    for name in mem._fields:
        value = getattr(mem, name)
        if name != 'percent':
            value = BytesConversion(value)
        else:
            pygame.draw.rect(SCREEN, pygame.Color('white'), (x + 40, y * 4, 40, -150))
            pygame.draw.rect(SCREEN, pygame.Color('red') if value >= 75 else pygame.Color('green'),
                             (x + 40, y * 4, 40, -150 * value / 100))
            value = str(value) + "%"
            SCREEN.blit((FONT_CALIBRI.render(value, True, DARKGREY)), [x + 43, y * 3.15])
        SCREEN.blit((FONT_CALIBRI.render('%-15s : %7s' % (name.capitalize(), value), True, DARKGREY)), [x, y + Dist])
        Dist += 15


def Graphs(screen, x, y, ysize, color, percent):
    pygame.draw.rect(screen, pygame.Color('white'), (x, y, 346, ysize))
    pygame.draw.rect(screen, color, (x, y, 346 * percent / 100, ysize))


def GraphsCpu(screen, Cpu_Percent):
    l_cpu_percent = Cpu_Percent
    num_cpu = len(l_cpu_percent)
    alt = 220
    larg = (366 - (num_cpu + 1) * 10) / num_cpu
    d = 120
    for i in l_cpu_percent:
        pygame.draw.rect(screen, pygame.Color('red') if i >= 75 else pygame.Color('green'), (d, 200, larg, alt))
        pygame.draw.rect(screen, pygame.Color('white'), (d, 200, larg, (1 - i / 100) * alt))
        SCREEN.blit((FONT_CALIBRI.render("{}%".format(str(round(i))), True, DARKGREY)), [d + larg / 5, 185])
        d = d + larg + 10


def ImageUpload():
    global TabFilesImg, TabProcessosImg, hdIcon, memIcon, pcIcon, processorIcon, overIcon, backIcon, FundoBranco, exitIcon, FundoCinza, TabExtend, file_icon, folder_icon, hd_icon

    exitIcon = [pygame.image.load("images/exit_icon.png"), pygame.image.load("images/exit_icon_1.png")]
    hdIcon = [pygame.image.load("images/HD_icon.png"), pygame.image.load("images/HD_icon_1.png")]
    memIcon = [pygame.image.load("images/mem_icon.png"), pygame.image.load("images/mem_icon_1.png")]
    pcIcon = [pygame.image.load("images/pc_icon.png"), pygame.image.load("images/pc_icon_1.png")]
    processorIcon = [pygame.image.load("images/cpu_icon.png"), pygame.image.load("images/cpu_icon_1.png")]
    overIcon = [pygame.image.load("images/overview_icon.png"), pygame.image.load("images/overview_icon_1.png")]
    FundoBranco = pygame.image.load("images/FundoBranco.png")
    FundoCinza = pygame.image.load("extend_bg.png")
    TabExtend = [pygame.image.load("images/Tab.png"), pygame.image.load("images/Tab_1.png")]
    TabFilesImg = [pygame.image.load("images/Tab_Files.png"), pygame.image.load("images/Tab_Files_1.png")]
    TabProcessosImg = [pygame.image.load("images/Tab_Processos.png"), pygame.image.load("images/Tab_Processos_1.png")]
    file_icon=pygame.image.load("images/files icons/file_icon.png")
    folder_icon=pygame.image.load("images/files icons/folder_icon.png")
    hd_icon=pygame.image.load("images/files icons/hd_icon.png")


def InfoUp():
    global OS, VERSION, PC_NAME, ARQ, CPU, BRAND, ARCH, BITS, FREQ_CURRENT, FREQ_MAX, CORES

    OS = FONT_CALIBRI.render(SystemInfo.os(), True, DARKGREY)
    VERSION = FONT_CALIBRI.render(SystemInfo.osVersion(), True, DARKGREY)
    CPU = FONT_CALIBRI.render(SystemInfo.cpu(), True, DARKGREY)
    BRAND = FONT_CALIBRI.render(CpuInfo.brand(), True, DARKGREY)
    ARCH = FONT_CALIBRI.render(CpuInfo.arch(), True, DARKGREY)
    BITS = FONT_CALIBRI.render("{}-bit".format(CpuInfo.bits()), True, DARKGREY)
    FREQ_CURRENT = FONT_CALIBRI.render("Atual: {}Ghz".format(str(round(CpuInfo.freq().current / 1000, 1))), True,
                                       DARKGREY)
    FREQ_MAX = FONT_CALIBRI.render("Max: {}Ghz".format(str(round(CpuInfo.freq().max / 1000, 1))), True, DARKGREY)
    CORES = FONT_CALIBRI.render(CpuInfo.cores(), True, DARKGREY)


def draw(img, x, y, MousePos, msg=None):
    imgSize = (pygame.Surface.get_rect(img[0]))
    PosX = (imgSize[2] + x)
    PosY = (imgSize[3] + y)
    if MousePos[0] < PosX and MousePos[0] > x:
        if MousePos[1] < PosY and MousePos[1] > y:
            SCREEN.blit(img[1], (x, y))
            if msg != None:
                ToolTip(msg, MousePos[0], MousePos[1])
        else:
            SCREEN.blit(img[0], (x, y))
    else:
        SCREEN.blit(img[0], (x, y))


def ToolTip(msg, tx, ty):
    text = FONT_CALIBRI.render(msg, True, DARKGREY)
    TextSize = len(msg)
    pygame.draw.rect(SCREEN, pygame.Color('white'), (tx + 10, ty + 10, (TextSize * 7), 20))
    pygame.draw.rect(SCREEN, pygame.Color('black'), (tx + 10, ty + 10, (TextSize * 7), 20), 1)
    SCREEN.blit(text, [15 + tx, 12 + ty])


def backRect():
    pygame.draw.rect(SCREEN, LIGHTGREY, (0, 0, width, height))
    pygame.draw.rect(SCREEN, MEDIUMGREY, (100, 12, 388, 426))


def MainMenu(MousePos, ScrBt, ScrBtExt):
    Extend(ScrBtExt)
    draw(TabExtend, TabExtendLoc[0], TabExtendLoc[1], MousePos, None)
    draw(exitIcon, 12, 377, MousePos, "Exit ")
    draw(overIcon, 12, 304, MousePos, "Overview  ")
    draw(hdIcon, 12, 231, MousePos, "HD Info ")
    draw(memIcon, 12, 158, MousePos, "Memory Info  ")
    draw(processorIcon, 12, 85, MousePos, "Processor Info")
    draw(pcIcon, 12, 12, MousePos, "System Info ")


def pids_to_list():

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
        except psutil.NoSuchProcess:
            pass
        else:
            pinfo['mem'] = BytesConversion(psutil.Process(pinfo['pid']).memory_info().rss)
            username = str(pinfo['username']).split('\\')
            if len(username) > 1:
                pinfo['username'] = username[1]
            else:
                pinfo['username'] = username[0]
        PIDInfo.append(pinfo)


def loop():
    global extend, width, height, cont, Page, ScrBt, ScrBtExt, SCREEN, MousePos, TabFiles, TabProcessos, path, file_loc, folder_loc, path_cont, listdir
    
    pids_to_list()
    while not EndProgram:
        if extend == True and 500 <= width < 950:
            pygame.image.save(SCREEN, "screenshot.png")
            TempScreen = pygame.image.load("screenshot.png")
            for i in range(9):
                width += 50
                SCREEN = pygame.display.set_mode((width, height))
                SCREEN.blit(FundoCinza, (500, 0))
                SCREEN.blit(TempScreen, (0, 0))
                pygame.display.update()
            os.remove("screenshot.png")


        elif extend is False and 950 >= width > 500:
            pygame.image.save(SCREEN, "screenshot.png")
            TempScreen = pygame.image.load("screenshot.png")
            for i in range(9):
                width -= 50
                SCREEN = pygame.display.set_mode((width, height))
                SCREEN.blit(TempScreen, (0, 0))
                pygame.display.update()
            os.remove("screenshot.png")

        # Taxa de Atualização de Dados
        if cont == 30:
            Cpu_Percent_Cores = psutil.cpu_percent(interval=0, percpu=True)
            Cpu_Percent = psutil.cpu_percent(interval=0)
            cont = 0
        cont += 1
        # Taxa de Atualização de Dados

        MousePos = pygame.mouse.get_pos()
        backRect()
        InfoUp()

        # Paginas
        if Page == 0:
            PcInfo(ScrBt)
        elif Page == 1:
            ProcessorInfo(SCREEN, Cpu_Percent_Cores, Cpu_Percent)
        elif Page == 2:
            MemoryInfo()
        elif Page == 3:
            HdInfo(ScrBt)
        elif Page == 4:
            Overview()
        # Paginas
        MainMenu(MousePos, ScrBt, ScrBtExt)

        # FPS
        fps = FONT_CALIBRI.render(str(int(TIME.get_fps())), True, pygame.Color('white'))
        SCREEN.blit(fps, (480, 430))
        # FPS

        pygame.display.update()
        TIME.tick(60)
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if Page < 4:
                        Page += 1
                        ScrBt = 0
                    elif Page == 4:
                        Page = 0
                        ScrBt = 0
                if event.key == pygame.K_LEFT:
                    if Page > 0:
                        Page -= 1
                        ScrBt = 0
                    elif Page == 0:
                        Page = 4
                        ScrBt = 0
                if event.key == pygame.K_SPACE:
                    Page = 4
                    ScrBt = 0

            if Page == 0 or Page == 3 or Page == 4:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if MousePos[0] < 500 and -ScrlSize <= ScrBt < 0:
                            ScrBt += 10
                        if MousePos[0] > 500 and -ScrlSizeExt <= ScrBtExt < 0:
                            ScrBtExt += 30
                    if event.button == 5:
                        if MousePos[0] < 500 and 0 >= ScrBt > -ScrlSize:
                            ScrBt -= 10
                        if MousePos[0] > 500 and -ScrlSizeExt < ScrBtExt <= 0:
                            ScrBtExt -= 30
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if MousePos[0] < 500 and -ScrlSize <= ScrBt < 0:
                            ScrBt += 10
                        if MousePos[0] > 500 and -ScrlSizeExt <= ScrBtExt < 0:
                            ScrBtExt += 30
                    if event.key == pygame.K_DOWN:
                        if MousePos[0] < 500 and 0 >= ScrBt > -ScrlSize:
                            ScrBt -= 10
                        if MousePos[0] > 500 and -ScrlSizeExt < ScrBtExt <= 0:
                            ScrBtExt -= 30
                if ScrlSize > 425 or ScrlSize == 0:
                    if ScrBt < -ScrlSize:
                        ScrBt = -ScrlSize
                    elif ScrBt > 0:
                        ScrBt = 0
                if ScrlSizeExt > 315 or ScrlSizeExt == 0:
                    if ScrBtExt < (-ScrlSizeExt) + 285:
                        ScrBtExt = (-ScrlSizeExt) + 285
                    elif ScrBtExt > 0:
                        ScrBtExt = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 88 > MousePos[0] > 12:
                        if 73 > MousePos[1] > 12:
                            Page = 0
                            ScrBt = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 88 > MousePos[0] > 12:
                        if 146 > MousePos[1] > 85:
                            Page = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 88 > MousePos[0] > 12:
                        if 219 > MousePos[1] > 158:
                            Page = 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 88 > MousePos[0] > 12:
                        if 292 > MousePos[1] > 231:
                            Page = 3
                            ScrBt = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 88 > MousePos[0] > 12:
                        if 365 > MousePos[1] > 304:
                            Page = 4

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if 88 > MousePos[0] > 12:
                        if 438 > MousePos[1] > 377:
                            raise SystemExit

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if TabExtendLoc[0] + TabExtendRect[2] > MousePos[0] > TabExtendLoc[0]:
                        if TabExtendLoc[1] + TabExtendRect[3] > MousePos[1] > TabExtendLoc[1]:
                            if extend:
                                extend = False
                            else:
                                extend = True

            if extend:

                if TabFiles:
                    if MousePos[0] > 500:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            for folder in folder_loc:
                                if folder[1] < MousePos[0] < folder[1]+40 and folder[2] < MousePos[1] < folder[2]+40:
                                    path.append(str(path[path_cont] + str(folder[0]) + "\\"))
                                    path_cont += 1
                                    ScrBtExt = 0
                                    try:
                                        listdir = os.listdir(path[path_cont])
                                    except Exception as erro:
                                        print(str(erro))
                                    break
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                                if path_cont > 0:
                                    path.pop()
                                    path_cont -= 1
                                    ScrBtExt = 0
                                    listdir = os.listdir(path[path_cont])

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        TabProcessosRect = (pygame.Surface.get_rect(TabProcessosImg[0]))
                        TabProcessosLoc = (width / 2 + 25, 45)
                        if TabProcessosLoc[0] + TabProcessosRect[2] > MousePos[0] > TabProcessosLoc[0]:
                            if TabProcessosLoc[1] + TabProcessosRect[3] > MousePos[1] > TabProcessosLoc[1]:
                                TabProcessos = True
                                TabFiles = False
                                ScrBtExt = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        TabFilesRect = (pygame.Surface.get_rect(TabFilesImg[0]))
                        TabFilesLoc = (width - 119, 45)
                        if TabFilesLoc[0] + TabFilesRect[2] > MousePos[0] > TabFilesLoc[0]:
                            if TabFilesLoc[1] + TabFilesRect[3] > MousePos[1] > TabFilesLoc[1]:
                                TabFiles = True
                                TabProcessos = False
                                ScrBtExt = 0

            if event.type == pygame.QUIT:
                raise SystemExit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                raise SystemExit


if __name__ == "__main__":
    ImageUpload()
    loop()

