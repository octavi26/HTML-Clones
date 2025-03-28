# HTML Clones

## Task

The project was to write a script that aims to group together different HTML files based on their appearance and how they are percieved from the user. Even though 2 HTML files can be different, they have simmilarities and these can determine how much they resemble each other.

## Idea

The script work by assosiacting a score for two files being simmilar and then calculates based on said score the probability that they are clones. It clusters files based on how well they compare to the other files in the cluster and if the probability is'nt high enough, the file is given a new cluster of its own. To determine the score of two files being simmilar, we reduce the ammount of data from one big file to small essential things, easy to check. More precisesly, a HTML file will be represented as it's files size, what links / anchors it has, what colors it has and what images it uses. Checking for 2 files things based on these characteristics can help determine the score we are looking for.

## Script

Firstly, the code opens a directory and looks for the HTML files to parse them one by one. For each file, we firstly eliminate the comments and get the links, colors and images from the file using the function getPart(s, begining, end) that returns a substring of s that starts with 'begining' and ends with 'end'. Now, representing the file with this smaller set of information we can check for each cluster what is the probability that it sould be part of it. To answer this, we calculate the simmilarity between the current file and every file in a cluster to then average them at the end. To calculate the proabability we take the part of the amount of points the pair of files make in raport to the amount of points which it could have, which is the amount of points from a file to itself. Now, we calculate these points / score with the function Points(D, DC) whichs look at the representatives of the files. Firstly, if the size difference from the file is smaller than 10% it will recieve a maximum of 4000 points depending of how big the difference. Then, we check if the files have the same links by counting the amount of links in common and giving 500 points for every link they have in common. We do this because links are a big part on how the page appears, representing nuttons and structer of the page. Then, we do the same thing with how many colors are in common. This is important as two pages look more simmilar if they have the same colors and therefor, for each color in common we get 250 points. Same thing with images and we get 1000 for every common image between the two.
Finaly, we calculate and select the cluster with the highest probability of it containing the file and if the simmilarities are more than 60% for the higest probability then the file is accepted in the cluster. If not, it means the file doesn't belong in any cluster so far so it makes a cluster for itself.

## Versatility

The solution is designed to be versatile and change the values for the scorse to better accentuate the importance of one aspect in front of another. For example we could choose to give more importance to colors and add 750 points for each common color instead of 150.
More than that, using the Points and getPart functions it is easy to add more criterias for two files to be simmilar other than size, links, colors and images. We could probably add a check for the scripts of the files.
