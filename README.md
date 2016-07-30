# onepasstopass
This tool does a very simple mapping from a [1Password](https://1password.com/) export (1pif) to a set of passwords in [pass](https://www.passwordstore.org/).

This is based on reverse engineering of the 1pif format, so may or may not work for you.

It only tries to import entries of type `webforms.WebForm`, which in 1Password are called "Logins". At present it ignores any other types (credit cards, secure notes et al), though a warning will be displayed so you know they're being skipped.

Any entry which has a location is assumed to be a website, and will be imported as `website/location` (eg `website/amazon.com`). Other entries will be imported as `misc/title` using the title from 1Password.

The content of each entry is the 1Password password field on the first line followed by the notes field on the following lines.

For me this produces sane results. If you have duplicate entries for the same site or anything I haven't come across, it won't work properly. Any damage should be contained to the trees `website` and `misc` in your pass data, so it should be easy to clean up.

## Usage

You can run it like this:
```
./onepasstopass.py ~/Desktop/export.1pif/data.1pif
```

This is just a simple prototype, so there are no supported options just now other than the name of the file to import from.

If you edit the last line of `onepasstopass.py` to call `dump` rather than `sendtopass`, you can dump the parsed output to stdout. Optionally, `dump` takes a parameter which will print the content of each entry as well as the path, including printing the imported passwords.
