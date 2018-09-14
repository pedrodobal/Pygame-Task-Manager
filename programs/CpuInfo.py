import cpuinfo, psutil

cpu_info = cpuinfo.get_cpu_info()

def brand():
    return str(cpu_info['brand'])
def arch():
    return str(cpu_info['arch'])
def bits():
    return str(cpu_info['bits'])
def freq():
    cpu_freq = psutil.cpu_freq()
    return cpu_freq
def cores():
    cores = str(psutil.cpu_count())
    cores = cores + " (" + str(psutil.cpu_count(logical=False)) + ")"
    return cores