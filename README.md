# ha-hunter
Homograph Domain Attacks Hunter

I was reading this https://wildfire.blazeinfosec.com/what-you-see-is-not-what-you-get-when-homographs-attack

The technique isn't really fresh, it has been around for some time... but I still thought it was cool and wanted to try it out.

Keep in mind that most modern web clients will convert these Internationalized Domain Names to Punycode to prevent confusion.

TLDR:
Homoglyphs are characters that belong to different alphabets that look alike. Sometimes depending on the font they happen to get rendered in a visually indistinguishable way, making it impossible for a user to tell the difference between them.

For the naked eye 'a' and 'а' looks the same (a homoglyph), but the former belongs to the Latin script and the latter to Cyrillic. While for the untrained human eye it is hard to distinguish between both of them, they may get interpreted entirely different by computers.

We can use homoglyphs to build homographs, which are are two strings that seem to be the same but are in fact different.
For example:
- https://www.apple.com (Latin)
- https://www.аррӏе.com (Cyrillic)

With this technique it's possible to create domain names that look indistinguishable from the legitimate ones.

Red Teams could use these domain names for their campaigns. Blue teams should hunt for these domain names.

## Why did I write this?

I had read of this other tool called ha-finder https://github.com/loganmeetsworld/homographs-talk/tree/master/ha-finder
it takes a list of domain names and replaces all possible letters with their homoglyphs.

What makes ha-hunter different is that it generates homographs with all possible character combinations. This means it generates homographs with 1 glyph replaced or 2 or 3 or as many combinations there can be. 
...also, it's written in python3.

## Usage
Clone it, install the requirements and run it as:
$ python3 hhunter.py target_domains.txt
