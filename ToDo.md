1. ~~Work on the embed that will be sent when asking for a stigmata~~
   1. ~~Embed 1 has top stigmata information~~
   2. ~~Embed 2 has mid stigmata information~~
   3. ~~Embed 3 has bot stigmata information~~
2. ~~Work on the embed containing the 2set and 3set effect.~~
3. Figure out which stigmata sets do not work with the current code and fix them (3set only for now)
   1. All stigmata sets that have the word (Stigmata) do not work because there is an extra box in the website.
      1. 'div' {'class':'infobox-base infobox-border'}
   2. Some stigmata dont have a back picture so consider not stacking the pictures and just using the front one.
4. Add the code to find single stigmata (single not set)
5. Add weapon information
6. Add battlesuit information (if available)
7. Use the find_all string argument to get rid of unwanted information.
8. Find the stigmata images by searching for width and height of 720px. and with relative z of 3. Or find the image by searching for alt text of Stig name + (T).png Also forget about image stacking (not worth it)
