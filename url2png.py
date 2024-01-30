import argparse
import datetime
import time
# import os
# import shutil

from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def take_screenshot(url, name=None, headless=True, width=None, height=None, wait=None, filepath=None, quiet=False):
    if name is None:
        now = datetime.datetime.now()
        date_time = now.isoformat().split(".")[0]
        name = f"{date_time}-{urlparse(url).netloc}-.png"
        # name = name.rsplit("-", maxsplit=1)[0]
        # extension = name.rsplit(".", maxsplit=1)[-1]
        # filename = name + "." + extension

    driver = '/home/cd/Downloads/chromedriver-linux64/chromedriver'
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=driver)

    driver.get(url)
    if wait is not None:
        time.sleep(wait)

    S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment   

    if filepath is not None :
        output_filename = filepath / name
    else:  # Move to current working directory
        output_filename = Path().cwd() / name

    driver.find_element_by_tag_name('body').screenshot(str(output_filename))

    if not quiet:
        print(output_filename.resolve())
    driver.quit()
    return output_filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--width", default=1280)
    parser.add_argument("--height", default=960)
    parser.add_argument("--no-headless", action="store_true")
    parser.add_argument("--wait", default=0)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--filepath", default="./screenshuts")
    parser.add_argument("--filename")
    args = parser.parse_args()

    filepath, filename = None, None
    if args.filepath:
        filepath = Path(args.filepath)
        if not filepath.exists():
            filepath.mkdir(parents=True)
    if args.filename:
        filename = Path(args.filename)

    screenshot_filename = take_screenshot(
        url=args.url,
        width=args.width,
        height=args.height,
        headless=not args.no_headless,
        wait=args.wait,
        filepath=filepath,
        name=filename
    )



if __name__ == "__main__":
    main()