village_layouts = []

village_1 = {
    "name":"Test Villge",
    "size":25,
    "well":{
        "size":1,
        "row":10,
        "col":12
    },
    "inn":{
        "size":5,
        "row":4,
        "col":12
    },
    "warehouse":{
        "size":5,
        "row":3,
        "col":3
    },
    "shop":{
        "size":5,
        "row":10,
        "col":3
    },
    "barn":{
        "size":5,
        "row":21,
        "col":19
    },
    "houses":{
        "size":3,
        "coords":{
            # row:cols
            5:[17, 21],
            10:[8, 18, 22],
            15:[15, 19, 23],
            16:[3, 7]            
        }
    },
    "stalls":{
        "size":1,
        "coords":{
            # row:cols
            14:[10,11],            
            16:[10,11],
            18:[10,11],           
        }
    },
    "paths": {
        "size": 1,
        "coords": {
            # row:cols (+1 added to range for readability)
            6:  [3],
            7:  [*range(3, 21+1)],
            8:  [12],
            9:  [*range(11, 13+1)],
            10: [11, 13],
            11: [11, 12, 13],
            12: [8, 12, 18, 22],
            13: [*range(3, 22+1)],
            14: [12],
            15: [*range(10, 12+1)],
            16: [12],
            17: [10, 11, 12, 15, 19, 23],
            18: [3, 7, *range(12, 23+1)],
            19: [*range(3, 12+1)],
            20: [12],
            21: [12],
            22: [12],
            23: [12],
            24: [*range(12, 19+1)],
        }
    },
    "farms": {
        "size": 1,
        "coords": {
            # row: cols (+1 added to range for readability)
            19: [*range(13, 16+1)],
            20: [*range(1, 10+1), *range(13, 16+1)],
            21: [*range(1, 10+1), *range(13, 16+1)],
            22: [*range(1, 10+1), *range(13, 16+1)],
            23: [*range(1, 10+1), *range(13, 16+1)],
        }
    }

}

village_layouts.append(village_1)