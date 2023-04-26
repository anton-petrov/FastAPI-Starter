import json

from models import DhtSchema


def test() -> None:
    # Load data
    with open("../tests/data/example1.json") as f:
        data = json.load(f)
        dht = DhtSchema.parse_raw(json.dumps(data, indent=2))
        print(dht)


if __name__ == "__main__":
    test()
