
from ortools.sat.python import cp_model
from itertools import combinations


# ============================================================
# 1. NPC DATABASE
# ============================================================

# Priority is read from top to bottom.
# "Others" is the neutral fallback.
# Entries below Others have negative priority.
# Nested lists mean equal priority.

NPCS = {
    "Guide": {
        "enabled": True,
        "npc_priority": [
            ["Clothier", "Zoologist"],
            ["Others"],
            ["Steampunker"],
            ["Painter"],
        ],
        "biome_priority": [
            "Forest",
            "Others",
            "Ocean",
        ]
    },

    "Merchant": {
        "enabled": True,
        "npc_priority": [
            ["Golfer", "Nurse"],
            ["Others"],
            ["Tax Collector"],
            ["Angler"],
        ],
        "biome_priority": [
            "Forest",
            "Others",
            "Desert",
        ]
    },

    "Nurse": {
        "enabled": True,
        "npc_priority": [
            "Arms Dealer",
            "Wizard",
            "Others",
            ["Party Girl", "Dryad"],
            "Zoologist",
        ],
        "biome_priority": [
            "Hallow",
            "Others",
            "Snow",
        ]
    },

    "Demolitionist": {
        "enabled": True,
        "npc_priority": [
            "Tavernkeep",
            "Mechanic",
            "Others",
            "Goblin Tinkerer",
            "Arms Dealer",
        ],
        "biome_priority": [
            "Underground",
            "Others",
            "Ocean",
        ]
    },

    "Dryad": {
        "enabled": True,
        "npc_priority": [
            ["Witch Doctor", "Truffle"],
            "Others",
            "Angler",
            "Golfer",
        ],
        "biome_priority": [
            "Jungle",
            "Others",
            "Desert",
        ]
    },

    "Arms Dealer": {
        "enabled": True,
        "npc_priority": [
            "Nurse",
            "Steampunker",
            "Others",
            "Golfer",
            "Demolitionist",
        ],
        "biome_priority": [
            "Desert",
            "Others",
            "Snow",
        ]
    },

    "Clothier": {
        "enabled": True,
        "npc_priority": [
            "Truffle",
            "Tax Collector",
            "Others",
            "Nurse",
            "Mechanic",
        ],
        "biome_priority": [
            "Underground",
            "Others",
            "Hallow",
        ]
    },

    "Mechanic": {
        "enabled": True,
        "npc_priority": [
            "Goblin Tinkerer",
            "Cyborg",
            "Others",
            "Clothier",
        ],
        "biome_priority": [
            "Snow",
            "Others",
            "Underground",
        ]
    },

    "Goblin Tinkerer": {
        "enabled": True,
        "npc_priority": [
            ["Mechanic"],
            ["Dye Trader"],
            ["Others"],
            ["Clothier"],
            ["Stylist"],
        ],
        "biome_priority": [
            ["Underground"],
            ["Others"],
            ["Jungle"],
        ]
    },

    "Wizard": {
        "enabled": True,
        "npc_priority": [
            ["Golfer"],
            ["Merchant"],
            ["Others"],
            ["Witch Doctor"],
            ["Cyborg"],
        ],
        "biome_priority": [
            ["Hallow"],
            ["Others"],
            ["Ocean"],
        ]
    },

    "Truffle": {
        "enabled": True,
        "npc_priority": [
            ["Guide"],
            ["Dryad"],
            ["Others"],
            ["Clothier"],
            ["Witch Doctor"],
        ],
        "biome_priority": [
            ["Glowing Mushrooms"],
        ]
    },

    "Dye Trader": {
        "enabled": True,
        "npc_priority": [
            ["Arms Dealer", "Painter"],
            "Others",
            "Steampunker",
            "Pirate",
        ],
        "biome_priority": [
            "Desert",
            "Others",
            "Forest",
        ]
    },

    "Party Girl": {
        "enabled": True,
        "npc_priority": [
            ["Wizard", "Zoologist"],
            "Stylist",
            "Others",
            "Merchant",
            "Tax Collector",
        ],
        "biome_priority": [
            "Hallow",
            "Others",
            "Underground",
        ]
    },

    "Painter": {
        "enabled": True,
        "npc_priority": [
            "Dryad",
            "Party Girl",
            "Others",
            ["Cyborg", "Truffle"],
        ],
        "biome_priority": [
            "Jungle",
            "Others",
            "Forest",
        ]
    },

    "Witch Doctor": {
        "enabled": True,
        "npc_priority": [
            ["Dryad", "Guide"],
            "Others",
            "Nurse",
            "Truffle",
        ],
        "biome_priority": [
            "Jungle",
            "Others",
            "Hallow",
        ]
    },

    "Stylist": {
        "enabled": True,
        "npc_priority": [
            "Dye Trader",
            "Pirate",
            "Others",
            "Tavernkeep",
            "Goblin Tinkerer",
        ],
        "biome_priority": [
            "Ocean",
            "Others",
            "Snow",
        ]
    },

    "Angler": {
        "enabled": True,
        "npc_priority": [
            ["Party Girl", "Demolitionist", "Tax Collector"],
            "Others",
            "Tavernkeep",
        ],
        "biome_priority": [
            "Ocean",
            "Others",
            "Desert",
        ]
    },

    "Tax Collector": {
        "enabled": True,
        "npc_priority": [
            ["Merchant"],
            ["Party Girl"],
            ["Others"],
            ["Demolitionist", "Mechanic"],
            ["Santa Claus"],
        ],
        "biome_priority": [
            "Snow",
            "Others",
            "Hallow",
        ]
    },

    "Tavernkeep": {
        "enabled": True,
        "npc_priority": [
            ["Demolitionist"],
            ["Goblin Tinkerer"],
            ["Others"],
            ["Guide"],
            ["Dye Trader"],
        ],
        "biome_priority": [
            "Hallow",
            "Others",
            "Snow",
        ]
    },

    "Golfer": {
        "enabled": True,
        "npc_priority": [
            ["Angler"],
            ["Zoologist", "Painter"],
            ["Others"],
            ["Pirate"],
            ["Merchant"],
        ],
        "biome_priority": [
            "Forest",
            "Others",
            "Underground",
        ]
    },

    "Zoologist": {
        "enabled": True,
        "npc_priority": [
            ["Witch Doctor"],
            ["Golfer"],
            ["Others"],
            ["Angler"],
            ["Arms Dealer"],
        ],
        "biome_priority": [
            "Forest",
            "Others",
            "Desert",
        ]
    },

    # ============================================================
    # Thorium

    "Blacksmith": {
        "enabled": True,
        "npc_priority": [
            "Demolitionist",
            "Weapon Master",
            "Others",
            "Tracker",
        ],
        "biome_priority": [
            "Underground",
            "Others",
        ]
    },

    "Cobbler": {
        "enabled": True,
        "npc_priority": [
            ["Zoologist", "Golfer"],
            "Spiritualist",
            "Others",
            ["Druid", "Dryad", "Angler"],
            "Nurse",
        ],
        "biome_priority": [
            "Forest",
            "Others",
            "Ocean",
        ]
    },

    "Confused Zombie": {
        "enabled": True,
        "npc_priority": [
            "Guide",
            "Clothier",
            "Others",
            "Spiritualist",
        ],
        "biome_priority": [
            "Forest",
            "Others",
            "Snow",
        ]
    },

    "Cook": {
        "enabled": True,
        "npc_priority": [
            "Santa Claus",
            "Truffle",
            "Others",
            "Angler",
            "Cyborg",
        ],
        "biome_priority": [
            "Glowing Mushrooms",
            "Others",
            "Underground",
        ]
    },

    "Desert Acolyte": {
        "enabled": True,
        "npc_priority": [
            ["Nurse", "Spiritualist"],
            "Others",
            "Pirate",
            ["Goblin Tinkerer", "Witch Doctor", "Weapon Master"],
        ],
        "biome_priority": [
            "Desert",
            "Others",
            "Jungle",
        ]
    },

    "Diverman": {
        "enabled": True,
        "npc_priority": [
            "Party Girl",
            "Pirate",
            "Others",
            "Angler",
        ],
        "biome_priority": [
            "Ocean",
            "Others",
            "Desert",
        ]
    },

    "Druid": {
        "enabled": True,
        "npc_priority": [
            "Dryad",
            "Others",
            "Demolitionist",
            "Steampunker",
        ],
        "biome_priority": [
            "Jungle",
            "Others",
            "Snow",
        ]
    },

    "Spiritualist": {
        "enabled": True,
        "npc_priority": [
            ["Stylist", "Witch Doctor"],
            "Others",
            ["Weapon Master", "Tax Collector"],
        ],
        "biome_priority": [
            "Hallow",
            "Others",
            "Underground",
        ]
    },

    "Tracker": {
        "enabled": True,
        "npc_priority": [
            "Tavernkeep",
            ["Guide", "Stylist"],
            "Others",
            "Dye Trader",
            "Desert Acolyte",
        ],
        "biome_priority": [
            "Snow",
            "Others",
            "Forest",
        ]
    },

    # ============================================================
    # AlchemistNPC

    "Alchemist": {
        "enabled": True,
        "npc_priority": [
            "Young Brewer",
            "Mechanic",
            "Others",
            "Brewer",
        ],
        "biome_priority": [
            "Underground",
            "Forest",
            "Others",
            "Snow",
        ]
    },

    "Architect": {
        "enabled": True,
        "npc_priority": [
            "Painter",
            "Goblin Tinkerer",
            "Others",
            "Tax Collector",
        ],
        "biome_priority": [
            "Jungle",
            "Ocean",
            "Others",
            "Snow",
        ]
    },

    "Brewer": {
        "enabled": True,
        "npc_priority": [
            "Young Brewer",
            "Alchemist",
            "Others",
            "Witch Doctor",
        ],
        "biome_priority": [
            "Forest",
            "Jungle",
            "Others",
            "Snow",
        ]
    },

    "Jeweler": {
        "enabled": True,
        "npc_priority": [
            "Merchant",
            "Tax Collector",
            "Others",
            "Party Girl",
        ],
        "biome_priority": [
            "Forest",
            "Jungle",
            "Others",
            "Snow",
        ]
    },

    "Musician": {
        "enabled": True,
        "npc_priority": [
            "Party Girl",
            "Wizard",
            "Others",
            "Goblin Tinkerer",
        ],
        "biome_priority": [
            "Hallow",
            "Underground",
            "Others",
            "Snow",
        ]
    },

    "Operator": {
        "enabled": True,
        "npc_priority": [
            "Cyborg",
            "Steampunker",
            "Others",
            "Clothier",
        ],
        "biome_priority": [
            "Snow",
            "Ocean",
            "Others",
            "Underground",
        ]
    },

    "Tinkerer": {
        "enabled": True,
        "npc_priority": [
            ["Steampunker"],
            ["Mechanic"],
            ["Others"],
            ["Dye Trader"],
        ],
        "biome_priority": [
            "Snow",
            "Underground",
            "Others",
            "Desert",
        ]
    },

    "Young Brewer": {
        "enabled": True,
        "npc_priority": [
            ["Brewer"],
            ["Alchemist"],
            ["Others"],
            ["Goblin Tinkerer"],
        ],
        "biome_priority": [
            "Forest",
            "Desert",
            "Others",
            "Snow",
        ]
    },

    # ============================================================
    # Birds++

    "Bird Watcher": {
        "enabled": True,
        "npc_priority": [
            ["Dryad", "Zoologist"],
            ["Witch Doctor"],
            ["Others"],
            ["Arms Dealer"],
            ["Demolitionist"],
        ],
        "biome_priority": [
            "Jungle",
            "Forest",
            "Others",
            "Ocean",
        ]
    },

    # ============================================================
    # Lost Girl/Nymph Town NPC Mod

    "Found Girl": {
        "enabled": True,
        "npc_priority": [
            ["Dryad", "Princess", "Tax Collector"],
            ["Party Girl", "Clothier", "Wizard", "Guide"],
            ["Others"],
            ["Demolitionist", "Goblin Tinkerer", "Angler"],
        ],
        "biome_priority": [
            ["Forest", "Hallow"],
            ["Snow", "Jungle"],
            ["Others"],
            ["Desert"],
            ["Underground", "Corruption", "Crimson"],
        ]
    },

    # ============================================================
    # Magic Builder

    "Housebearer": {
        "enabled": True,
        "npc_priority": [
            ["Guide"],
            ["Merchant"],
            ["Others"],
            ["Wizard"],
            ["Tax Collector"],
        ],
        "biome_priority": [
            "Forest",
            "Hallow",
            "Others",
            "Underground",
        ]
    },

    # ============================================================
    # Magic Storage

    "Automaton": {
        "enabled": True,
        "npc_priority": [
            ["Mechanic"],
            ["Witch Doctor"],
            ["Others"],
            ["Wizard"],
            ["Tax Collector"],
        ],
        "biome_priority": [
            "Snow",
            "Forest",
            "Others",
            "Desert",
            "Hallow",
        ]
    },
    
    # ============================================================
    # Useful NPCs

    "Alchemist 2": {
        "enabled": True,
        "npc_priority": [
            ["Guide", "Zoologist"],
            ["Others"],
            ["Old Champion"],
        ],
        "biome_priority": [
            ["Forest", "Jungle", "Desert", "Snow"],
            ["Others"],
            ["Ocean"],
        ]
    },
    
    "Builder": {
        "enabled": True,
        "npc_priority": [
            ["Angler"],
            ["Others"],
            ["Martian"],
        ],
        "biome_priority": [
            ["Jungle"],
            ["Underground"],
            ["Others"],
            ["Hallow"],
        ]
    },
    
    "Dealer": {
        "enabled": True,
        "npc_priority": [
            ["Nurse"],
            ["Builder"],
            ["Others"],
            ["Arms Dealer"],
        ],
        "biome_priority": [
            ["Jungle", "Forest"],
            ["Others"],
            ["Desert", "Ocean"],
        ]
    },
    
    "Hephaestus": {
        "enabled": True,
        "npc_priority": [
            ["Others"],
        ],
        "biome_priority": [
            ["Others"],
        ]
    },
    
    "Old Champion": {
        "enabled": True,
        "npc_priority": [
            ["Dryad"],
            ["Others"],
            ["Tax Collector"],
            ["Angler"],
        ],
        "biome_priority": [
            ["Forest", "Desert", "Jungle"],
            ["Others"],
            ["Hallow", "Glowing Mushrooms"],
        ]
    },
    
    "Shooting Star": {
        "enabled": True,
        "npc_priority": [
            ["Truffle"],
            ["Party Girl"],
            ["Others"],
            ["Builder"],
        ],
        "biome_priority": [
            ["Glowing Mushrooms"],
            ["Hallow"],
            ["Others"],
            ["Jungle"],
        ]
    }
}


# ============================================================
# 2. PYLON DATABASE
# ============================================================

PYLONS = {
    "Forest Pylon": {
        "enabled": True,
        "biome_tags": ["Forest"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Jungle Pylon": {
        "enabled": True,
        "biome_tags": ["Jungle"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Hallow Pylon": {
        "enabled": True,
        "biome_tags": ["Hallow"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Cavern Pylon": {
        "enabled": True,
        "biome_tags": ["Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Ocean Pylon": {
        "enabled": True,
        "biome_tags": ["Ocean"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Desert Pylon": {
        "enabled": True,
        "biome_tags": ["Desert"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Snow Pylon": {
        "enabled": True,
        "biome_tags": ["Snow"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Mushroom Pylon": {
        "enabled": True,
        "biome_tags": ["Glowing Mushrooms"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Chlorophyte Pylon": {
        "enabled": True,
        "biome_tags": ["Jungle", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Cloud Pylon": {
        "enabled": True,
        "biome_tags": ["Cloud", "Space", "Forest"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Coral Pylon": {
        "enabled": True,
        "biome_tags": ["Ocean"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Dungeon Pylon": {
        "enabled": True,
        "biome_tags": ["Dungeon", "Forest"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Gem Pylon": {
        "enabled": True,
        "biome_tags": ["Gems", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Glowing Moss Pylon": {
        "enabled": False,
        "biome_tags": ["Glowing Moss", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Granite Pylon": {
        "enabled": True,
        "biome_tags": ["Granite", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Grave Pylon": {
        "enabled": True,
        "biome_tags": ["Graveyard", "Forest"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Honey Pylon": {
        "enabled": True,
        "biome_tags": ["Beehive", "Jungle", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Ice Pylon": {
        "enabled": True,
        "biome_tags": ["Snow", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Living Pylon": {
        "enabled": True,
        "biome_tags": ["Living Tree", "Forest"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Living Mahogany Pylon": {
        "enabled": True,
        "biome_tags": ["Living Mahogany Tree", "Jungle", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Marble Pylon": {
        "enabled": True,
        "biome_tags": ["Marble", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Oasis Pylon": {
        "enabled": True,
        "biome_tags": ["Oasis", "Desert"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Sandstone Pylon": {
        "enabled": True,
        "biome_tags": ["Desert", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Space Pylon": {
        "enabled": True,
        "biome_tags": ["Space", "Forest"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Spider Pylon": {
        "enabled": True,
        "biome_tags": ["Spider Nest", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Temple Pylon": {
        "enabled": True,
        "biome_tags": ["Temple", "Jungle", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Underworld Pylon": {
        "enabled": True,
        "biome_tags": ["Hell", "Underground"],
        "min_npcs": 1,
        "max_npcs": 2
    },

    "Xmas Pylon": {
        "enabled": False,
        "biome_tags": ["Presents", "Snow"],
        "min_npcs": 1,
        "max_npcs": 2
    }
}


# ============================================================
# 3. PRIORITY SYSTEM
# ============================================================

def normalize_groups(priority_list):

    groups = []

    for item in priority_list:

        if isinstance(item, str):
            groups.append([item])

        elif isinstance(item, list):
            groups.append(item)

        else:
            raise ValueError(
                f"Invalid priority entry: {item}"
            )

    return groups


def priority_score(target, priority_list):
    """
    Others is optional.

    If Others exists:
        Unlisted entries receive its score.

    If Others is absent:
        Unlisted entries receive 0.
    """

    groups = normalize_groups(priority_list)

    others_index = next(
        (
            i for i, group in enumerate(groups)
            if any(name.lower() == "others" for name in group)
        ),
        None
    )

    target = target.lower()

    # Find explicitly listed target.
    for index, group in enumerate(groups):

        if any(name.lower() == target for name in group):

            if others_index is None:
                return len(groups) - index

            return others_index - index

    # Unlisted target.
    if others_index is None:
        return 0

    return 0


# ============================================================
# 4. HAPPINESS SCORING
# ============================================================

def biome_score(npc, pylon):

    preferences = NPCS[npc]["biome_priority"]

    # Multiple biome tags are supported.
    # Only the best matching tag counts.

    scores = [
        priority_score(biome, preferences)
        for biome in PYLONS[pylon]["biome_tags"]
    ]

    return max(scores, default=0)


def relationship_score(npc_a, npc_b):
    """
    Both NPCs contribute to the relationship score.

    If A loves B but B dislikes A,
    both preferences are still considered.
    """

    score_a = priority_score(
        npc_b,
        NPCS[npc_a]["npc_priority"]
    )

    score_b = priority_score(
        npc_a,
        NPCS[npc_b]["npc_priority"]
    )

    return score_a + score_b


# ============================================================
# 5. DATA VALIDATION
# ============================================================

def validate_data():

    npcs = [
        name for name, data in NPCS.items()
        if data.get("enabled", True)
    ]

    pylons = [
        name for name, data in PYLONS.items()
        if data.get("enabled", True)
    ]

    if not npcs:
        raise ValueError("No NPCs found.")

    if not pylons:
        raise ValueError("No pylons found.")

    total_min = sum(
        data["min_npcs"]
        for data in PYLONS.values()
    )

    total_max = sum(
        data["max_npcs"]
        for data in PYLONS.values()
    )

    if len(npcs) < total_min:
        raise ValueError(
            "Not enough NPCs to activate all pylons."
        )

    if len(npcs) > total_max:
        raise ValueError(
            "Too many NPCs for the available pylon capacity."
        )

    for npc, data in NPCS.items():

        for field in (
            "npc_priority",
            "biome_priority"
        ):

            groups = normalize_groups(data[field])

            others_count = sum(
                any(
                    name.lower() == "others"
                    for name in group
                )
                for group in groups
            )

            if others_count > 1:
                raise ValueError(
                    f"{npc}: {field} cannot contain multiple Others."
                )

    for pylon, data in PYLONS.items():

        minimum = data["min_npcs"]
        maximum = data["max_npcs"]

        if not data["biome_tags"]:
            raise ValueError(
                f"{pylon} needs at least one biome tag."
            )

        if maximum < minimum:
            raise ValueError(
                f"{pylon}: maximum is below minimum."
            )


# ============================================================
# 6. OPTIMIZATION ENGINE
# ============================================================

def optimize():

    validate_data()

    npcs = [
        name for name, data in NPCS.items()
        if data.get("enabled", True)
    ]

    pylons = [
        name for name, data in PYLONS.items()
        if data.get("enabled", True)
    ]

    model = cp_model.CpModel()

    # --------------------------------------------------------
    # NPC assignment variables
    # --------------------------------------------------------

    x = {}

    for npc in npcs:

        for pylon in pylons:

            x[(npc, pylon)] = model.new_bool_var(
                f"x_{npc}_{pylon}"
            )

    # --------------------------------------------------------
    # NPC pair variables
    # --------------------------------------------------------

    y = {}

    for a, b in combinations(npcs, 2):

        for pylon in pylons:

            var = model.new_bool_var(
                f"pair_{a}_{b}_{pylon}"
            )

            y[(a, b, pylon)] = var

            # Pair exists only if both NPCs live there.

            model.add(
                var <= x[(a, pylon)]
            )

            model.add(
                var <= x[(b, pylon)]
            )

            model.add(
                var >= (
                    x[(a, pylon)]
                    + x[(b, pylon)]
                    - 1
                )
            )

    # --------------------------------------------------------
    # Constraint 1: Every NPC has exactly one home.
    # --------------------------------------------------------

    for npc in npcs:

        model.add(
            sum(
                x[(npc, pylon)]
                for pylon in pylons
            ) == 1
        )

    # --------------------------------------------------------
    # Constraint 2: Every pylon needs 2 to 3 NPCs.
    # --------------------------------------------------------

    for pylon in pylons:

        residents = sum(
            x[(npc, pylon)]
            for npc in npcs
        )

        model.add(
            residents >= PYLONS[pylon]["min_npcs"]
        )

        model.add(
            residents <= PYLONS[pylon]["max_npcs"]
        )

    # --------------------------------------------------------
    # Constraint 3: Maximize total happiness.
    # --------------------------------------------------------

    objective = []

    # Individual biome preferences.

    for npc in npcs:

        for pylon in pylons:

            score = biome_score(npc, pylon)

            objective.append(
                score * x[(npc, pylon)]
            )

    # Relationships between NPCs.

    for a, b in combinations(npcs, 2):

        for pylon in pylons:

            score = relationship_score(a, b)

            objective.append(
                score * y[(a, b, pylon)]
            )

    model.maximize(sum(objective))

    # --------------------------------------------------------
    # Run solver.
    # --------------------------------------------------------

    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = 30
    solver.parameters.num_search_workers = 8

    status = solver.solve(model)

    if status not in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ):

        print("No valid arrangement found.")
        return

    # ========================================================
    # 7. RESULTS
    # ========================================================

    print("\n" + "=" * 55)
    print("TERRARIA NPC OPTIMIZER")
    print("=" * 55)

    print("Status:", solver.status_name(status))
    print("Total score:", solver.objective_value)

    if status == cp_model.OPTIMAL:
        print("Optimal arrangement found.")
    else:
        print("Best arrangement found within time limit.")

    for pylon in pylons:

        residents = [
            npc for npc in npcs
            if solver.value(x[(npc, pylon)])
        ]

        biome_total = sum(
            biome_score(npc, pylon)
            for npc in residents
        )

        relationship_total = sum(
            relationship_score(a, b)
            for a, b in combinations(residents, 2)
        )

        print("\n" + "-" * 55)

        print(pylon)

        print(
            "Biomes:",
            ", ".join(PYLONS[pylon]["biome_tags"])
        )

        print(
            f"Residents: {len(residents)}/"
            f"{PYLONS[pylon]['max_npcs']}"
        )

        for npc in residents:

            print(
                f"  {npc}: "
                f"Biome {biome_score(npc, pylon):+}"
            )

        print("Biome score:", biome_total)
        print("Relationship score:", relationship_total)

        print(
            "Pylon score:",
            biome_total + relationship_total
        )

        # Show relationships between residents.

        print("Relationships:")

        for a, b in combinations(residents, 2):

            print(
                f"  {a} + {b}: "
                f"{relationship_score(a, b):+}"
            )

    print("\n" + "=" * 55)


# ============================================================
# 8. MAIN
# ============================================================

if __name__ == "__main__":
    optimize()
