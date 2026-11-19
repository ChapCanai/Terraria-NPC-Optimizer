import json
import os
from pathlib import Path
from ortools.sat.python import cp_model
from itertools import combinations


# ============================================================
# SETTINGS

BASE_FOLDER = Path(__file__).parent

NPC_FOLDER = BASE_FOLDER / "npcs"
PYLON_FOLDER = BASE_FOLDER / "pylons"

MAX_OPTIMIZER_SECONDS = 120


# ============================================================
# JSON LOADER

def load_database(folder):
    database = {}

    for root, dirs, files in os.walk(folder):

        # Ignore disabled folders at every depth.
        dirs[:] = [
            directory
            for directory in dirs
            if directory.lower() != "_disabled"
        ]

        for filename in files:

            if not filename.lower().endswith(".json"):
                continue

            file_path = Path(root) / filename
            name = file_path.stem

            if name in database:
                raise ValueError(
                    f"Duplicate entry '{name}': {file_path}"
                )

            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError(
                    f"{file_path} must contain a JSON object."
                )

            database[name] = data

    return database

NPCS = load_database(NPC_FOLDER)
PYLONS = load_database(PYLON_FOLDER)


# ============================================================
# PRIORITY SYSTEM

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
# HAPPINESS SCORING

def biome_score(npc, pylon):

    preferences = NPCS[npc]["biome_priority"]

    # Multiple biome tags are supported.
    # Only the best matching tag counts.

    scores = [
        priority_score(biome, preferences)
        for biome in PYLONS[pylon]["biome_tags"]
    ]

    return min(scores, default=0)


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
# DATA VALIDATION

def validate_data():
    
    npcs = list(NPCS.keys())
    pylons = list(PYLONS.keys())

    if not npcs:
        raise ValueError("No NPCs found.")

    if not pylons:
        raise ValueError("No pylons found.")

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

        if not data["biome_tags"]:
            raise ValueError(
                f"{pylon} needs at least one biome tag."
            )
        

# ============================================================
# OPTIMIZATION ENGINE

def optimize():

    validate_data()

    npcs = list(NPCS.keys())
    pylons = list(PYLONS.keys())

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
    # Constraint 2: Distribute NPCs as evenly as possible.
    # --------------------------------------------------------

    total_npcs = len(npcs)
    total_pylons = len(pylons)

    min_residents = total_npcs // total_pylons
    max_residents = -(-total_npcs // total_pylons)

    for pylon in pylons:

        residents = sum(
            x[(npc, pylon)]
            for npc in npcs
        )

        model.add(residents >= min_residents)
        model.add(residents <= max_residents)

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

    solver.parameters.max_time_in_seconds = MAX_OPTIMIZER_SECONDS
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

        print(f"Residents: {len(residents)}")

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
# MAIN

if __name__ == "__main__":
    optimize()
