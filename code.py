from pathlib import Path
import os

def removeHTMLcomments(File):
    while "<!--" in File:
        indexStart = File.index("<!--")
        indexEnd = File[indexStart + 4:].index("-->")
        File = File[:indexStart] + File[indexStart + 4:][indexEnd + 3:]
    while "/*" in File:
        indexStart = File.index("/*")
        indexEnd = File[indexStart + 2:].index("*/")
        File = File[:indexStart] + File[indexStart + 2:][indexEnd + 2:]

def getPart(text, start, end):
    if start not in text or end not in text:
        return None
    
    indexStart = text.index(start)
    indexEnd = text[indexStart + len(start):].index(end) + len(end)

    return text[indexStart:indexEnd + len(start) + indexStart]

def Points(D, DC):
    points = 0

    # File Size
    sizeDifference = abs(D['size'] - DC['size'])
    if sizeDifference / max(D['size'], DC['size']) * 100 < 10:
        points += (10 - sizeDifference / max(D['size'], DC['size']) * 100) * 400

    # Links
    linkDifference = abs(len(D['links']) - len(DC['links']))
    linkCommon = D['links'] & DC['links']
    if linkDifference < 25:
        points += (25 - linkDifference) * 20
    points += len(linkCommon) * 500

    # Images
    imgDifference = abs(len(D['imgs']) - len(DC['imgs']))
    imgCommon = D['imgs'] & DC['imgs']
    if imgDifference < 25:
        points += (25 - imgDifference) * 20
    points += len(imgCommon) * 1000

    # Colors
    colorsCommon = D['colors'] & DC['colors']
    points += len(colorsCommon) * 250

    return points


if __name__ == "__main__":
    # Opens Directory
    tier = str(input("Tier to check: "))
    directory = str(Path.cwd()) + "/clones/tier" + str(tier)
    ## print(directory)

    L = os.listdir(directory)

    for i in range(len(L)):
        if L[i][0] == ".":
            continue
        File = "".join(open(directory + "/" + L[i], "r", encoding="utf-8").read().strip().split())

        D = {} # The Dictionary representing the HTML file
        D['name'] = L[i] # Name of the file
        D['size'] = os.stat(directory + "/" + L[i]).st_size # size of the file

        # Removing any comments from the file as it doesn not affect the end-result
        removeHTMLcomments(File)

        # Get Links
        Links = []
        link = getPart(File, "href=\"", "\"")
        while link:
            Links.append(link)
            File = File.replace(link, "")
            link = getPart(File, "href=\"", "\"")
        Links = set(Links)
        D["links"] = Links # Links of the file

        # Get Images
        Images = []
        img = getPart(File, "img src=\"", "\"")
        while img:
            Images.append(img)
            File = File.replace(img, "")
            img = getPart(File, "img src=\"", "\"")
        Images = set(Images)
        D["imgs"] = Images # Images of the file

        # Get Colors
        Colors = []
        # rgb()
        color = getPart(File, "rgb(", ")")
        while color:
            Colors.append(color)
            File = File.replace(color, "")
            color = getPart(File, "rgb(", ")")
        # rgba()
        color = getPart(File, "rgba(", ")")
        while color:
            Colors.append(color)
            File = File.replace(color, "")
            color = getPart(File, "rgba(", ")")
        # #ffffff
        color = File[File.index("#"):File.index("#") + 7] if "#" in File else None
        while color:
            Colors.append(color)
            File = File.replace(color, "")
            color = File[File.index("#"):File.index("#") + 7] if "#" in File else None

        Colors = set(Colors)
        D["colors"] = Colors # Colors of the file

        # Final:
        L[i] = D # Replacing the file with the dictionary representing it


    Clusters = [[L[0]]] # The Clusters that are gonna be forming from cloned HTMLs
    for i in range(1, len(L)):
        D = L[i]

        maxProbability = 0
        selectedCluster = []
        for cluster in Clusters:
            # calculating the probability score for it being part of the current cluster
            probability = 0
            for DC in cluster:
                probability += Points(D, DC) / Points(D, D) * 100
            probability /= len(cluster)

            # selecting the cluster with the highest probability
            if probability > maxProbability:
                maxProbability = probability
                selectedCluster = cluster
        
        # if the maximum probability for it being part of a cluster is higher then 60, then it is enough
        # else, it must create a cluster of its own
        if maxProbability > 60:
            selectedCluster.append(D)
        else:
            Clusters.append([D])

    # Rpinting the Clusters
    for cluster in Clusters:
        print([(D['name'], D['size']) for D in cluster], end="\n")

    # Printing the average probability for each cluster
    #
    # for i in range(len(Clusters)):
    #     D = Clusters[i][0]
    #     probability = 0
    #     for j in range(1, len(Clusters[i])):
    #         DC = Clusters[i][j]
    #         probability += Points(D, DC) / Points(D, D) * 100
    #     if len(Clusters[i]) > 1:
    #         probability /= (len(Clusters[i]) - 1)
    #     else:
    #         probability = 100
    #     print(str(probability) + "%")

