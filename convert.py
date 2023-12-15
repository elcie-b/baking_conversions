
def input_conversions(filename):
    """
    creates dictionary with ingredients as the keys and how many grams a cup weighs as the value

    Args:
        filename (string): name of file with gram values

    Returns:
        dictionary: maps gram values of a cup to corresponding ingredient
    """
    dict = {}
    file = open(filename, "r")
    for line in file:
        splits = line.split(",")
        ingredient = splits[0].replace(" ", "")
        cup_grams = int(splits[1].strip())
        if ingredient not in dict.keys():
            dict[ingredient] = cup_grams
    return dict
    
def process_recipe(filename, dict):
    """
    runs through each line of recipe file and calls read_ingredients 
    method when it finds an ingredient line

    Args:
        filename (string): recipe filename
        dict (dictionary): maps gram values of a cup to corresponding ingredient
    """
    infile = open(filename, "r")
    outfile = open("gram_recipe.txt", "w")
    while True:
        line = infile.readline()
        if "ingredient" in line:
            outfile.writelines(line)
            read_ingredients(infile, outfile, dict)
        if not line:
            break
        else:
            outfile.writelines(line)
            
def read_ingredients(infile, outfile, dict):
    """
    runs through ingredient section and call process_cup_line when 
    it finds a line that contains convertable measurements

    Args:
        infile (file): recipe file
        outfile (file): output file with converted recipe
        dict (dictionary): maps gram values of a cup to corresponding ingredient
    """
    while True:
        line = infile.readline()
        if not line:
            break
        if "cup" in line:
            process_cup_line(line, outfile, dict)
        else:
            outfile.writelines(line)
        
def process_cup_line(line, outfile, dict):
    """
    writes line to outfile after replacing cup measurement with gram measurement

    Args:
        infile (file): recipe file
        outfile (file): output file with converted recipe
        dict (dictionary): maps gram values of a cup to corresponding ingredient
    """
    splits = line.split(" ")
    for i in range(len(splits)):
        if "cup" in splits[i]:
            #relavant number will always occur right before "cup" or "cups"
            number = float(splits[i - 1])
            #find how many other words are in the line after the measurement
            remaining_range = len(splits) - i - 1
            #pull ingredient words from splits and reconstitute them, excluding words within parenthesis
            ingredient = ""
            difference = len(splits) - remaining_range
            for j in range(remaining_range):
                if "(" in splits[difference + j] or ")" in splits[difference + j]:
                    pass
                else:
                    ingredient += splits[difference + j].strip()
            #convert from cup value to gram value and rewrite the line
            #if ingredient not in dictionary, use the original line
            if ingredient in dict.keys():
                grams = number * dict[ingredient]
                if number.is_integer():
                    number = int(number)
                line = line.replace(str(number), str(grams)).replace("cups", "grams").replace("cup", "grams")
                outfile.writelines(line)
            else:
                outfile.writelines(line)
    
def main():
    dict = input_conversions("conversions.txt")
    process_recipe("recipe.txt", dict)
    print("done")
    
if __name__  == "__main__":
    main()