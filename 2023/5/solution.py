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
        is_range = (index) % 2

        if is_range:
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
    resource_intervals = []
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
        number_pairs = []
        for keyword in keyword_to_map.keys():
            if keyword in data:
                current_keyword = keyword
                current_map = keyword_to_map[keyword]
        
        for line in data.split("\n"):
            if current_keyword not in line and line != "":
                destination, source, rangee = line.split(" ")
                current_map.add_range(int(destination), int(source), int(rangee))
                number_pairs.append({
                    "source": [int(source), int(source) + int(rangee) - 1],
                    "dest": [int(destination), int(destination) + int(rangee) - 1]
                })
                source_numbers.append(int(source))
                source_numbers.append(int(rangee))
                destination_numbers.append(int(destination))
                destination_numbers.append(int(rangee))
        if number_pairs:
            resource_intervals.append(number_pairs)
        if source_numbers:
            # Add source first, then destination
            # print(destination_numbers)
            resource_map_intervals.append({
                "source": calculate_intervals(source_numbers),
                "dest": calculate_intervals(destination_numbers)
            })

    return [
        seeds,
        seed_intervals,
        resource_map_intervals,
        resource_intervals,
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
    seeds, _, _, _, maps = parse_input_data(INPUT_DATA)

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
    """
    Start and End are the Sources
    Dest are errr the destinations
    Seeds will be copied through with no transformations so we can trace it back
    """
    def __init__(self,  start, end, dest_start = 0, dest_end = 0):
        self.start = start
        self.end = end
        self.dest_start = dest_start
        self.dest_end = dest_end
        self.dest_offset = dest_start - start


    def __repr__(self):
        # return f"[{self.start}, {self.end}]"
        return f"[{self.start}, {self.end}]({self.dest_start}-{self.dest_end})"

    def is_in_range(self, number):
        return number >= self.start and number <= self.end

    def convert_from_source_to_dest(self):
        self.start = self.dest_start
        self.end = self.dest_end
        self.dest_start = None
        self.dest_end = None
        self.dest_offset = 0

    def split_interval(self, split_intervals):
        """
            Self:  [[1, 9]]
            New Split: [[3, 5], [8, 12]]

            Step 1: [1-2, 3-5, 6-9] - split 1,9 amongst new split
            Step 2: [1-2, 3-5, 6-7, 8-9]
        """
        new_intervals = []
        current_index = self.start
        max_end = self.end
        if current_index == max_end:
            # print("[0] Add 1")
            # interval is just 1 number
            for split_interval in split_intervals:
                if current_index >= split_interval.start and current_index <= split_interval.end:
                    return [IntervalTracker(
                        start=current_index,
                        end=max_end,
                        dest_start=current_index + split_interval.dest_offset,
                        dest_end=max_end + split_interval.dest_offset,
                    )]

        # create splits until we cover this split from start to finish
        while current_index < max_end:
            # iterate through each split interval until our current index is past this split's max end
            for split_interval in split_intervals:
                split_start = split_interval.start
                split_end = split_interval.end
                if current_index > split_end or current_index > max_end:   # (10 > 9)
                    continue
                if split_start == current_index and split_end == max_end:  #  split is the same as interval
                    # print("[1] Add 1")
                    new_intervals.append(
                        IntervalTracker(
                            start=current_index,
                            end=max_end,
                            dest_start=split_interval.dest_start,
                            dest_end=split_interval.dest_end
                        )
                    )
                    current_index = max_end
                elif split_start > current_index and split_end < max_end:  # split is in the middle of the interval
                    # print("[2] Add 3")
                    # Front interval
                    new_intervals.append(
                        IntervalTracker(
                            start=current_index,
                            end=split_start,
                            dest_start=current_index + split_interval.dest_offset,
                            dest_end=split_start + split_interval.dest_offset
                        )
                    )
                    current_index = split_start
                    # Middle interval
                    new_intervals.append(
                        IntervalTracker(
                            start=current_index,
                            end=split_end,
                            dest_start=current_index + split_interval.dest_offset,
                            dest_end=split_end + split_interval.dest_offset
                        )
                    )
                    current_index = split_end
                    # End Interval
                    new_intervals.append(
                        IntervalTracker(
                            start=current_index,
                            end=max_end,
                            dest_start=current_index + split_interval.dest_offset,
                            dest_end=max_end + split_interval.dest_offset
                        )
                    )
                    current_index = max_end  # move index to 3 | move to 8
                elif split_start <= current_index and split_end >= self.end:  # check if split encompasses interval
                    # print("[3] add 1")
                    final_split = IntervalTracker(
                        start=current_index,
                        end=max_end,
                        dest_start=current_index + split_interval.dest_offset,
                        dest_end=max_end + split_interval.dest_offset
                    )
                    new_intervals.append(final_split)
                    current_index = max_end + 1
                elif split_start < current_index and split_end < max_end:  # if split overlaps with front of interval
                    # print("[4] Add 2")
                    new_intervals.append(
                        IntervalTracker(
                            start=current_index,
                            end=split_end,
                            dest_start=current_index + split_interval.dest_offset,
                            dest_end=split_end + split_interval.dest_offset
                        )
                    )
                    current_index = split_end + 1
            if current_index < max_end:
                # print("[5] Add 1")
                new_intervals.append(
                    IntervalTracker(
                        start=current_index,
                        end=max_end,
                        dest_start=current_index + self.dest_offset,
                        dest_end=max_end + self.dest_offset
                    )
                )
                current_index = max_end + 1 

        return new_intervals


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
        pass

    return None


def solve_part_two():
    _, seed_intervals, resource_map_intervals, resource_intervals, _ = parse_input_data(INPUT_DATA)
    # sort the seed intervals
    seed_intervals.sort(key=lambda x:x[0])

    # print(seed_intervals)
    # resource_map_intervals = [
    #   intervals = [
    #       source->dest[
    #            source [x, y],
    #            dest  [a, b]
    #       ]
    #   ]
    # ]
    # sort the intervals in place

    for intervals in resource_intervals:
        # sort them
        intervals.sort(key=lambda x:x['source'][0])


    seed_intervals = [
        IntervalTracker(
            start=seed_interval[0],
            end=seed_interval[1],
        )
        for seed_interval in seed_intervals
    ]

    resource_interval_list = []

    for intervals in resource_intervals:
        resource_interval_trackers = []
        for interval in intervals:
            resource_interval_trackers.append(
                IntervalTracker(
                    start=interval['source'][0],
                    end=interval['source'][1],
                    dest_start=interval['dest'][0],
                    dest_end=interval['dest'][1],
                )
            )

        resource_interval_list.append(resource_interval_trackers)


    first_resource_interval = resource_interval_list.pop(0)

    current_intervals = []
    # print(seed_intervals)
    # print(first_resource_interval)

    # create intervals where the seed is part of the first resource
    for seed_interval in seed_intervals:
        new_intervals = seed_interval.split_interval(first_resource_interval)
        current_intervals += new_intervals

    # print(current_intervals)
    # print("\n")

    # convert source to dest
    for interval in current_intervals:
        interval.convert_from_source_to_dest()
        # Re-Sort
    current_intervals.sort(key=lambda interval:interval.start)


    for resource_intervals in resource_interval_list:
        new_intervals = []
        current_intervals_temp = current_intervals
        # print(f"S:  {current_intervals_temp}")
        # print(resource_intervals)
        for interval in current_intervals_temp:
            split_intervals = interval.split_interval(resource_intervals)

            new_intervals += split_intervals
        # print(f"F: {new_intervals}")
        # print(f"Len:    {len(new_intervals)}")
        # print("\n")
        # convert from source to dest
        for interval in new_intervals:
            interval.convert_from_source_to_dest()

        # re-sort
        new_intervals.sort(key=lambda interval:interval.start)

        current_intervals = new_intervals

    # print("\nDone")
    # print(current_intervals)

    return current_intervals[0].start

def main():
    print(f"Answer 1:     {solve_part_one()}")
    print(f"Answer 2:     {solve_part_two()}")


if __name__ == "__main__":
    main()