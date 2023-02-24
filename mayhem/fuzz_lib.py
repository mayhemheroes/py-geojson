#!/usr/bin/env python3

import atheris
import sys
import fuzz_helpers
from typing import List, Tuple

with atheris.instrument_imports():
    import geojson


def get_coord_list(fdp: fuzz_helpers.EnhancedFuzzedDataProvider, count: int) -> List[Tuple[float, float]]:
    return [(fdp.ConsumeRegularFloat(), fdp.ConsumeRegularFloat()) for _ in range(count)]


def get_point(fdp: fuzz_helpers.EnhancedFuzzedDataProvider) -> geojson.Point:
    return geojson.Point((fdp.ConsumeRegularFloat(), fdp.ConsumeRegularFloat()))


def get_line_string(fdp: fuzz_helpers.EnhancedFuzzedDataProvider) -> geojson.LineString:
    coords = get_coord_list(fdp, fdp.ConsumeIntInRange(1, 6))
    return geojson.LineString(coords)


def build_feature(fdp: fuzz_helpers.EnhancedFuzzedDataProvider) -> geojson.Feature:
    properties = fuzz_helpers.build_fuzz_dict(fdp, [str, str])
    return geojson.Feature(geometry=get_point(fdp), id=fdp.ConsumeInt(1), properties=properties)


def TestOneInput(data):
    fdp = fuzz_helpers.EnhancedFuzzedDataProvider(data)
    test = fdp.ConsumeIntInRange(0, 9)

    if test == 0:
        get_point(fdp)
    elif test == 1:
        coords = get_coord_list(fdp, fdp.ConsumeIntInRange(1, 6))
        geojson.MultiPoint(coords)
    elif test == 2:
        get_line_string(fdp)
    elif test == 3:
        coords = fuzz_helpers.build_fuzz_list(fdp, [list, float])
        geojson.MultiLineString(coords)
    elif test == 4:
        coords = fuzz_helpers.build_fuzz_list(fdp, [list, float])
        geojson.Polygon(coords)
    elif test == 5:
        coords = fuzz_helpers.build_fuzz_list(fdp, [tuple, list, float])
        geojson.MultiPolygon(coords)
    elif test == 6:
        geojson.GeometryCollection([get_point(fdp), get_line_string(fdp)])
    elif test == 7:
        build_feature(fdp)
    elif test == 8:
        features = [build_feature(fdp) for _ in range(fdp.ConsumeIntInRange(0, 8))]
        geojson.FeatureCollection(features)
    else:
        pt = get_point(fdp)
        dumped_pt = geojson.dumps(pt, sort_keys=fdp.ConsumeBool())
        loaded_pt = geojson.loads(dumped_pt)
        assert pt == loaded_pt, "Loads failed! %s != %s" % (pt, loaded_pt)


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
