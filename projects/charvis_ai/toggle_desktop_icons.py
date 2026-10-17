import win32gui
import win32con

# Function to toggle desktop icons
def toggle_desktop_icons():
    hwnd = win32gui.FindWindow('Progman', 'Program Manager')
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    if style & win32con.WS_VISIBLE:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    else:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

if __name__ == '__main__':
    toggle_desktop_icons()
