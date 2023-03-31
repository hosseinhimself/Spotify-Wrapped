import argparse
from get_info import wrapped


def main(args):
    # Do something with the command-line arguments
    if args.mode == "U":
        print("Spotify Wrapped Alternative by Hossein Mohseni")
        print("\tPlease Wait...")
        wrapped(args.object)
        print("Your Spotify Wrapped saved Successfully!")
    elif args.mode == "P":
        print("Simple mode enabled for " + args.object)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spotify Wrapped Alternative by Hossein Mohseni")
    parser.add_argument("mode", help="mode of operation: P for playlist or U for user")
    parser.add_argument("object", help="If you are working with a playlist, please enter its address. And if you are working with a user, please enter their username.")
    args = parser.parse_args()
    main(args)
