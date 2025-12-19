f = open("source.txt", "r+")
f.write("\nNew line added.")
print(f.read())
f.close()
