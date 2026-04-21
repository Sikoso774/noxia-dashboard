import sys
from app import App

if __name__ == "__main__":
    try :
        app = App()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit(0)