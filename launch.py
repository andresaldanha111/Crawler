from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler


def main(config_file, restart):
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart)
    crawler = Crawler(config, restart)
    crawler.start()


if __name__ == "__main__":
    # Create ArgumentParser instance with description
    parser = argparse.ArgumentParser(description="This script does something useful.")
    
    # Add arguments with help messages
    parser.add_argument("--restart", action="store_true", default=False, help="Restart the script.")
    parser.add_argument("--config_file", type=str, default="config.ini", help="Path to the configuration file.")
    
    # Use argparse.ArgumentParser() context manager
    with parser:
        # Parse arguments and call main() function
        args = parser.parse_args()
        main(args.config_file, args.restart)
