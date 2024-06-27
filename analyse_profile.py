import pstats
import sys


def analyze_profile(profile_file):
    # Create a Stats object from the profile file
    stats = pstats.Stats(profile_file)

    # Sort the statistics by the cumulative time spent in the function
    stats.sort_stats('cumulative')

    # Print the ten functions that took the most cumulative time
    stats.print_stats(10)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_profile.py profile_file")
    else:
        analyze_profile(sys.argv[1])
