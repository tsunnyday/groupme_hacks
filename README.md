# groupme_hacks
Playing around with the GroupMe API

A proof of concept of some of the issues with vanilla GroupMe (without GORT).
Any actual malicious action done with this code is not my responsibility.

Basic usage -

Make a fake groupme account using Guerilla Mail and a free text number (like TextFree for Android)
Sign in to groupme's developer page and get an API token.

With group_me_commands.py, you can remove all members besides the owner of a group, then by impersonating the owner,
create a new group with all of those members with the same name as the original group.

In this way, in the original group, the owner is left all by his lonesome, and a new,
identical group is created with you as the owner.

