chelseaPlayers = {
    "Morata": "Spanish",
    "Willian": "Brazilian",
    "Hazard": "Belgian",
    "Cahill": "English",
    "Christensen": "Danish",
    "Kante": "French"
}

print(len(chelseaPlayers))

print("Andreas Christensen is " + chelseaPlayers.get("Christensen"))

#Deletes Value with selected key
del chelseaPlayers["Morata"]
print(chelseaPlayers)

print(chelseaPlayers.keys(), end="")
print(chelseaPlayers.values())

chelseaPlayers["Jorginho"] = "Italian"

print(chelseaPlayers)



