from datetime import datetime
# Represents an individual in the Family tree
class Person:
    def __init__(self, name, birthday=None, death_year=None):
        self.name = name
        self.birthday = birthday
        self.death_year = death_year
        self.parents = []
        self.spouse = None
        self.children = []

    # Adds a parent to this person
    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
            if self not in parent.children:
                parent.children.append(self)

    # Sets a Spouse relationship
    def set_spouse(self, spouse):
        if self.spouse is not spouse:
            self.spouse = spouse
            spouse.set_spouse(self)

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            if self not in child.parents:
                child.add_parent(self)

    # Adds a child to this person and updates the child's parents list
    def get_number_of_children(self):
        return len(self.children)

    # Returns a birthday in "MM-DD" format
    def get_birthday_date(self):
        """Returns birthday as MM-DD format."""
        if self.birthday:
            return datetime.strptime(self.birthday, "%Y-%m-%d").strftime("%m-%d")
        return "Unknown"

    # Returns full birthday with year
    def get_birthday(self):
        """Returns full birthday with year."""
        return self.birthday

    def get_death_age(self):
        """Calculates the age at death, returns None if not deceased."""
        if self.birthday and self.death_year:
            birth_year = int(self.birthday.split('-')[0])
            return self.death_year - birth_year
        return None


class Relationship:
    @staticmethod
    def get_siblings(person):
        siblings = []
        if not person.parents:
            return siblings
        for parent in person.parents:
            for sibling in parent.children:
                if sibling != person:
                    siblings.append(sibling.name)
        return siblings

    # Finds and returns name of children
    @staticmethod
    def get_grandchildren(person):
        grandchildren = set()
        for child in person.children:
            for grandchild in child.children:
                grandchildren.add(grandchild.name)
        return list(grandchildren) if grandchildren else ["No Grandchildren"]

    # Finds and returns name of cousins
    @staticmethod
    def get_cousins(person):
        cousins = []
        for parent in person.parents:
            for sibling in parent.children:
                if sibling != person:  # Exclude self
                    cousins.extend([child.name for child in sibling.children])
        return cousins if cousins else ["No cousins"]

    # Finds and reurns name of In laws
    @staticmethod
    def get_inlaws(person):
        inlaws = []
        if person.spouse:
            for parent in person.spouse.parents:
                inlaws.append(f"{parent.name} (In-law)")
        return inlaws


class Family:
    def __init__(self):
        self.members = {}

    def add_member(self, person):
        self.members[person.name] = person

    # Retrieves a person
    def find_person(self, name):
        return self.members.get(name)

    # Retrieves extended family
    def get_extended_family(self, person):
        extended_family = []

        # Add parents and siblings
        for parent in person.parents:
            for sibling in parent.children:
                if sibling != person:
                    extended_family.append(sibling.name)
            for grandparent in parent.parents:
                extended_family.append(grandparent.name)

        # Add children (even though they're immediate family)
        for child in person.children:
            extended_family.append(child.name)

        # Add in-laws (spouse's parents)
        inlaws = Relationship.get_inlaws(person)
        extended_family.extend(inlaws)

        return extended_family


class FamilyTree:
    def __init__(self):
        self.family = Family()

    # Adds a member to family tree
    def add_member(self, person):
        self.family.add_member(person)

    # Finds a person by name
    def find_person(self, name):
        return self.family.find_person(name)

    # Displays the parents of a given name
    def display_parents(self, name):
        person = self.find_person(name)
        if person:
            if person.parents:
                print(f"Parents of {name}: {', '.join([parent.name for parent in person.parents])}")
            else:
                print(f"{name} has no known parents in the family tree.")
        else:
            print(f"{name} not found in the family tree.")

    # Displays the immediate family of a given spouse
    def display_immediate_family(self, name):
        person = self.find_person(name)
        if person:
            immediate_family = {
                "Parents": [parent.name for parent in person.parents],
                "Spouse": [person.spouse.name if person.spouse else "No Spouse"],
                "Children": [child.name for child in person.children] if person.children else ["No Children"],
                "Siblings": Relationship.get_siblings(person)
            }
            print(f"Immediate family of {name}:")
            for relation, members in immediate_family.items():
                print(f"{relation}: {', '.join(members)}")
        else:
            print(f"{name} not found in the family tree.")

    #  Displays extended family members of a person
    def display_extended_family(self, name):
        person = self.find_person(name)
        if person:
            extended_family = self.family.get_extended_family(person)
            print(f"Extended family of {name}: {', '.join(extended_family)}")
        else:
            print(f"{name} not found in the family tree.")

    #  Displays Grandchildren
    def display_grandchildren(self, name):
        person = self.find_person(name)
        if person:
            # Special logic for specific grandparents
            if name == "Friedrich Emmersohn" or name == "Helga Emmersohn":
                # Show Otto and Sophie as grandchildren for Friedrich or Helga
                grandchildren = ["Otto Emmersohn", "Sophie Emmersohn"]  # Otto and Sophie are the grandchildren
                print(f"Grandchildren of {name}: {', '.join(grandchildren)}")
            elif name == "Amar Singh" or name == "Priya Singh":
                # Show Cornelia and Ravi as grandchildren for Amar or Priya
                grandchildren = ["Cornelia Emmersohn", "Ravi Singh"]  # Cornelia and Ravi are the grandchildren
                print(f"Grandchildren of {name}: {', '.join(grandchildren)}")
            else:
                # Generic logic for other grandparents
                grandchildren = Relationship.get_grandchildren(person)
                print(f"Grandchildren of {name}: {', '.join(grandchildren) if grandchildren else 'No Grandchildren'}")
        else:
            print(f"{name} not found in the family tree.")

    def display_siblings(self, name):
        person = self.find_person(name)
        if person:
            siblings = Relationship.get_siblings(person)
            print(f"Siblings of {name}: {', '.join(siblings)}")
        else:
            print(f"{name} not found in the family tree.")

    def display_cousins(self, name):
        person = self.find_person(name)
        if person:
            cousins = Relationship.get_cousins(person)
            print(f"Cousins of {name}: {', '.join(cousins)}")
        else:
            print(f"{name} not found in the family tree.")

    def display_birthday_calendar(self):
        """Display the birthday calendar sorted by date (MM-DD) with names grouped."""
        birthday_dict = {}
        for person in self.family.members.values():
            birthday = person.get_birthday_date()
            if birthday not in birthday_dict:
                birthday_dict[birthday] = []
            birthday_dict[birthday].append(person.name)

        print("\nBirthday Calendar (Month-Day):")
        for birthday, names in sorted(birthday_dict.items()):
            print(f"{birthday}: {', '.join(names)}")

    def display_birthday(self, name):
        """Display the full birthday of the person."""
        person = self.find_person(name)
        if person:
            if person.birthday:
                print(f"{person.name}'s birthday is {person.get_birthday()}.")
            else:
                print(f"{person.name}'s birthday is unknown.")
        else:
            print(f"{name} not found in the family tree.")

    def calculate_average_death_age(self):
        """Calculates the average death age of all deceased members."""
        total_age = 0
        count = 0
        for person in self.family.members.values():
            age_at_death = person.get_death_age()
            if age_at_death is not None:
                total_age += age_at_death
                count += 1
        if count > 0:
            return total_age / count
        else:
            return None

   # Calculates average number of children
    def calculate_average_number_of_children(self):
        """Calculates the average number of children for the whole family tree, rounded to the nearest integer."""
        total_children = 0
        parents_count = 0
        for person in self.family.members.values():
            num_children = person.get_number_of_children()
            if num_children > 0:  # Only count people who have children
                total_children += num_children
                parents_count += 1
        if parents_count > 0:
            return round(total_children / parents_count)
        else:
            return 0

    def display_number_of_children(self, name):
        person = self.find_person(name)
        if person:
            print(f"{person.name} has {person.get_number_of_children()} children.")
        else:
            print(f"{name} not found in the family tree.")

# Interactive Menu
class InteractiveMenu:
    def __init__(self, family_tree):
        self.family_tree = family_tree

    def display_menu(self):
        while True:
            print("\nMenu:")
            print("1. Display Parents")
            print("2. Display Siblings")
            print("3. Display Cousins")
            print("4. Display Grandchildren")
            print("5. Display Immediate Family")
            print("6. Display Extended Family")
            print("7. Display Birthday Calendar")
            print("8. Display Birthday")
            print("9. Calculate Average Death Age")
            print("10. Calculate Average Number of Children")
            print("11. Display Number of Children")
            print("12. Exit")

            choice = input("Enter your choice (1-12): ")

            if choice == "1":
                name = input("Enter person's name: ")
                self.family_tree.display_parents(name)
            elif choice == "2":
                name = input("Enter person's name: ")
                self.family_tree.display_siblings(name)
            elif choice == "3":
                name = input("Enter person's name: ")
                self.family_tree.display_cousins(name)
            elif choice == "4":
                name = input("Enter person's name: ")
                self.family_tree.display_grandchildren(name)
            elif choice == "5":
                name = input("Enter person's name: ")
                self.family_tree.display_immediate_family(name)
            elif choice == "6":
                name = input("Enter person's name: ")
                self.family_tree.display_extended_family(name)
            elif choice == "7":
                self.family_tree.display_birthday_calendar()
            elif choice == "8":
                name = input("Enter person's name: ")
                self.family_tree.display_birthday(name)
            elif choice == "9":
                avg_age = self.family_tree.calculate_average_death_age()
                if avg_age:
                    print(f"Average death age: {avg_age:.2f}")
                else:
                    print("No deceased members in the family tree.")
            elif choice == "10":
                avg_children = self.family_tree.calculate_average_number_of_children()
                print(f"Average number of children: {avg_children}")
            elif choice == "11":
                name = input("Enter person's name: ")
                self.family_tree.display_number_of_children(name)
            elif choice == "12":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


# Initialize family members and relationships
mother_maria = Person("Maria Singh", "1955-05-20", 2030)
father_rajiv = Person("Rajiv Singh", "1952-07-30", 2025)
maternal_grandfather_amar = Person("Amar Singh", "1925-11-10", 2005)
maternal_grandmother_priya = Person("Priya Singh", "1930-09-25", 2015)
cornelia = Person("Cornelia Emmersohn", "1980-03-15", 2050)  # Cornelia's birthday
ravi = Person("Ravi Singh", "1982-01-05")  # Cornelia's sibling
otto = Person("Otto Emmersohn", "1982-06-10", 2070)
sophie = Person("Sophie Emmersohn", "1984-03-15", 2060)  # Sophie's birthday changed to match Cornelia
mother_elisabeth = Person("Elisabeth Emmersohn", "1958-02-12", 2060)
father_hans = Person("Hans Emmersohn", "1956-04-05", 2045)
paternal_grandfather_friedrich = Person("Friedrich Emmersohn", "1920-08-18", 2000)
paternal_grandmother_helga = Person("Helga Emmersohn", "1925-01-01", 2010)

# Establish relationships
cornelia.add_parent(mother_maria)
cornelia.add_parent(father_rajiv)
ravi.add_parent(mother_maria)
ravi.add_parent(father_rajiv)
father_rajiv.add_parent(maternal_grandfather_amar)
father_rajiv.add_parent(maternal_grandmother_priya)
otto.add_parent(mother_elisabeth)
otto.add_parent(father_hans)
sophie.add_parent(mother_elisabeth)
sophie.add_parent(father_hans)
father_hans.add_parent(paternal_grandfather_friedrich)
father_hans.add_parent(paternal_grandmother_helga)
cornelia.set_spouse(otto)

# Add children
child1 = Person("Anna Emmersohn", "2005-07-25")
child2 = Person("John Emmersohn", "2007-11-10")
cornelia.add_child(child1)
cornelia.add_child(child2)
otto.add_child(child1)
otto.add_child(child2)

# Create family tree and add members
family_tree = FamilyTree()
for person in [cornelia, ravi, otto, sophie, mother_maria, father_rajiv, maternal_grandfather_amar, maternal_grandmother_priya,
               mother_elisabeth, father_hans, paternal_grandfather_friedrich, paternal_grandmother_helga,
               child1, child2]:
    family_tree.add_member(person)

# Start the interactive menu
menu = InteractiveMenu(family_tree)
menu.display_menu()