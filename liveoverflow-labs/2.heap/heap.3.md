## heap3

TODO: writeup + diagrams.

This level is the “unsafe unlink / heap metadata corruption” style challenge. It requires crafting a fake chunk so that one of the `free()` calls performs an unlink that writes to an attacker-chosen address (typically a GOT entry) and redirects control flow to `winner()`.

I’ll implement this after `heap0–2` are verified, because it’s substantially more involved and very allocator/version dependent.
