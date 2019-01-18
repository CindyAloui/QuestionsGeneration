import io
import os


if __name__ == "__main__":
    dirName = "data/QuestionsPatterns_auto"
    for fname in os.listdir(dirName):
        f = io.open(os.path.join(dirName, fname))
        contents = f.readlines()
        frame_name = fname[:-6]
        f.close()
        i = 0
        j = 0
        while i < len(contents):
            line = contents[i]
            if not line.strip():
                i += 1
                continue
            if "#Pattern" in line :
                contents[i] = "#Pattern_" + frame_name + "_" + str(j) + "\n"
                j += 1
                i += 3
                continue
            contents.insert(i, "#Pattern" + frame_name + "_" + str(j) + "\n")
            j += 1
            i += 3

        f = open(os.path.join(dirName, fname), "w")
        contents = "".join(contents)
        f.write(contents)
        f.close()
