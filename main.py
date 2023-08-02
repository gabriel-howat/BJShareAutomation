#from config.configuration import configure_app
from login.login import open_login
from system_tray.system_tray import setup_system_tray
from download_manager.download_manager import run




def main():
    print("running main")
    #configure_app()
    setup_system_tray()
    driver = open_login()
    run(driver)


if __name__ == "__main__":
    main()