from input import INPUT_DATA


class MapRangeThing:
    def __init__(self, destination, source, rangee):
        self.destination = destination
        self.max_destination = destination + rangee
        self.source = source
        self.max_source = source + rangee
        self.rangee = rangee

    def is_in_range(self, number):
        return self.source <= number and number <= self.max_source
    
    def get_destination(self, number):
        if self.is_in_range(number):
            difference = number - self.source
            return self.destination + difference
        raise Exception("Oh No")


class PlantMap:
    def __init__(self):
        self.ranges = []

    def add_range(self, destination, source, rangee):
        self.ranges.append(
            MapRangeThing(
                destination,
                source,
                rangee
            )
        )

    def get_destination(self, source):
        for range_thing in self.ranges:
            if range_thing.is_in_range(source):
                return range_thing.get_destination(source)

        return source


def parse_input_data(input_data):
    lines = input_data.split("\n\n")

    seeds_text = lines[0]
    seeds = []

    for number_text in seeds_text.split(" "):
        if number_text.isdigit():
            seeds.append(int(number_text))

    # Map Data
    seed_to_soil_map = PlantMap()
    soil_to_fertilizer_map = PlantMap()
    fertilizer_to_water_map = PlantMap()
    water_to_light_map = PlantMap()
    light_to_temperature_map = PlantMap()
    temperature_to_humidty_map = PlantMap()
    humidity_to_location_map = PlantMap()

    keyword_to_map = {
        "seed-to-soil map:": seed_to_soil_map,
        "soil-to-fertilizer map:": soil_to_fertilizer_map,
        "fertilizer-to-water map:": fertilizer_to_water_map,
        "water-to-light map:": water_to_light_map,
        "light-to-temperature map:": light_to_temperature_map,
        "temperature-to-humidity map:": temperature_to_humidty_map,
        "humidity-to-location map:": humidity_to_location_map,
    }

    for data in lines:
        current_map = {}
        current_keyword = ""
        for keyword in keyword_to_map.keys():
            if keyword in data:
                current_keyword = keyword
                current_map = keyword_to_map[keyword]
        
        for line in data.split("\n"):
            if current_keyword not in line and line != "":
                destination, source, rangee = line.split(" ")
                current_map.add_range(int(destination), int(source), int(rangee))

    return [
        seeds,
        [
            seed_to_soil_map,
            soil_to_fertilizer_map,
            fertilizer_to_water_map,
            water_to_light_map,
            light_to_temperature_map,
            temperature_to_humidty_map,
            humidity_to_location_map,
        ]
    ]


def traverse_seed_to_location(
    seed,
    maps
):
    current_location = seed
    (
        seed_to_soil_map,
        soil_to_fertilizer_map,
        fertilizer_to_water_map,
        water_to_light_map,
        light_to_temperature_map,
        temperature_to_humidty_map,
        humidity_to_location_map
    ) = maps

    current_location = seed_to_soil_map.get_destination(current_location)
    current_location = soil_to_fertilizer_map.get_destination(current_location)
    current_location = fertilizer_to_water_map.get_destination(current_location)
    current_location = water_to_light_map.get_destination(current_location)
    current_location = light_to_temperature_map.get_destination(current_location)
    current_location = temperature_to_humidty_map.get_destination(current_location)
    current_location = humidity_to_location_map.get_destination(current_location)

    return current_location


def solve_part_one():
    seeds, maps = parse_input_data(INPUT_DATA)

    locations = [
        traverse_seed_to_location(seed, maps)
        for seed in seeds
    ]

    return min(locations)


def solve_part_two():
    return 0


def main():
    print(f"Answer 1:     {solve_part_one()}")
    print(f"Answer 2:     {solve_part_two()}")


if __name__ == "__main__":
    main()