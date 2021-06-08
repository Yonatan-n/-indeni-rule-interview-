def is_name_similar(name1: str, name2: str) -> bool:
    index = 0
    flag = False
    while index < min(len(name1), len(name2)):
        if name1[index] != name2[index]:
            flag = True
            break
        index += 1
    if flag == False and max(len(name1), len(name2)) - index <= 1: # 1 letter diff or less
        return True
    if name1[index+1:] == name2[index:] or name1[index:] == name2[index+1:] or (name1[index:]) == (name2[index:]) :
        return True
    return False
    