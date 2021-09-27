import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set(),
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set(),
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def look_for_way(current_node, data):
    possible_result = []
    possible_result.append(current_node.state)

    visited = []
    visited.append(current_node)
    for x_is_way in data["explored"]:
        if current_node.action == x_is_way.action:
            visited.append(x_is_way)

    def recusrive_fake(next_node):
        while True:
            for x in range(len(visited)):
                if (
                    visited[x].state == next_node.parent
                    and visited[x].parent != data["source"]
                ):
                    next_node = visited[x]
                    possible_result.append(visited[x].state)
                    del visited[x]
                    break

            finish = True
            for x_finish in visited:
                if (
                    x_finish.state == next_node.parent
                    and x_finish.parent != data["source"]
                ):
                    finish = False

            if finish:
                break

    recusrive_fake(current_node)
    possible_result.reverse()
    data["results"].append(possible_result)


def is_explored(node, explored):
    for x_explored in explored:
        if x_explored.state == node.state and x_explored.parent == node.parent:
            return True
    return False


def shortest_path(source, target):
    frontiers_stars = neighbors_for_person(source)

    frontier = StackFrontier()

    explored: list(Node) = []
    results = []
    gps = 0
    data = {
        "results": results,
        "explored": explored,
        "source": source,
        "target": target,
    }

    for star in frontiers_stars:
        node = Node(star, (star[0], source), gps)
        if (
            star[1] != source
            and not frontier.contains_state(star)
            and not is_explored(node, data["explored"])
        ):
            data["explored"].append(node)
            frontier.add(node)
            gps += 1
            if star[1] == target:
                return [star]

    while True:
        try:
            node_frontier: Node = QueueFrontier.remove(frontier)
            frontiers_stars = neighbors_for_person(node_frontier.state[1])
            data["explored"].append(node_frontier)

            for star in frontiers_stars:
                node = Node(star, node_frontier.state, node_frontier.action)
                if (
                    star[1] != source
                    and not frontier.contains_state(star)
                    and not is_explored(node, data["explored"])
                ):
                    frontier.frontier.append(node)

                    if star[1] == target:
                        look_for_way(frontier.frontier[-1], data)
                        return data["results"][0]

        except Exception:
            return None

    return data["results"][0] or None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
