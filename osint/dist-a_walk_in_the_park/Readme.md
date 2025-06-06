# A Walk In The Park
The difficulty of OSINT challenges tend to depend on the stinginess of initial information provided, as well as ease of finding and following subsequent leads. In this challenge, we were given an image of a censored park signage and tasked to locate it accurately. Thankfully, it was clearly within Singapore, which you'd think would narrow the search by a huge margin, but in reality, did not. 

![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/a_walk_in_the_park.jpg)

Based on previous OSINT challenges in other competitions, I have once made the mistake of examining an image and trying to extract every metadata there is in order to retrieve the flag, only for the answer to be as simple as an reverse image search.  
This time, I've tried to reverse image search instead, just for the initial lead to be hidden in the image's metadata :sob:.  
Unfortunately I was too heckled by other challenges at that point in time to figure this out within the challenge deadline, but safe to say this was a tough lesson learnt.

After figuring out the answer, this challenge is quite similar to the OSINT challenge in CDDC2025 where we were tasked to find a DOI based on an image of a moon.

The general workflow is intuitive:
1. extract image metadata
2. stalk the username of the 'Artist'
3. follow leads and the flag will emerge

Extracting image metadata can be done simply using `exiftool`, as shown below:

![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/exif_park.png)

From there, we can take into account a few red flags. 
- Odd resolution values
  ```
  X Resolution: 1
  Y Resolution: 1
  Resolution Unit: None
  ```
  Normally, DPI values of 72, 96 or 300, and a resolution unit of `inches` or `cm` are expected.
- `Date/ Time Original`, `Create Date`, and `Modify Date` are all exactly `2025:05:21 16:55:21`.
  This is impossible in natural photography workflows for obvious reasons.
- File size and megapixels
  ```
  File Size: 293 KB
  Image Size: 841x1565 (≈ 1.3 MP)
  ```
  There is a relatively high pixel count for such a small file size, suggesting heavy compression.

These can all suggest manual crafting or editing of metadata, while the suspicious file size can also suggest compression to fit within challenge constraints. Basically, these may not be as suspicious in the context of a CTF, but will keep them in mind when I get stuck potentially later. 

For now, I have chosen to follow the easiest lead: the Artist, Owner, and Copyright owner, `the_real_lim_kx`. Googling gave me no results, but a trend in OSINT challenges is using Twitter or Instagram. As my Twitter had not been updated in a while, I've decided to try IG first. 

While IG did show me exactly 1 result for my search, initial glimpse of his posts and bio gave no leads or clues. Only after opening his stories do I get some sense of relief from a GreyCTF shoutout.

![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/ig_gctf.jpg)

Further stalking did not give anymore details nor clues about this guy's relation to the park. However, he seems to have a real passion for running given his following stories:

![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/ig_watch.jpg)


I figured no chill runner would consider getting a triathlon watch or make up public running polls. He is clearly from Singapore and the only places he can have intense running trainings is probably in a public park, which is highly likely where the signage where we are tasked to find lies in.

The most popular app for tracking exercises in Singapore is probably Strava (it is also the only app I have for exercising). If Strava came up with nothing I was planning hit up some friends who are more athletic for their suggestions on other apps they use. 
Thankfully, my search for the same username came up with just 1 result, with the same name and profile picture. 

![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/serangoon_run.jpg)
![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/bedok_run.jpg)

Thankfully we are only expected to search through 2 parks, with the 3rd activity seeming more like a red herring. 
Following his route along Upper Serangoon road, we find a relatively small interim park somewhere in the middle of his tracks.
When I clicked on it, I was immediately shown the image:

![alt text](https://github.com/qmkoh/Greyctf2025-writeups/blob/main/osint/dist-a_walk_in_the_park/flag.png)

Though at a slightly different angle, the prominent red and white building at the back is still present, along with other familiar infrastructures. 

Thus we get the flag:
`grey{interim_park_upper_serangoon_road}`
