from input import INPUT_DATA


#                  50 -> 98 98 -> 100
#                  52 -> 100 50 -> 2
# 0 -> 15 15 -> 52 52-> 54
# 39-> 51 0  -> 37 37 -> 39
# 
# Could also be reprsented as
# seed      0 -> 15   (0)
# soil      0 -> 15   (0)
# fert      0 -> 15   (0)
# water     39 -> 51  (39)
# light     7 -> 22   (-32)
# temp      

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


def calculate_intervals(numbers):
    intervals = []

    for index, number in enumerate(numbers):
        is_seed = (index + 1) % 2

        if not is_seed:
            continue

        intervals.append([number, numbers[index + 1] + number])

    return intervals


def parse_input_data(input_data):
    lines = input_data.split("\n\n")

    seeds_text = lines[0]
    seeds = []
    

    for number_text in seeds_text.split(" "):
        if number_text.isdigit():
            seeds.append(int(number_text))

    seed_intervals = calculate_intervals(seeds)

    # Map Data
    seed_to_soil_map = PlantMap()
    soil_to_fertilizer_map = PlantMap()
    fertilizer_to_water_map = PlantMap()
    water_to_light_map = PlantMap()
    light_to_temperature_map = PlantMap()
    temperature_to_humidty_map = PlantMap()
    humidity_to_location_map = PlantMap()
    resource_map_intervals = []

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
        source_numbers = []
        destination_numbers = []

        for keyword in keyword_to_map.keys():
            if keyword in data:
                current_keyword = keyword
                current_map = keyword_to_map[keyword]
        
        for line in data.split("\n"):
            if current_keyword not in line and line != "":
                destination, source, rangee = line.split(" ")
                current_map.add_range(int(destination), int(source), int(rangee))
                source_numbers.append(int(source))
                source_numbers.append(int(rangee))
                destination_numbers.append(int(destination))
                destination_numbers.append(int(rangee))

        if source_numbers:
            # Add source first, then destination
            resource_map_intervals.append([
                calculate_intervals(source_numbers),
                calculate_intervals(destination_numbers)
            ])

    return [
        seeds,
        seed_intervals,
        resource_map_intervals,
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
    seeds, _, _, maps = parse_input_data(INPUT_DATA)

    locations = [
        traverse_seed_to_location(seed, maps)
        for seed in seeds
    ]

    return min(locations)


def merge_intervals(intervals):
    merged_intervals = []
    current_start = None
    current_end = 0

    for index, interval in enumerate(intervals):
        interval_start = interval[0]
        interval_end = interval[1]

        if current_start is None:
            current_start = interval_start
            current_end = interval_end

        if interval_end >= current_end:
            current_end = interval_end
        else:
            # end of the interval
            current_start = None
            merged_intervals.append([current_start, current_end])

    if current_start is not None:
        merged_intervals.append([current_start, current_end])

    return merged_intervals


class IntervalTracker:
    def __init__(self, seed_start, seed_end, start, end):
        self.seed_start = seed_start
        self.seed_end = seed_end
        self.start = start
        self.end = end

    def is_in_range(self, number):
        return number >= self.start and number <= self.end

    def split_interval(self, new_split_intervals):
        """
            Self:  [[1, 9]]
            New Split: [[3, 5], [8, 12]]

            Step 1: [1-2, 3-5, 6-9] - split 1,9 amongst new split
            Step 2: [1-2, 3-5, 6-7, 8-9]
        """
        new_intervals = [self]

        current_start = self.start
        current_seed_start = self.seed_start
        current_end = self.end
        current_seed_end = self.seed_end

        # for current_interval in new_intervals:
        for split_interval in new_split_intervals:
            if split_interval.end <= current_start:
                new_interval_end = split_interval.end
                # get the new seed end
                current_seed_end = (new_interval_end - current_start) + current_seed_start
                new_intervals.append(
                    IntervalTracker(
                        seed_start=current_seed_start,
                        seed_end=current_seed_end,
                        start=current_start,
                        end=new_interval_end
                    )
                )
                # set the new start
                current_start = new_interval_end + 1
            else:


        

def normalize_interval_to_mapping_scope(input_intervals, source_intervals, destination_intervals):
    """
    Given two intervals, input and mapping, create a new interval from the input that meets the scope.
        1. output intervals must start and end within the range of the scope intervals
        2. "fill in" the gaps using the challenge logic of "if not in "source" the number is the map

    Input:  [[1, 9]]
    Source: [[3, 5], [8, 12]]
    Dest:   [[7, 9], [12, 16]]

    Step 1: [[1, 2], [3, 5], [6, 7], [8-9]] - split intervals from input to meet source, but maintain bounds of input
    Step 2: [[1, 2], [7, 9], [6, 7], [12-13]] seed tracker would know that 7-9 was originally 3-5 and 1-5 was 8-12

    # Example 2
    Input:  [[1, 5], [8, 12]]
    Source: [[1, 3], [6, 9]]
    Dest:   [[10, 13], [16, 19]]

    Step 1: [[1, 3], [4, 5], [8, 9], [10, 12]] - split intervals to confirm
    Step 2: [[10, 13], [4, 5], [18, 19], [10, 12]  - swap out using the source to destination
    
    Need to figure out how to maintain the trace back to the input. Create a class that maintains the current range but the original seed range it represents
    """
    output_intervals = []

    for interval in input_intervals:



def solve_part_two():
    _, seed_intervals, resource_map_intervals, maps = parse_input_data(INPUT_DATA)
    # sort the seed intervals
    seed_intervals.sort(key=lambda x:x[0])

    print(seed_intervals)
    # resource_map_intervals = [
    #   intervals = [
    #       source->dest[
    #            source [x, y],
    #            dest  [a, b]
    #       ]
    #   ]
    # ]
    # sort the intervals in place
    merged_resource_map_intervals = []
    merged_seed_interval = merge_intervals(seed_intervals)

    print(merged_seed_interval)
    print(f"Seeds Len:  {len(merged_seed_interval)}")

    for resource_intervals in resource_map_intervals:
        resource_intervals.sort(key=lambda x:x[0][0])
        merged_resource_map_intervals.append([
            merge_intervals(resource_intervals[0]),
            merge_intervals(resource_intervals[1])
        ])


    for resource_intervals in merged_resource_map_intervals:
        print(f"Len:     {len(resource_intervals[0])}")
    all_sorted_intervals = seed_intervals + resource_map_intervals

    lowest_seed = merged_resource_map_intervals[0][0]

    for layer_number, layer in enumerate(merged_resource_map_intervals):
        is_destination_layer = layer_number % 2

        if is_destination_layer:
            # find new lowest seed
            pass
        else:
            # transfer to new number set

    return 0

def interval_traverser()


def main():
    print(f"Answer 1:     {solve_part_one()}")
    print(f"Answer 2:     {solve_part_two()}")


if __name__ == "__main__":
    main()