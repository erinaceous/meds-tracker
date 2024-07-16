#!/usr/bin/env python3
import json
import time


def main():
    print(
        json.dumps({
            "processed_at": time.time()
        }, indent=1)
    )


if __name__ == "__main__":
    main()
