
import winreg,sys,os,ctypes

def is_admin():#判断管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class win_startup():
    '''
    程序开机启动类
    '''
    def __init__(self):
        #判断管理员权限
        if is_admin()==False:
            #重新启动程序
            ctypes.windll.shell32.ShellExecuteW(None,"runas", sys.executable, __file__, None, 1)
            sys.exit(0)
        self.regedit_name=self._get_regedit_name()
        self.regedit_link=r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'

    def _get_regedit_name(self):
        (filepath, filename) = os.path.split(sys.argv[0])
        (name, suffix) = os.path.splitext(filename)
        return name

    def startup_load(self):#读取是否写入开机启动
        '''
        读取是否写入开机启动,写入则返回写入的路径,否则返回None
        '''
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self.regedit_link, access=winreg.KEY_ALL_ACCESS)
            software, REG_SZ = winreg.QueryValueEx(key, self.regedit_name)
            software = bytes(software,encoding="utf-8").decode()
            winreg.CloseKey(key)
            key.Close()
        except :
            software =None
        return(software)

    def startup_write(self):#写入开机启动
        '''
        写入开机启动,成功返回True,否则返回False
        '''
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self.regedit_link, access=winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key,self.regedit_name, 0, winreg.REG_SZ,sys.argv[0])
        winreg.CloseKey(key)
        key.Close()
        try:

            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,self.regedit_link, access=winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key,self.regedit_name, 0, winreg.REG_SZ,sys.argv[0])
            winreg.CloseKey(key)
            key.Close()
            return(True)
        except :
            return(False)

    def startup_delete(self):#取消开机启动
        '''
        取消开机启动,成功返回True,否则返回False
        '''
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.regedit_link, access=winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key,self.regedit_name)
            winreg.CloseKey(key)
            key.Close()
            return(True)
        except :
            return(False)


  
