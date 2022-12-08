from gui import *

def main():
    window = Tk()
    window.title('Final Project')
    window.geometry('360x620')
    window.resizable(False, False)

    widgets = GUI(window)
    window.mainloop()

if __name__ == '__main__':
    main()
